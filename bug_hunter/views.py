
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction

from .models import Question, GameSession, PlayerStats

from datetime import timedelta

from django.utils import timezone

from django.db.models import Q


# GAME DASHBOARD
@login_required
def game_dashboard(request):

    stats, created = PlayerStats.objects.get_or_create(
        user=request.user
    )

    context = {
        "stats": stats,
        "recent_games": GameSession.objects.filter(
            user=request.user,
            status="completed"
        ).order_by("-completed_at")[:5],
    }

    return render(
        request,
        "bug_hunter/dashboard.html",
        context
    )


# START GAME
@login_required
def start_game(request):

    if request.method != "POST":
        return redirect("bug_hunter:dashboard")

    mode = request.POST.get("mode")
    language_input = request.POST.get("language", "all")
    difficulty = request.POST.get("difficulty", "all")

    questions = Question.objects.filter(is_published=True)

    # LANGUAGE TEST
    if mode == "language":

        valid_languages = dict(Question.LANGUAGE_CHOICES)

        if language_input not in valid_languages:
            messages.error(request, "Invalid language selected.")
            return redirect("bug_hunter:dashboard")

        language = language_input
        questions = questions.filter(language=language)

    # MIXED TEST
    elif mode == "mixed":

        language = "mixed"

    # PRACTICE TEST
    elif mode == "practice":

        if language_input == "all":
            language = "all"
        else:
            valid_languages = dict(Question.LANGUAGE_CHOICES)

            if language_input not in valid_languages:
                messages.error(request, "Invalid language selected.")
                return redirect("bug_hunter:dashboard")

            language = language_input
            questions = questions.filter(language=language)

    else:
        messages.error(request, "Invalid game mode.")
        return redirect("bug_hunter:dashboard")

    # DIFFICULTY FILTER
    valid_difficulties = dict(Question.DIFFICULTY_CHOICES)

    if difficulty != "all":

        if difficulty not in valid_difficulties:
            messages.error(request, "Invalid difficulty selected.")
            return redirect("bug_hunter:dashboard")

        questions = questions.filter(difficulty=difficulty)

    # RANDOM QUESTION SELECTION
    selected_questions = list(
        questions.order_by("?")[:10]
    )

    if len(selected_questions) < 10:
        messages.error(
            request,
            "Not enough published questions. Please try another category."
        )
        return redirect("bug_hunter:dashboard")

    # CREATE GAME SESSION
    game = GameSession.objects.create(
        user=request.user,
        language=language,
        difficulty=difficulty,
        total_questions=10,
    )

    # TEMPORARY QUESTION IDS
    request.session[f"bug_hunter_game_{game.id}"] = [
        question.id for question in selected_questions
    ]

    request.session.modified = True

    return redirect(
        "bug_hunter:play_game",
        session_id=game.id
    )


# PLAY GAME
@login_required
def play_game(request, session_id):

    game = get_object_or_404(
        GameSession,
        id=session_id,
        user=request.user
    )

    if game.status == "completed":
        return redirect(
            "bug_hunter:game_result",
            session_id=game.id
        )

    question_ids = request.session.get(
        f"bug_hunter_game_{game.id}"
    )

    if not question_ids:
        messages.error(
            request,
            "Game session expired. Please start a new game."
        )
        return redirect("bug_hunter:dashboard")

    question_map = {
        question.id: question
        for question in Question.objects.filter(
            id__in=question_ids,
            is_published=True
        )
    }

    if len(question_map) != 10:
        messages.error(
            request,
            "Some questions are no longer available. Start a new game."
        )
        return redirect("bug_hunter:dashboard")

    selected_questions = [
        question_map[qid] for qid in question_ids
    ]

    context = {
        "game": game,
        "questions": selected_questions,
        "game_duration": 600,
        "game_started_at_ms": int(
            game.started_at.timestamp() * 1000
        ) if game.started_at else int(
            timezone.now().timestamp() * 1000
        ),
    }

    return render(
        request,
        "bug_hunter/play_game.html",
        context
    )


