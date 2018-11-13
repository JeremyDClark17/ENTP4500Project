"""entp4500project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'UrTourn.views.home', name = 'home'),
    url(r'^login/$', 'UrTourn.views.userLogin', name = 'home'),
    url(r'^logout/$', 'UrTourn.views.userLogout', name = 'logout'),
    url(r'^signup/$', 'UrTourn.views.signup', name = 'signup'),
    url(r'^u/$', 'UrTourn.views.profile', name = 'profile'),
    url(r'^u/(?P<Username>[\w.@+\- ]+)/$', 'UrTourn.views.profiles', name = 'profile'),
    url(r'^u/(?P<Username>[\w.@+\- ]+)/follow/$', 'UrTourn.views.follow', name = 'follow'),
    url(r'^u/(?P<Username>[\w.@+\- ]+)/unfollow/$', 'UrTourn.views.unfollow', name = 'unfollow'),
    url(r'^update_profile/$', 'UrTourn.views.update_profile', name = 'update'),
    url(r'^delete_profile/$', 'UrTourn.views.delete_profile', name = 'delete'),
    url(r'^tournaments/$', 'UrTourn.views.tournaments', name = 'tournaments'),
    url(r'^tournaments/(?P<index>\S{36})/$', 'UrTourn.views.tournament', name = 'tournament'),
    url(r'^tournaments/(?P<index>\S{36})/join$', 'UrTourn.views.join_tournament', name = 'join_tournament'),
    url(r'^tournaments/(?P<index>\S{36})/leave$', 'UrTourn.views.leave_tournament', name = 'leave_tournament'),
    url(r'^tournaments/(?P<index>\S{36})/edit$', 'UrTourn.views.edit_tournament', name = 'edit_tournament'),
    url(r'^tournaments/(?P<index>\S{36})/delete$', 'UrTourn.views.delete_tournament', name = 'delete_tournament'),
    url(r'^create_tournament/$', 'UrTourn.views.create_tournament', name = 'create_tournament'),
    url(r'^players/$', 'UrTourn.views.players', name = 'players'),
    url(r'^messages/$', 'UrTourn.views.messages', name = 'messages'),
    url(r'^messages/(?P<index>\d{1,36})/$', 'UrTourn.views.message', name = 'message'),
    url(r'^create_message/$', 'UrTourn.views.create_message', name = 'create_message'),
    url(r'^reply_message/(?P<index>\d{1,36})/$', 'UrTourn.views.reply_message', name = 'reply_message'),
    url(r'^new_message/(?P<profile>[\w.@+\- ]+)$', 'UrTourn.views.new_message', name = 'new_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
