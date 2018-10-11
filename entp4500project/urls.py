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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'UrTourn.views.home', name = 'home'),
    url(r'^login/', 'UrTourn.views.userLogin', name = 'home'),
    url(r'^logout/', 'UrTourn.views.userLogout', name = 'logout'),
    url(r'^signup/', 'UrTourn.views.signup', name = 'signup'),
    url(r'^profile/', 'UrTourn.views.profile', name = 'profile'),
    url(r'^update_profile/', 'UrTourn.views.update_profile', name = 'update'),
]
