from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about', views.about),
    path('legal', views.legal),
    path('contact', views.contact),
]
