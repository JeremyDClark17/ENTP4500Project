from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm, TournamentForm, MessageForm, SocialMediaForm
from .models import Tournament, Message, SocialMedia
from .forms import SignUpForm, ProfileForm, TournamentForm, SocialMediaForm
from .models import Tournament, SocialMedia
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.core import serializers
from django.template import loader
from django.shortcuts import get_object_or_404
from django.db.models import Q

def home(request):
   if request.user.is_authenticated():
       newMessages = doesUserHaveNewMessage(request)
   else:
       newMessages = False
   return render(request, "homepage.html", {'request' : request, 'newMessages' : newMessages})
 
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

def profiles(request, Username):
    try:
        template = loader.get_template("profilev2.html")
        user = User.objects.get(username=Username)
        currentUser = request.user
        followers = user.followers
        following = False
        #if user is on another profile and if they are following that person, mark True
        if currentUser != user and currentUser in user.profile.followers.all():
          following = True
        newMessages = doesUserHaveNewMessage(request)
        context = {'user' : user, 'currentUser' : currentUser, 'followers' : followers, 'following' : following, 'newMessages' : newMessages}
        return HttpResponse(template.render(context, request))
    except User.DoesNotExist:
        return redirect(signup)

def profile(request):
    if request.user.is_authenticated():
        return redirect('/u/%s' % request.user.username )
    else:
        return redirect(home)

def follow(request, Username):
    try:
        user = User.objects.get(username=Username)
        currentUser = request.user
        #Logged in and not following user
        if request.user.is_authenticated() and currentUser not in user.profile.followers.all():
            user.profile.followers.add(request.user)
            return redirect(profiles, user.username) 
        else:
            return redirect(userLogin)
    except User.DoesNotExist:
        return redirect(signup)

def unfollow(request, Username):
    try:
        user = User.objects.get(username=Username)
        currentUser = request.user
        #Logged in and following user
        if request.user.is_authenticated() and currentUser in user.profile.followers.all():
            user.profile.followers.remove(request.user)
            return redirect(profiles, user.username)
        else:
            return redirect(userLogin)
    except User.DoesNotExist:
        return redirect(signup)

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

def social_media(request):
    template_name = 'social_media.html'
    """form = SocialMediaForm(request.POST, request.FILES, instance = request.user.profile)"""
            
    
    if request.user.is_authenticated():
        if request.method == 'POST':
            """if form.is_valid():
                story = form.save(commit=False)
                story.user = request.user
                story.save()
                
                text=form.cleaned_data['story']
                return redirect(social_media)
            
            args = {'form':form, 'text':text}
            return render(request, template_name, args)
            
        else:
            form = SocialMediaForm(request.POST, request.FILES, instance = request.user.profile)
            stories = SocialMedia.objects.all()
            return render(request, template_name, {'form':form})
            """
            social_media_form = SocialMediaForm(request.POST)
    	    if social_media_form.is_valid():
        		story = social_media_form.save(commit=False)
        		story.user = request.user
        		story.save()
        		stories = SocialMedia.objects.all().order_by('-created')
        		"""text = social_media_form.cleaned_data['story']"""
          		social_media_form = SocialMediaForm(instance = request.user)
        		return render(request, "social_media.html", {'social_media_form':social_media_form, 'stories': stories})
            else:
                return render(request, "social_media.html", {'social_media_form':social_media_form, 'stories': stories})
        else:
            stories = SocialMedia.objects.all().order_by('-created')
            social_media_form = SocialMediaForm(instance = request.user)
            args = {'social_media_form': social_media_form, 'stories': stories, 'user' : request.user}
        
	    
            return render(request, "social_media.html", args)
    else:
        return redirect(social_media)	
    

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
    newMessages = doesUserHaveNewMessage(request)
    context = {'tournament' : tournament, 'count' : count, 'userStatus' : userStatus, 'tournamentJoinable' : tournamentJoinable, 'userHost' : userHost, 'user' : request.user, 'newMessages' : newMessages}
    return HttpResponse(template.render(context, request))

def tournaments(request):
    tournaments = Tournament.objects.all()
    query = request.GET.get("q")
    if query:
        tournaments = tournaments.filter(
            Q(name__icontains=query)|
            Q(game__icontains=query)|
            Q(tournament_type__icontains=query)|
            Q(host__username__icontains=query))
    template = loader.get_template("tournamentsHome.html")
    newMessages = doesUserHaveNewMessage(request)
    context = {'tournaments' : tournaments, 'user' : request.user, 'newMessages' : newMessages}
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
        return render(request, "create_tournament.html", {'form' : form})
    else:
      return render(request, "create_tournament.html", {'form' : form})

