from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse

# Create your views here.


def register(request):
    if request.method == "GET":
        return render(request, "registration/register.html", {"form": UserCreationForm})
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("chatRoom"))
        else:
            return render(request, "registration/register.html", {"form": UserCreationForm})


def landing(request):
    if request.method == "GET":
        return render(request, "registration/landing.html")
