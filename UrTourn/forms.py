from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from UrTourn.models import Profile

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

    class Meta:
        model = Profile
        fields = ('bio', 'location', 'gamertag', 'birth_date', 'profile_image',)
