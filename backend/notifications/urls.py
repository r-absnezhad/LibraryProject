from django.urls import path, include


urlpatterns = [
    path("api/v1/", include("notifications.api.v1.urls")),
]