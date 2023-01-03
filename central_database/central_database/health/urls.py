from django.urls import path

from . import views

app_name = "health"
urlpatterns = [
    path("", views.HealthCheck.as_view(), name="health-check"),
]
