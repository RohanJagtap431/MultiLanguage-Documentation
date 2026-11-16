
import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import (
    ClassAccess,
    Subject,
    Exam,
    Question,
    GeneratedPaper,
)


import json
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.utils import timezone

from groq import Groq

from .models import (
    ExamResult,
    AnswerKey,
    MCQOption,
)


PAPER_PATTERN = {
    20: {"mcq": 5, "short": 3, "long": 1},
    30: {"mcq": 6, "short": 4, "long": 2},
    40: {"mcq": 10, "short": 4, "long": 3},
}


@login_required
def class_dashboard(request):
    assigned_class = None
    subjects = []

    if not request.user.is_superuser:
        class_access = (
            ClassAccess.objects
            .select_related("academic_class")
            .filter(
                student=request.user,
                academic_class__is_active=True
            )
            .first()
        )

        if class_access:
            assigned_class = class_access.academic_class
            subjects = (
                assigned_class.subjects
                .filter(is_active=True)
                .order_by("name")
            )

    return render(
        request,
        "examination/class_dashboard.html",
        {
            "assigned_class": assigned_class,
            "subjects": subjects,
        }
    )


@login_required
def question_papers(request):
    class_access = (
        ClassAccess.objects
        .select_related("academic_class")
        .filter(
            student=request.user,
            academic_class__is_active=True
        )
        .first()
    )

    if not class_access:
        messages.error(request, "Tumhala class assign kelela nahi.")
        return redirect("examination:class_dashboard")

    assigned_class = class_access.academic_class

    subjects = Subject.objects.filter(
        academic_class=assigned_class,
        is_active=True
    ).order_by("name")

    selected_subject = ""
    selected_marks = ""

    if request.method == "POST":
        
        selected_subject = request.POST.get("subject", "")
        selected_marks = request.POST.get("marks", "")
        

        if selected_marks not in ["20", "30", "40"]:
            messages.error(request, "Invalid paper marks.")

        else:
            exam = Exam.objects.filter(
                subject__in=subjects,
                subject_id=selected_subject,
                total_marks=int(selected_marks),
                is_published=True
            ).first()

            if not exam:
                messages.error(
                    request,
                    "Ya subject sathi published exam available nahi."
                )
            else:
                pattern = PAPER_PATTERN[exam.total_marks]

                questions_by_type = {}

                for question_type, required_count in pattern.items():
                    candidates = list(
                        Question.objects.filter(
                            subject=exam.subject,
                            question_type=question_type,
                            is_active=True,
                            answer_key__isnull=False
                        ).annotate(
                            option_count=Count("options"),
                            correct_count=Count(
                                "options",
                                filter=Q(options__is_correct=True)
                            )
                        )
                    )

                    if question_type == "mcq":
                        candidates = [
                            q for q in candidates
                            if q.option_count == 4
                            and q.correct_count == 1
                        ]

                    questions_by_type[question_type] = candidates

                    if len(candidates) < required_count:
                        messages.error(
                            request,
                            f"{question_type.upper()} questions insufficient. "
                            f"Required: {required_count}, Available: {len(candidates)}."
                        )
                        break

                else:
                    selected_questions = []

                    for question_type, required_count in pattern.items():
                        selected_questions.extend(
                            random.sample(
                                questions_by_type[question_type],
                                required_count
                            )
                        )

                    random.shuffle(selected_questions)

                    now = timezone.now()

                    with transaction.atomic():
                        paper = GeneratedPaper.objects.create(
                            student=request.user,
                            exam=exam,
                            selected_question_ids=[
                                q.id for q in selected_questions
                            ],
                            started_at=now,
                            expires_at=now + timedelta(
                                minutes=exam.duration_minutes
                            ),
                        )

                    return redirect(
                        "examination:take_paper",
                        paper_id=paper.id
                    )

    return render(
        request,
        "examination/question_papers.html",
        {
            "assigned_class": assigned_class,
            "subjects": subjects,
            "selected_subject": selected_subject,
            "selected_marks": selected_marks,
        }
    )



def evaluate_written_answer(question, student_answer):
    if not student_answer.strip():
        return Decimal("0.00")

    if not settings.GROQ_API_KEY:
        raise ValueError("Groq API key is not configured.")

    answer_key = question.answer_key

    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = f"""
You are an examiner evaluating a college examination answer.

Question:
{question.question_text}

Maximum Marks:
{question.marks}

Model Answer:
{answer_key.model_answer}

Marking Rubric:
{answer_key.marking_rubric}

Important Keywords:
{answer_key.important_keywords}

Student Answer:
{student_answer}

Evaluate fairly.
Award marks only according to correctness and relevance.
Do not award marks just for answer length.

Return ONLY valid JSON in this format:
{{
    "marks": 0,
    "feedback": "Brief feedback"
}}

Marks must be between 0 and {question.marks}.
"""

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a strict and fair academic examiner."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )

    result = json.loads(
        response.choices[0].message.content
    )

    marks = Decimal(str(result["marks"]))

    if not marks.is_finite():
        raise ValueError("Invalid AI marks.")

    marks = max(Decimal("0"), min(marks, Decimal(question.marks)))

    return marks.quantize(Decimal("0.01"))




