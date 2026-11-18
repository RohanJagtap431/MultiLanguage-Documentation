
from django.urls import path
from . import views
from . import mcq_views
from . import duel_views

app_name = "examination"

urlpatterns = [
    path("class/", views.class_dashboard, name="class_dashboard"),

    path("question-papers/", views.question_papers, name="question_papers"),

    path("my-results/", views.my_results, name="my_results"),

    path("ranking/", views.class_ranking, name="class_ranking"),

    path(
        "paper/<int:paper_id>/",
        views.take_paper,
        name="take_paper"
    ),

    path(
        "result/<int:result_id>/",
        views.result_detail,
        name="result_detail"
    ),
    
    path("mcq-test/", mcq_views.mcq_test, name="mcq_test"),
    path("mcq-test/start/", mcq_views.mcq_test_start, name="mcq_test_start"),
    path("mcq-test/take/", mcq_views.mcq_test_take, name="mcq_test_take"),
    
    path("duel/", duel_views.duel_home, name="duel_home"),
    path("duel/create/", duel_views.duel_create, name="duel_create"),
    path("duel/join/", duel_views.duel_join, name="duel_join"),
    path("duel/<str:code>/", duel_views.duel_room, name="duel_room"),
    path("duel/<str:code>/status/", duel_views.duel_status, name="duel_status"),
    path("duel/<str:code>/submit/", duel_views.duel_submit, name="duel_submit"),
    path("duel/<str:code>/delete/", duel_views.duel_delete, name="duel_delete"),
]
