from django.urls import path, include

app_name = "api-v1-accounts"
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]