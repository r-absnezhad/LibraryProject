
from django.urls import path, include
from .views import ReviewModelViewSet
from rest_framework import routers
app_name = 'api_v1_reviews'

router = routers.SimpleRouter()
router.register('reviews', ReviewModelViewSet, basename='review')
urlpatterns = [
    path('', include(router.urls)),
]