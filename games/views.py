from django.shortcuts import (
    render, HttpResponse
)

# Create your views here.
def rps(request):
    return render(request, 'games/rps.html', {})