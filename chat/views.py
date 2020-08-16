from django.shortcuts import (
    render, HttpResponse, redirect
)

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'chat/chat.html', {
            'room_name': 'room1'
        })