from django.db import models
from django.contrib.postgres.fields import ArrayField

class Courses(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    pre_video_content = models.TextField()
    course_content = models.TextField()
    marketing_content = models.TextField()
#     # # students_enrolled = 
    created_at = models.DateField()
    last_modified_at = models.DateField()
    course_type = models.CharField(max_length=50)
    certification_avaliable = models.BooleanField()
    fees = models.CharField(max_length=50)
    plan_type = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Instructors(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=18)
    country = models.CharField(max_length=100)
    address = models.TextField()
    zipcode = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    profile_image = models.URLField(max_length=250)
#     # social_profiles =
#     # notifications_settings =
#     # linked_accounts =
    total_reviews = models.CharField(max_length=10)

    courses_taught = models.ManyToManyField(Courses)

    def __str__(self):
        return self.name
class Students(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=30)
    password = models.CharField(max_length=400)
    profileImage = models.URLField(max_length=250)
    billinginfo = models.CharField(max_length=200)
    subscription = models.CharField(max_length=200)
    fees_amount_paid = models.CharField(max_length=30)
    payment_method = models.CharField(max_length=30)
    wishlist = ArrayField(models.CharField(max_length=50), size=10)
    # wishlist = models.ManyToManyField(Courses)


    courses_enrolled = models.ManyToManyField(Courses)
    def __str__(self):
        return self.name