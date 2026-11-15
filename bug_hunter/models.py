
from django.db import models
from django.conf import settings


class Question(models.Model):

    LANGUAGE_CHOICES = [
        ("python", "Python"),
        ("html", "HTML"),
        ("css", "CSS"),
        ("javascript", "JavaScript"),
        ("django", "Django"),
        ("drf", "Django REST Framework"),
    ]

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    OPTION_CHOICES = [
        ("A", "Option A"),
        ("B", "Option B"),
        ("C", "Option C"),
        ("D", "Option D"),
    ]

    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES
    )

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )

    title = models.CharField(max_length=200)

    question_text = models.TextField()

    buggy_code = models.TextField()

    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)

    correct_option = models.CharField(
        max_length=1,
        choices=OPTION_CHOICES
    )

    explanation = models.TextField()

    points = models.PositiveIntegerField(default=10)

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.language})"


class GameSession(models.Model):

    STATUS_CHOICES = [
        ("started", "Started"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bug_hunter_sessions"
    )

    language = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=10)

    total_questions = models.PositiveIntegerField(default=10)
    correct_count = models.PositiveIntegerField(default=0)
    wrong_count = models.PositiveIntegerField(default=0)
    unanswered_count = models.PositiveIntegerField(default=0)

    points_earned = models.IntegerField(default=0)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="started"
    )

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.language} - {self.status}"


class GameAnswer(models.Model):

    session = models.ForeignKey(
        GameSession,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        related_name="game_answers"
    )

    selected_option = models.CharField(
        max_length=1,
        choices=Question.OPTION_CHOICES,
        null=True,
        blank=True
    )

    is_correct = models.BooleanField(default=False)

    points_awarded = models.IntegerField(default=0)

    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "question"],
                name="unique_question_per_session"
            )
        ]

    def __str__(self):
        return f"{self.session.user} - {self.question.title}"


class PlayerStats(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bug_hunter_stats"
    )

    total_xp = models.IntegerField(default=0)

    games_played = models.PositiveIntegerField(default=0)

    correct_answers = models.PositiveIntegerField(default=0)

    questions_answered = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.total_xp} XP"