# SUBMIT GAME
@login_required
@transaction.atomic
def submit_game(request, session_id):

    if request.method != "POST":
        return redirect("bug_hunter:dashboard")

    game = get_object_or_404(
        GameSession.objects.select_for_update(),
        id=session_id,
        user=request.user
    )

    if game.status == "completed":
        return redirect(
            "bug_hunter:game_result",
            session_id=game.id
        )

    question_ids = request.session.get(
        f"bug_hunter_game_{game.id}"
    )

    if not question_ids or len(question_ids) != 10:
        messages.error(
            request,
            "Game session expired. Please start again."
        )
        return redirect("bug_hunter:dashboard")

    question_map = {
        question.id: question
        for question in Question.objects.filter(
            id__in=question_ids,
            is_published=True
        )
    }

    if len(question_map) != 10:
        messages.error(request, "Questions are unavailable.")
        return redirect("bug_hunter:dashboard")

    correct_count = 0
    wrong_count = 0
    unanswered_count = 0
    points_earned = 0

    for question_id in question_ids:

        question = question_map[question_id]

        selected_option = request.POST.get(
            f"question_{question_id}", ""
        )

        if selected_option not in ["A", "B", "C", "D"]:
            unanswered_count += 1
            continue

        if selected_option == question.correct_option:

            correct_count += 1
            points_earned += 10

        else:

            wrong_count += 1
            points_earned -= 5

    # SAVE ONLY GAME SUMMARY
    game.correct_count = correct_count
    game.wrong_count = wrong_count
    game.unanswered_count = unanswered_count
    game.points_earned = points_earned
    game.status = "completed"
    game.completed_at = timezone.now()

    game.save()

    # UPDATE PLAYER XP
    stats, created = PlayerStats.objects.get_or_create(
        user=request.user
    )

    stats.total_xp += points_earned
    stats.games_played += 1
    stats.correct_answers += correct_count
    stats.questions_answered += (
        correct_count + wrong_count
    )

    stats.save()

    # DELETE TEMPORARY QUESTION IDS
    request.session.pop(
        f"bug_hunter_game_{game.id}",
        None
    )

    request.session.modified = True

    return redirect(
        "bug_hunter:game_result",
        session_id=game.id
    )


# GAME RESULT
@login_required
def game_result(request, session_id):

    game = get_object_or_404(
        GameSession,
        id=session_id,
        user=request.user,
        status="completed"
    )

    stats, created = PlayerStats.objects.get_or_create(
        user=request.user
    )

    accuracy = 0

    if game.total_questions:
        accuracy = round(
            game.correct_count / game.total_questions * 100,
            2
        )

    context = {
        "game": game,
        "stats": stats,
        "accuracy": accuracy,
    }

    return render(
        request,
        "bug_hunter/result.html",
        context
    )


from django.db.models import Q


# GLOBAL LEADERBOARD
@login_required
def leaderboard(request):

    # Current player's stats
    current_stats, created = PlayerStats.objects.get_or_create(
        user=request.user
    )

    # Calculate global rank
    players_above = PlayerStats.objects.filter(
        Q(total_xp__gt=current_stats.total_xp) |
        Q(
            total_xp=current_stats.total_xp,
            correct_answers__gt=current_stats.correct_answers
        ) |
        Q(
            total_xp=current_stats.total_xp,
            correct_answers=current_stats.correct_answers,
            id__lt=current_stats.id
        )
    ).count()

    current_rank = players_above + 1

    # Top 50 players
    players = PlayerStats.objects.select_related(
        "user"
    ).order_by(
        "-total_xp",
        "-correct_answers",
        "id"
    )[:50]

    context = {
        "players": players,
        "current_stats": current_stats,
        "current_rank": current_rank,
    }

    return render(
        request,
        "bug_hunter/leaderboard.html",
        context
    )