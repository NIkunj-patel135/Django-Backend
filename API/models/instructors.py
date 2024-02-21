from django.db import models
from django.contrib.postgres.fields import ArrayField
from .courses import Courses

class Instructors(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=18,blank=True, default='')
    country = models.CharField(max_length=100,blank=True, default='')
    address = models.TextField(blank=True, default='')
    zipcode = models.CharField(max_length=50,blank=True, default='')
    password = models.CharField(max_length=400)
    profile_image = models.URLField(max_length=250,blank=True, default='')
#     # social_profiles =
#     # notifications_settings =
#     # linked_accounts =
    total_reviews = models.CharField(max_length=10,blank=True, default='')

    courses_taught = models.ManyToManyField(Courses)

    def __str__(self):
        return self.name