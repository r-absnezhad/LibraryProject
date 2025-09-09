from django.urls import path, include
from . import views
app_name = "api-v1-accounts"
urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view() ,name='registration'),
    # change pass
    # reset pass
    # login token
    # login jwt
]