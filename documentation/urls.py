
from django.urls import path
from . import views

urlpatterns = [

    # Documentation Home
    path(
        "documentation/",
        views.home,
        name="documentation_home"
    ),

    # Python Documentation
    path(
        "documentation/python/",
        views.python_index,
        name="python_index"
    ),

    path(
        "documentation/python/<str:topic>/",
        views.python_topic,
        name="python_topic"
    ),

    # HTML Documentation
    path(
        "documentation/html/",
        views.html_index,
        name="html_index"
    ),

    path(
        "documentation/html/<str:topic>/",
        views.html_topic,
        name="html_topic"
    ),

    # CSS Documentation
    path(
        "documentation/css/",
        views.css_index,
        name="css_index"
    ),

    path(
        "documentation/css/<str:topic>/",
        views.css_topic,
        name="css_topic"
    ),
    
    path(
        "documentation/javascript/",
        views.javascript_index,
        name="javascript_index"
    ),

    path(
        "documentation/javascript/<str:topic>/",
        views.javascript_topic,
        name="javascript_topic"
    ),
    
    # Django Documentation
    path(
        "documentation/django/",
        views.django_index,
        name="django_index"
    ),

    path(
        "documentation/django/<str:topic>/",
        views.django_topic,
        name="django_topic"
    ),

]
