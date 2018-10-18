from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

def home(request):
   return render(request, "home.html")
 
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

def profile(request):
   if request.user.is_authenticated():
        return render(request, "profilev2.html", {'user' : request.user})
   else:
        return redirect(home)

def update_profile(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, ('Your profile was successfully updated!'))
                return redirect(profile)
            else:
                messages.error(request, ('Please correct the error below.'))
        else:
            profile_form = ProfileForm(instance=request.user.profile)
        return render(request, "update_profile.html", {'profile_form' : profile_form})
    else:
        return redirect(home)
