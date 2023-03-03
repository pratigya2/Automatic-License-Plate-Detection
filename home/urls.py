from django.urls import path
from . import views

urlpatterns = [
    path('', views.testimonals, name = 'base'),
    path('upload', views.upload, name = 'home'),
    path('result', views.result, name = 'result'),
    
]