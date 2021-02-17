from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import Context

# Create your views here.


@login_required
def chatRoom(request):
    return render(request, "chat/chatRoom.html", {"username": str(request.user)})
