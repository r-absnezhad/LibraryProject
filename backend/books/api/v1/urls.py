from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookModelViewSet, GenreModelViewSet, BookRequestModelViewSet

app_name = "api-v1-books"
router = DefaultRouter()
router.register('books', BookModelViewSet, basename='book')
router.register('genres', GenreModelViewSet, basename='genre')
router.register('book_requests', BookRequestModelViewSet, basename='book_request')
urlpatterns = [
    path('', include(router.urls)),
]