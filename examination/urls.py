
from django.urls import path
from . import views
from . import mcq_views

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
]
