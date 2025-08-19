from django.urls import path, include
from .views import NotificationModelViewSet
from rest_framework import routers
app_name = 'api_v1_notifications'

router = routers.SimpleRouter()
router.register('notifications', NotificationModelViewSet)
urlpatterns = [
    path('', include(router.urls)),
]