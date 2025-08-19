from django.urls import path, include
from .views import LoanModelViewSet
from rest_framework import routers
app_name = 'api_v1_loans'

router = routers.SimpleRouter()
router.register('loans', LoanModelViewSet)
urlpatterns = [
    path('', include(router.urls)),
]