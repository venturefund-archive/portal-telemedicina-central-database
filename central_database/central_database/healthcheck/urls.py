from django.urls import path

from . import views

app_name = "healthcheck"
urlpatterns = [
    path("", views.Health.as_view()),
]
