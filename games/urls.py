from django.urls import path
from . import views

urlpatterns = [
    path('rps/', views.rps, name="rps")
]