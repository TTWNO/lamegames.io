from django.urls import path
from . import views

urlpatterns = [
    path('rps/', views.rps, name="rps"),
    path('rps/join', views.rps_join, name="rps/join"),
    path('rps/create', views.rps_create, name="rps/create")
]