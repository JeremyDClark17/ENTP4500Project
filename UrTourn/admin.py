from django.contrib import admin
from .models import Profile, Tournament, SocialMedia, Message

# Register your models here.
admin.site.register(Profile)
admin.site.register(Tournament)
admin.site.register(Message)
admin.site.register(SocialMedia)
