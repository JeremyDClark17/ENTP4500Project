from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

def home(request):
   return render(request, "home.html")

def profile(request):
   if request.user.is_authenticated():
   	return render(request, "profile.html", {'user' : request.user})
   else:
        return redirect(home)
 
def userLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
	    username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(profile)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form' : form})

def userLogout(request):
    if request.method == "POST":
        logout(request)
        return redirect(home)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(profile)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
