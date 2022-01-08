from django.shortcuts import (
    render, HttpResponse, redirect
)
from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .tokens import account_activation_token
from .forms import LameUserSignupForm
from .models import LameUser


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "signed_in.html", {
          "games": settings.VISIBLE_GAME_LINKS,
        })
    else:
        return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        form = LameUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your lamegames account."
            message = render_to_string("registration/activation_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid":urlsafe_base64_encode(force_bytes(user.pk)),
                "token":account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, "registration/confirm_your_email.html", {})
    else:
        form = LameUserSignupForm()
    return render(request, "registration/signup.html", {"form": form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = LameUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, LameUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect("home")
        return render(request, "registration/account_activated.html")
    else:
        return render(request, "registration/invalid_link.html")

