from django.urls import path
from .views import ProcessVideoAPIView
urlpatterns = [
    path('process', ProcessVideoAPIView.as_view()),
]