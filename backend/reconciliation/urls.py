from django.urls import path

from .views import disagreements


urlpatterns = [
    path(
        "disagreements/",
        disagreements,
        name="disagreements"
    ),
]