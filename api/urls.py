from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='api_upload_video'),
    path('predefined-videos/', views.predefined_videos, name='api_predefined_videos')
]
