from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    rating = models.IntegerField(default=0, blank=True)
    gamertag = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/')
    favorite_games = models.TextField(max_length=140, blank=True)
    current_interests = models.TextField(max_length=200, blank=True)
    followers = models.ManyToManyField(User, related_name="followers", blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()

    def __str__(self):
        return self.user.username

class Tournament(models.Model):
    tournament_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    start_day = models.CharField(max_length=10)
    start_time = models.CharField(max_length=7)
    game = models.CharField(max_length=40)
    tournament_type = models.CharField(max_length=40)
    size = models.IntegerField(default=0)
    description = models.TextField(max_length=200)
    players = models.ManyToManyField(User, related_name="players")

    def __str__(self):
	return self.name

class Message(models.Model):
    subject = models.CharField(max_length=40)
    sender = models.ForeignKey(User, related_name="sender")
    receiver = models.ForeignKey(User, related_name="receiver")
    msg_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class SocialMedia(models.Model):
    story = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.story