@login_required
def take_paper(request, paper_id):

    paper = get_object_or_404(
        GeneratedPaper.objects.select_related("exam", "exam__subject"),
        id=paper_id,
        student=request.user
    )

    # Already submitted paper: show existing result
    if paper.status != "in_progress":
        result = ExamResult.objects.filter(
            generated_paper=paper
        ).first()

        if result:
            return redirect(
                "examination:result_detail",
                result_id=result.id
            )

        messages.info(request, "This paper is already closed.")
        return redirect("examination:question_papers")

    now = timezone.now()

    questions = list(
        Question.objects.filter(
            id__in=paper.selected_question_ids,
            subject=paper.exam.subject
        ).prefetch_related("options")
    )

    question_map = {q.id: q for q in questions}

    ordered_questions = [
        question_map[qid]
        for qid in paper.selected_question_ids
        if qid in question_map
    ]

    if len(ordered_questions) != len(paper.selected_question_ids):
        messages.error(request, "Paper questions could not be loaded.")
        return redirect("examination:question_papers")

    if request.method == "POST":

        try:
            with transaction.atomic():

                # Lock paper to prevent simultaneous duplicate submissions
                paper = (
                    GeneratedPaper.objects
                    .select_for_update()
                    .select_related("exam", "exam__subject")
                    .get(id=paper_id, student=request.user)
                )

                # Check status again after acquiring lock
                if paper.status != "in_progress":
                    result = ExamResult.objects.filter(
                        generated_paper=paper
                    ).first()

                    if result:
                        return redirect(
                            "examination:result_detail",
                            result_id=result.id
                        )

                    return redirect("examination:question_papers")

                total_score = Decimal("0.00")

                for question in ordered_questions:

                    answer = request.POST.get(
                        f"answer_{question.id}", ""
                    ).strip()

                    if question.question_type == "mcq":

                        if answer:
                            correct = MCQOption.objects.filter(
                                id=answer,
                                question=question,
                                is_correct=True
                            ).exists()

                            if correct:
                                total_score += Decimal("1.00")

                    else:
                        marks = evaluate_written_answer(
                            question,
                            answer
                        )

                        total_score += marks

                total_score = min(
                    total_score,
                    Decimal(paper.exam.total_marks)
                )

                submitted_time = timezone.now()

                paper.status = (
                    "expired"
                    if submitted_time >= paper.expires_at
                    else "submitted"
                )

                paper.submitted_at = submitted_time

                paper.save(
                    update_fields=["status", "submitted_at"]
                )

                result = ExamResult.objects.create(
                    generated_paper=paper,
                    marks_obtained=total_score,
                    status="pending"
                )

            # Redirect only after transaction succeeds
            return redirect(
                "examination:result_detail",
                result_id=result.id
            )

        except Exception as e:
            import traceback

            print("\n========== EXAM SUBMISSION ERROR ==========")
            print(type(e).__name__, str(e))
            traceback.print_exc()
            print("===========================================\n")

            messages.error(
                request,
                "Submission failed. Please try again."
            )

            remaining_seconds = max(
                0,
                int((paper.expires_at - timezone.now()).total_seconds())
            )

            return render(
                request,
                "examination/take_paper.html",
                {
                    "paper": paper,
                    "questions": ordered_questions,
                    "remaining_seconds": remaining_seconds,
                }
            )

    # GET request: check expiry
    if now >= paper.expires_at:

        paper.status = "expired"
        paper.submitted_at = now

        paper.save(
            update_fields=["status", "submitted_at"]
        )

        messages.warning(request, "Exam time is over.")
        return redirect("examination:question_papers")

    remaining_seconds = max(
        0,
        int((paper.expires_at - now).total_seconds())
    )

    return render(
        request,
        "examination/take_paper.html",
        {
            "paper": paper,
            "questions": ordered_questions,
            "remaining_seconds": remaining_seconds,
        }
    )


@login_required
def result_detail(request, result_id):

    result = get_object_or_404(
        ExamResult.objects.select_related(
            "generated_paper",
            "generated_paper__exam",
            "generated_paper__exam__subject",
        ),
        id=result_id,
        generated_paper__student=request.user
    )

    exam = result.generated_paper.exam

    percentage = (
        float(result.marks_obtained) / exam.total_marks * 100
        if exam.total_marks else 0
    )

    return render(
        request,
        "examination/result_detail.html",
        {
            "result": result,
            "exam": exam,
            "percentage": round(percentage, 2),
        }
    )
    
    
