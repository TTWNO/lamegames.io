from django.shortcuts import (
    render, HttpResponse
)
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm

from . import forms

# Create your views here.
def index(request):
    return render(request, 'index.html')

class SignUp(generic.CreateView):
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
