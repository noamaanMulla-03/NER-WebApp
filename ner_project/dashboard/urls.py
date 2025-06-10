# Dashboard URLs
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('upload/', views.upload_view, name='upload'),
    path('summary/', views.summary_view, name='summary'),
    path('logout/', LogoutView.as_view(), name='logout')
]