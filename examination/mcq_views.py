import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import ClassAccess, Subject, Question


# ==================================================
# MCQ TEST SETTINGS
# ==================================================

MCQ_TEST_QUESTIONS = 10   # kiti MCQ prashna ek test madhe
MCQ_TEST_MINUTES = 10     # test chi vel (minutes)
SESSION_KEY = "mcq_test_state"


def _verify_class_access(user, class_id):
    """Student la hi class assigned ahe ka te tapasa."""
    return get_object_or_404(
        ClassAccess.objects.select_related("academic_class"),
        student=user,
        academic_class_id=class_id,
        academic_class__is_active=True,
    )


# ==================================================
# 1. MCQ TEST PAGE: subject nivda
# ==================================================

@login_required
def mcq_test(request):
    class_id = request.GET.get("class")

    if not class_id or not class_id.isdigit():
        messages.error(request, "Please select your class.")
        return redirect("examination:class_dashboard")

    class_access = _verify_class_access(request.user, class_id)
    assigned_class = class_access.academic_class

    subjects = Subject.objects.filter(
        academic_class=assigned_class,
        is_active=True,
    ).order_by("name")

    return render(
        request,
        "examination/mcq_test.html",
        {
            "assigned_class": assigned_class,
            "selected_class": assigned_class,
            "subjects": subjects,
            "test_questions": MCQ_TEST_QUESTIONS,
            "test_minutes": MCQ_TEST_MINUTES,
        },
    )


# ==================================================
# 2. START TEST: random MCQ prashna nivda
# ==================================================

@login_required
def mcq_test_start(request):
    if request.method != "POST":
        return redirect("examination:class_dashboard")

    class_id = request.POST.get("class", "")
    subject_id = request.POST.get("subject", "")

    if not class_id.isdigit() or not subject_id.isdigit():
        messages.error(request, "Class ani subject nivda.")
        return redirect("examination:class_dashboard")

    class_access = _verify_class_access(request.user, class_id)
    assigned_class = class_access.academic_class

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        academic_class=assigned_class,
        is_active=True,
    )

    # Fakta barobar 4 options (ya madhe 1 correct) asalele MCQ prashna
    candidates = list(
        Question.objects.filter(
            subject=subject,
            question_type="mcq",
            is_active=True,
        )
        .annotate(
            option_count=Count("options", distinct=True),
            correct_count=Count(
                "options",
                filter=Q(options__is_correct=True),
                distinct=True,
            ),
        )
        .filter(option_count__gte=2, correct_count=1)
    )

    if len(candidates) < MCQ_TEST_QUESTIONS:
        messages.error(
            request,
            f"{subject.name} sathi MCQ prashna kami ahet. "
            f"Required: {MCQ_TEST_QUESTIONS}, Available: {len(candidates)}."
        )
        return redirect(
            f"{reverse('examination:mcq_test')}?class={assigned_class.id}"
        )

    selected = random.sample(candidates, MCQ_TEST_QUESTIONS)

    request.session[SESSION_KEY] = {
        "class_id": assigned_class.id,
        "subject_name": subject.name,
        "question_ids": [q.id for q in selected],
        "started_at": timezone.now().isoformat(),
    }

    return redirect("examination:mcq_test_take")


# ==================================================
# 3. TAKE TEST (GET) ani SUBMIT (POST)
# ==================================================

@login_required
def mcq_test_take(request):
    state = request.session.get(SESSION_KEY)

    if not state:
        messages.error(request, "Test suru nahi jhala. Please punha test nivda.")
        return redirect("examination:class_dashboard")

    class_access = _verify_class_access(request.user, state["class_id"])
    assigned_class = class_access.academic_class

    questions = Question.objects.filter(
        id__in=state["question_ids"]
    ).prefetch_related("options")

    question_map = {q.id: q for q in questions}
    ordered_questions = [
        question_map[qid]
        for qid in state["question_ids"]
        if qid in question_map
    ]

    # ---------- SUBMIT ----------
    if request.method == "POST":
        results = []
        score = 0

        for question in ordered_questions:
            options = list(question.options.all())
            correct = next((o for o in options if o.is_correct), None)

            chosen_raw = request.POST.get(f"q_{question.id}", "")
            chosen = next(
                (o for o in options if str(o.id) == chosen_raw),
                None
            )

            is_right = bool(chosen and correct and chosen.id == correct.id)

            if is_right:
                score += 1

            results.append({
                "question": question,
                "chosen": chosen,
                "correct": correct,
                "is_right": is_right,
            })

        # Test ek vela submit hoto; session madhun state kadhun taka
        del request.session[SESSION_KEY]

        total = len(ordered_questions)
        percentage = round((score / total) * 100, 2) if total else 0

        return render(
            request,
            "examination/mcq_test_result.html",
            {
                "assigned_class": assigned_class,
                "selected_class": assigned_class,
                "subject_name": state["subject_name"],
                "results": results,
                "score": score,
                "total": total,
                "percentage": percentage,
            },
        )

    # ---------- SHOW TEST (GET) ----------
    started_at = parse_datetime(state["started_at"])
    elapsed = (timezone.now() - started_at).total_seconds()
    remaining_seconds = max(0, int(MCQ_TEST_MINUTES * 60 - elapsed))

    return render(
        request,
        "examination/mcq_test_take.html",
        {
            "assigned_class": assigned_class,
            "subject_name": state["subject_name"],
            "questions": ordered_questions,
            "remaining_seconds": remaining_seconds,
        },
    )