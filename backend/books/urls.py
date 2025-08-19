from django.urls import path, include


urlpatterns = [
    path("api/v1/", include("books.api.v1.urls")),
]