@login_required
def my_results(request):

    results = (
        ExamResult.objects
        .filter(generated_paper__student=request.user)
        .select_related(
            "generated_paper",
            "generated_paper__exam",
            "generated_paper__exam__subject"
        )
        .order_by("-submitted_at")
    )

    total_exams = results.count()

    approved_count = results.filter(
        status="approved"
    ).count()

    pending_count = results.filter(
        status="pending"
    ).count()

    rejected_count = results.filter(
        status="rejected"
    ).count()

    return render(
        request,
        "examination/my_results.html",
        {
            "results": results,
            "total_exams": total_exams,
            "approved_count": approved_count,
            "pending_count": pending_count,
            "rejected_count": rejected_count,
        }
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import ClassAccess, Subject, ExamResult


@login_required
def class_ranking(request):

    # 1. Get student's assigned class
    class_access = (
        ClassAccess.objects
        .select_related("academic_class")
        .filter(
            student=request.user,
            academic_class__is_active=True
        )
        .first()
    )

    if not class_access:
        return redirect("examination:class_dashboard")

    assigned_class = class_access.academic_class

    # 2. Get active subjects
    subjects = Subject.objects.filter(
        academic_class=assigned_class,
        is_active=True
    ).order_by("name")

    # 3. Read ranking filter
    ranking_type = request.GET.get("type", "overall")
    subject_id = request.GET.get("subject", "")

    selected_subject = None

    if ranking_type == "subject" and subject_id:
        selected_subject = subjects.filter(
            id=subject_id
        ).first()

    if ranking_type == "subject" and not selected_subject:
        ranking_type = "overall"

    # 4. Get all students assigned to this class
    student_ids = list(
        ClassAccess.objects.filter(
            academic_class=assigned_class
        ).values_list("student_id", flat=True)
    )

    # 5. Get approved results only
    all_results = (
        ExamResult.objects.filter(
            generated_paper__student_id__in=student_ids,
            generated_paper__exam__subject__academic_class=assigned_class
        ).select_related(
            "generated_paper__student",
            "generated_paper__exam__subject"
        )
    )

    if ranking_type == "subject":
        all_results = all_results.filter(
            generated_paper__exam__subject=selected_subject
        )

    # 6. Calculate each student's best percentage
    student_subject_best = {}

    for result in all_results:

        student = result.generated_paper.student
        subject = result.generated_paper.exam.subject

        total_marks = result.generated_paper.exam.total_marks

        if total_marks <= 0:
            continue

        percentage = (
            float(result.marks_obtained) / total_marks
        ) * 100

        key = (student.id, subject.id)

        if (
            key not in student_subject_best
            or percentage > student_subject_best[key]
        ):
            student_subject_best[key] = percentage

    # 7. Prepare student ranking scores
    student_scores = {}

    for (student_id, subject_id), percentage in student_subject_best.items():

        if student_id not in student_scores:
            student_scores[student_id] = {
                "student_id": student_id,
                "subject_percentages": []
            }

        student_scores[student_id]["subject_percentages"].append(
            percentage
        )

    ranking_data = []

    for student_id, data in student_scores.items():

        percentages = data["subject_percentages"]

        if not percentages:
            continue

        if ranking_type == "subject":
            final_percentage = percentages[0]
        else:
            final_percentage = sum(percentages) / len(percentages)

        ranking_data.append({
            "student_id": student_id,
            "percentage": round(final_percentage, 2)
        })

    # 8. Sort highest percentage first
    ranking_data.sort(
        key=lambda item: (
            -item["percentage"],
            item["student_id"]
        )
    )

    # 9. Add rank with equal marks receiving equal rank
    previous_percentage = None
    current_rank = 0

    for index, item in enumerate(ranking_data, start=1):

        if item["percentage"] != previous_percentage:
            current_rank = index

        item["rank"] = current_rank
        previous_percentage = item["percentage"]

    # 10. Get student objects
    from django.contrib.auth import get_user_model

    User = get_user_model()

    ranked_student_ids = [
        item["student_id"] for item in ranking_data[:50]
    ]

    students = User.objects.in_bulk(ranked_student_ids)

    for item in ranking_data:
        student = students.get(item["student_id"])

        item["student"] = student

        if student:
            item["student_name"] = (
                student.get_full_name().strip()
                or getattr(student, "name", "")
                or getattr(student, "full_name", "")
                or getattr(student, "display_name", "")
                or "Student"
            ) if student else "Student"
        else:
            item["student_name"] = "Student"

    # 11. Top 3 and Top 50
    top_three = ranking_data[:3]
    top_fifty = ranking_data[:50]

    context = {
        "assigned_class": assigned_class,
        "subjects": subjects,
        "ranking_type": ranking_type,
        "selected_subject": selected_subject,
        "top_three": top_three,
        "top_fifty": top_fifty,
        "total_ranked_students": len(ranking_data),
    }

    return render(
        request,
        "examination/class_ranking.html",
        context
    )

