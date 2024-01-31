from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)

    def __unicode__(self):
        return self.user.username
    
class Organization(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Library(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='libraries')

    def __str__(self):
        return f"{self.name} (in {self.organization})"

class Book(models.Model):
    name = models.CharField(max_length=128)
    # price = models.FloatField()
    author = models.CharField(max_length=128)
    publish_date = models.DateField()
    genre = models.CharField(max_length=128)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name
    
    def __str__(self):
        return self.title


class Img(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    img = models.ImageField(upload_to='image/%Y/%m/%d/')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name
