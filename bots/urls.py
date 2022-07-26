from bots.views import bot
from django.urls import path

urlpatterns = [
    path('ANY-RANDOM-LINK/', bot, name="bot"),
]