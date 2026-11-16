
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
        "get_user_name",
        "language",
        "difficulty",
        "correct_count",
        "wrong_count",
        "points_earned",
        "status",
        "started_at",
    )

    list_filter = ("language", "difficulty", "status")

    search_fields = (
        "user__name",
        "user__mobile_number",
    )

    @admin.display(description="Player Name")
    def get_user_name(self, obj):
        return obj.user.name


@admin.register(GameAnswer)
class GameAnswerAdmin(admin.ModelAdmin):

    list_display = (
        "get_user_name",
        "session",
        "question",
        "selected_option",
        "is_correct",
        "points_awarded",
    )

    list_filter = ("is_correct",)

    @admin.display(description="Player Name")
    def get_user_name(self, obj):
        return obj.session.user.name


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):

    list_display = (
        "get_user_name",
        "total_xp",
        "games_played",
        "correct_answers",
        "questions_answered",
        "updated_at",
    )

    search_fields = (
        "user__name",
        "user__mobile_number",
    )

    ordering = ("-total_xp",)

    @admin.display(description="Player Name")
    def get_user_name(self, obj):
        return obj.user.name
