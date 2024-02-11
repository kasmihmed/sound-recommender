"""
URL configuration for soundrecommender project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from playlists.views import create_playlist
from sounds.views import create_sound

from sounds.views import get_sounds

urlpatterns = [
    # TODO: give a schema of the api and docs
    #path('admin/', admin.site.urls),
    path('admin/sounds', create_sound, name='create_sound'),
    path('sounds', get_sounds, name='get_sounds'),
    path('playlists', create_playlist, name='create_playlist'),
]
