from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm, TournamentForm
from .models import Tournament
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.core import serializers
from django.template import loader

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
                messages.error(request, ('Please correct the error(s) below.'))
        else:
            profile_form = ProfileForm(instance=request.user.profile)
        return render(request, "update_profile.html", {'profile_form' : profile_form})
    else:
        return redirect(home)

def delete_profile(request):
    if request.user.is_authenticated():
        request.user.delete()
    return redirect(home)

def tournament(request, index):
    tournament = Tournament.objects.get(tournament_id=index)
    count = tournament.players.count()
    userStatus = False
    tournamentJoinable = True
    userHost = False
    if request.user in tournament.players.all():
      userStatus = True
    if count == tournament.size:
      tournamentJoinable = False
    if request.user.id == tournament.host.id:
      userHost = True
    template = loader.get_template("tournament.html")
    context = {'tournament' : tournament, 'count' : count, 'userStatus' : userStatus, 'tournamentJoinable' : tournamentJoinable, 'userHost' : userHost}
    return HttpResponse(template.render(context, request))

def tournaments(request):
    tournaments = Tournament.objects.all()
    template = loader.get_template("tournamentsHome.html")
    context = {'tournaments' : tournaments}
    return HttpResponse(template.render(context, request))

def create_tournament(request):
    form = TournamentForm(request.POST)
    if request.method == 'POST':
      if form.is_valid():
        tourney = form.save(commit=False)
        tourney.host = request.user
        tourney.save()
        messages.success(request, ('Your tournament was successfully created!'))
        return redirect(tournaments)
      else:
        messages.error(request, ('Please correct the error(s) below'))
    else:
      return render(request, "create_tournament.html", {'form' : form})

def join_tournament(request, index):
    tourney = Tournament.objects.get(tournament_id=index)
    count = tourney.players.count()
    if count < tourney.size and request.user.is_authenticated():
      tourney.players.add(request.user)
      return redirect(tournament, index)
    else:
      return redirect(userLogin) 

def leave_tournament(request, index):
    tourney = Tournament.objects.get(tournament_id=index)
    count = tourney.players.count()
    if request.user.is_authenticated() and request.user in tourney.players.all():
      tourney.players.remove(request.user)
      return redirect(tournament, index)
    else:
      return  redirect(userLogin)

def delete_tournament(request, index):
    tourney = Tournament.objects.get(tournament_id=index)
    if request.user.is_authenticated() and request.user.id == tourney.host.id:
        tourney.delete()
        return redirect(tournaments)
    else:
        return redirect(userLogin)
