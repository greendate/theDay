from django.db import models
from django.contrib.auth.models import User
import os

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    telegram_alias = models.CharField(max_length=30)
    messenger_alias = models.CharField(max_length=30)
    interests_description = models.TextField()
    picture_url = models.URLField(max_length=120)


class Event(models.Model):
    names = models.CharField(max_length=100)
    date = models.DateField()
    our_story = models.TextField()
    when = models.TimeField()
    where = models.CharField(max_length=30)
    picture_url = models.URLField(max_length=120)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)


class Coming(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
