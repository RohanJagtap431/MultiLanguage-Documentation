from django.contrib import admin
from django.urls import path, include
from accounts.views import landing_view

urlpatterns = [
    path("", landing_view, name="home"),

    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),
    path("", include("documentation.urls")),
    path("code-detective/", include("bug_hunter.urls")),
    path("examination/", include("examination.urls")),
]