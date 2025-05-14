from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('legal', views.legal, name='legal'),
    path('contact', views.contact, name='contact'),
    path('detect/error/', views.detect_video_error, name='detect_video_error'),
    path('detect/<str:video_id>', views.detect_video, name='detect_video'),
]
