
from django.urls import path
from . import views

app_name = "bug_hunter"

urlpatterns = [
    # Game Dashboard
    path("", views.game_dashboard, name="dashboard"),

    # Start a new game
    path("start/", views.start_game, name="start_game"),

    # Play game
    path("play/<int:session_id>/", views.play_game, name="play_game"),

    # Submit answers
    path("submit/<int:session_id>/", views.submit_game, name="submit_game"),

    # Game result
    path("result/<int:session_id>/", views.game_result, name="game_result"),

    # Leaderboard
    path("leaderboard/", views.leaderboard, name="leaderboard"),
]
