from django.urls import path, include
#from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.signup, name="signup"),
    path('', include('django.contrib.auth.urls')),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate')
]