def edit_tournament(request, index):
    tournament = Tournament.objects.get(tournament_id=index)
    if request.user.is_authenticated():
        if request.method == 'POST':
            tournament_form = TournamentForm(request.POST, request.FILES, instance=tournament)
            if tournament_form.is_valid():
                tournament_form.save()
                messages.success(request, ('Your tournament was successfully updated!'))
                return redirect(tournaments)
            else:
                messages.error(request, ('Please correct the error(s) below.'))
        else:
            tournament_form = TournamentForm(instance=tournament)
        return render(request, "edit_tournament.html", {'form' : tournament_form})
    else:
        return redirect(home)

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
      return redirect(userLogin)

def delete_tournament(request, index):
    tourney = Tournament.objects.get(tournament_id=index)
    if request.user.is_authenticated() and request.user.id == tourney.host.id:
        tourney.delete()
        return redirect(tournaments)
    else:
        return redirect(userLogin)

def players(request):
    players = User.objects.all()
    query = request.GET.get("q")
    if query:
        players = User.objects.filter(
                Q(username__icontains=query)|
                Q(profile__gamertag__icontains=query)|
                Q(profile__favorite_games__icontains=query))
    template = loader.get_template("players.html")
    newMessages = doesUserHaveNewMessage(request)
    context = {'players' : players, 'user' : request.user, 'newMessages' : newMessages}
    return HttpResponse(template.render(context, request))

def messages(request):
    messages = Message.objects.all()
    inboxCount = messages.filter(receiver = request.user).count()
    sentCount = messages.filter(sender = request.user).count()
    query = request.GET.get("q")
    if query:
        if query == "inbox":
            messages = messages.filter(receiver = request.user).order_by('-created_at')
        elif query == "sent":
            messages = messages.filter(sender = request.user).order_by('-created_at')
        else:
            messages = messages.filter(
                Q(sender__username__icontains=query)|
                Q(receiver__username__icontains=query)|
                Q(msg_content__icontains=query)).order_by('-created_at')
    else:
        messages = messages.filter(receiver = request.user)
    template = loader.get_template("messages.html")
    context = {'messages' : messages, 'user' : request.user, 'inboxCount' : inboxCount, 'sentCount' : sentCount}
    return HttpResponse(template.render(context, request))

def message(request, index):
    messages = Message.objects.all()
    message = Message.objects.get(id=index)
    message.read = True
    message.save()
    template = loader.get_template("message.html")
    inboxCount = messages.filter(receiver = request.user).count()
    sentCount = messages.filter(sender = request.user).count()
    context = {'message' : message, 'user' : request.user, 'inboxCount' : inboxCount, 'sentCount' : sentCount}
    return HttpResponse(template.render(context, request))

def doesUserHaveNewMessage(request):
    try:
        if Message.objects.filter(read=False).count() > 0:
            return True
        else:
            return False
    except Message.DoesNotExist:
        return False

def create_message(request):
    form = MessageForm(request.POST)
    if request.method == 'POST':
      if form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.msg_content = form.cleaned_data['message']
        try:
            message.receiver = User.objects.get(username = form.cleaned_data['to'])
            message.save()
            return redirect(messages)
        except User.DoesNotExist:
            return render(request, "create_message.html", {'form' : form})
      else:
        return render(request, "create_message.html", {'form' : form})
    else:
      return render(request, "create_message.html", {'form' : form})

def reply_message(request, index):
    message = Message.objects.get(id=index)
    form = MessageForm(initial={'to': message.sender.username, 'subject': 'RE: ' + message.subject})
    if request.method == 'POST':
      if form.is_valid():
        newMessage = form.save(commit=False)
        newMessage.sender = request.user
        newMessage.msg_content = form.cleaned_data['message']
        try:
            newMessage.receiver = User.objects.get(username = form.cleaned_data['to'])
            newMessage.save()
            return redirect(messages)
        except User.DoesNotExist:
            return render(request, "create_message.html", {'form' : form})
      else:
        return render(request, "create_message.html", {'form' : form})
    else:
      return render(request, "create_message.html", {'form' : form})

def new_message(request, profile):
    form = MessageForm({'to': profile})
    if request.method == 'POST':
      if form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.msg_content = form.cleaned_data['message']
        try:
            message.receiver = User.objects.get(username = form.cleaned_data['to'])
            message.save()
            return redirect(messages)
        except User.DoesNotExist:
            return render(request, "create_message.html", {'form' : form})
      else:
        return render(request, "create_message.html", {'form' : form})
    else:
      return render(request, "create_message.html", {'form' : form})
      

