
from django.contrib import admin
from .models import Question, GameSession, GameAnswer, PlayerStats


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "language",
        "difficulty",
        "points",
        "is_published",
        "created_at",
    )

    list_filter = (
        "language",
        "difficulty",
        "is_published",
    )

    search_fields = (
        "title",
        "question_text",
        "buggy_code",
    )

    list_editable = ("is_published", "points")

    ordering = ("language", "difficulty")


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "language",
        "difficulty",
        "correct_count",
        "wrong_count",
        "points_earned",
        "status",
        "started_at",
    )

    list_filter = ("language", "difficulty", "status")

    search_fields = ("user__username",)


@admin.register(GameAnswer)
class GameAnswerAdmin(admin.ModelAdmin):

    list_display = (
        "session",
        "question",
        "selected_option",
        "is_correct",
        "points_awarded",
    )

    list_filter = ("is_correct",)


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "total_xp",
        "games_played",
        "correct_answers",
        "questions_answered",
        "updated_at",
    )

    search_fields = ("user__username",)

    ordering = ("-total_xp",)
