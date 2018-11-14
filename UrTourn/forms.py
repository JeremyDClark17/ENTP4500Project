from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from UrTourn.models import Profile, Tournament, SocialMedia
from django.utils import timezone

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "20"}), required=False)
    location = forms.CharField(max_length=30, required=False)
    gamertag = forms.CharField(max_length=20, required=False)
    birth_date = forms.DateField(required=False)
    profile_image = forms.ImageField(required=False)
    favorite_games = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "8"}), required=False)
    current_interests = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "10"}), required=False)

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'gamertag', 'birth_date', 'profile_image', 'favorite_games', 'current_interests')

class TournamentForm(forms.ModelForm):
    name = forms.CharField(max_length=40, required=True)
    start_day = forms.CharField(max_length=10, help_text='MM/DD/YYYY', required=True)
    start_time = forms.CharField(max_length=7, help_text='HH:MM(am/pm)', required=True)
    game = forms.CharField(max_length=40, required=True)
    tournament_type = forms.CharField(max_length=40, required=True)
    size = forms.IntegerField(required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "20"}), required=True)

    class Meta:
	model = Tournament
	fields = ('name', 'start_day', 'start_time', 'game', 'tournament_type', 'size', 'description')

class SocialMediaForm(forms.ModelForm):
    story = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "80", 'rows': "20"}), required=False)
    
    class Meta:
	model = SocialMedia
	fields = ('story',)
