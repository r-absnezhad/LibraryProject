from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookModelViewSet, GenreModelViewSet

router = DefaultRouter()
router.register('books', BookModelViewSet, basename='book')
router.register('genres', GenreModelViewSet, basename='genre')
urlpatterns = [
    path('', include(router.urls)),
]