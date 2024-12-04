from django.db import models

from pereval.passage.extensons import *


class User(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    fam = models.TextField(max_length=20)
    name = models.TextField(max_length=20)
    otc = models.TextField(max_length=20)

class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    heitht = models.IntegerField()


class Levels(models.Model):
    winter = models.CharField(max_length=3,choices=LEVEL, null=True,blank=True)
    summer = models.CharField(max_length=3,choices=LEVEL, null=True,blank=True)
    autumn = models.CharField(max_length=3,choices=LEVEL, null=True,blank=True)
    spring = models.CharField(max_length=3,choices=LEVEL, null=True,blank=True)

class Passages(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    beauty_title = models.TextField(null=True, blank=True)
    other_titlt =models.CharField(max_length=100, null=True, blank=True)
    add_time =models.DateTimeField(auto_now_add=True, null=True, blank=True)
    connect = models.TextField(null=True, blank=True)
    status =models.CharField(max_length=10, choices=CHOICE_TYPE, default='new')

    user = models.ForeignKey(Coordinates, on_delete=models.CASCADE)
    coordinates = models.ForeignKey(Coordinates,on_delete=models.CASCADE)
    level = models.TextField(Levels, on_delete=models.CASCADE)

class Images(models.Model):
    urls = models.URLField(null=True, blank=True)
    title = models.TextField(max_length=255, null=True, blank=True)

    passage = models.FloatField(Passages, on_delete=models.CASCADE, null=True, blank=True)