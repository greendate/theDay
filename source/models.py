from django.db import models
from django.contrib.auth.models import User
import os

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    telegram_alias = models.CharField(max_length=30, default="unknown")
    messenger_alias = models.CharField(max_length=30, default="unknown")
    interests_description = models.TextField(default="Something about me..")
    picture_url = models.ImageField(upload_to='source/static/images/', default="source/static/img/default-profile-icon-16.png")


class Event(models.Model):
    names = models.CharField(max_length=100)
    date = models.DateField()
    our_story = models.TextField()
    when = models.TimeField()
    where = models.CharField(max_length=30)
    picture_url = models.ImageField(upload_to='source/static/images/')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)


class Coming(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Image(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField()
    picture = models.ImageField(upload_to='source/static/images/')


class Status(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status_text = models.TextField()
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)


class Like(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    comment = models.TextField()
