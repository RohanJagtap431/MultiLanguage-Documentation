
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# ==================================================
# 1. ACADEMIC CLASS
# ==================================================

class AcademicClass(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Academic Classes"

    def __str__(self):
        return self.name


# ==================================================
# 2. SUBJECT
# ==================================================

class Subject(models.Model):
    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    name = models.CharField(max_length=150)
    subject_code = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("academic_class", "name")

    def __str__(self):
        return f"{self.academic_class.name} - {self.name}"


# ==================================================
# 3. STUDENT CLASS ACCESS
# ==================================================

class ClassAccess(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="examination_classes"
    )
    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE,
        related_name="student_access"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "academic_class")

    def __str__(self):
        return f"{self.student} - {self.academic_class}"


# ==================================================
# 4. TOPIC
# ==================================================

class Topic(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="topics"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.subject.name} - {self.name}"


# ==================================================
# 5. STUDY NOTES
# ==================================================

class StudyNote(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="notes"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    attachment = models.FileField(
        upload_to="examination/notes/",
        blank=True,
        null=True
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.title


# ==================================================
# 6. QUESTION BANK
# ==================================================

class Question(models.Model):

    QUESTION_TYPES = [
        ("mcq", "Choose the Correct Answer"),
        ("short", "Short Answer Questions"),
        ("long", "Long Answer Questions"),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        related_name="questions",
        blank=True,
        null=True
    )

    question_text = models.TextField()

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES
    )

    marks = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(6)
        ]
    )

    is_active = models.BooleanField(default=True)

    # Temporary migration-friendly default
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def clean(self):
        expected_marks = {
            "mcq": 1,
            "short": 3,
            "long": 6,
        }

        if self.question_type in expected_marks:
            if self.marks != expected_marks[self.question_type]:
                raise ValidationError({
                    "marks": (
                        f"{self.get_question_type_display()} "
                        f"must have {expected_marks[self.question_type]} marks."
                    )
                })

        if self.topic and self.subject_id:
            if self.topic.subject_id != self.subject_id:
                raise ValidationError({
                    "topic": "Topic must belong to the selected subject."
                })

    def __str__(self):
        return f"{self.subject} - {self.marks} Marks"


# ==================================================
# 7. MCQ OPTIONS
# ==================================================

class MCQOption(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options"
    )

    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def clean(self):
        if self.question and self.question.question_type != "mcq":
            raise ValidationError(
                "Options can only be added to MCQ questions."
            )

    def __str__(self):
        return self.option_text


# ==================================================
# 8. ANSWER KEY
# ==================================================

class AnswerKey(models.Model):

    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        related_name="answer_key"
    )

    model_answer = models.TextField()

    marking_rubric = models.TextField(
        help_text="Criteria used by AI and teachers to evaluate answers."
    )

    important_keywords = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer Key - {self.question}"


# ==================================================
# 9. EXAM CONFIGURATION
# ==================================================

class Exam(models.Model):

    EXAM_TYPES = [
        (20, "20 Marks"),
        (30, "30 Marks"),
        (40, "40 Marks"),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="exams"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    total_marks = models.PositiveIntegerField(
        choices=EXAM_TYPES
    )

    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    is_published = models.BooleanField(default=False)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.total_marks} Marks)"


# ==================================================
# 10. GENERATED PAPER
# ==================================================

class GeneratedPaper(models.Model):

    STATUS_CHOICES = [
        ("in_progress", "In Progress"),
        ("submitted", "Submitted"),
        ("expired", "Expired"),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="generated_papers"
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="generated_papers"
    )

    selected_question_ids = models.JSONField(default=list)

    started_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    submitted_at = models.DateTimeField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress"
    )

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.student} - {self.exam.title}"


# ==================================================
# 11. EXAM RESULT
# ==================================================

class ExamResult(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    generated_paper = models.OneToOneField(
        GeneratedPaper,
        on_delete=models.CASCADE,
        related_name="result"
    )

    marks_obtained = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-submitted_at"]

    def clean(self):
        if self.generated_paper_id:
            maximum = self.generated_paper.exam.total_marks

            if self.marks_obtained > maximum:
                raise ValidationError({
                    "marks_obtained": "Marks cannot exceed total marks."
                })

    def __str__(self):
        return f"{self.generated_paper} - Result"

    @property
    def percentage(self):
        if not self.generated_paper_id:
            return 0

        total = self.generated_paper.exam.total_marks

        if total == 0:
            return 0

        return round(
            (float(self.marks_obtained) / total) * 100,
            2
        )
