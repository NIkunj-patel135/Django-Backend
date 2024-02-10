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
    course_video = models.URLField(max_length=300,blank=True,default="")
    instructor_id = models.CharField(max_length=1000,blank=True,default="")    

    def __str__(self):
        return self.title


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
class Students(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=30,blank=True, default='')
    password = models.CharField(max_length=400)
    profileImage = models.URLField(max_length=250,blank=True, default='')
    billinginfo = models.CharField(max_length=200,blank=True, default='')
    subscription = models.CharField(max_length=200,blank=True, default='')
    fees_amount_paid = models.CharField(max_length=30,blank=True, default='')
    payment_method = models.CharField(max_length=30,blank=True, default='')
    wishlist = ArrayField(models.CharField(max_length=50), size=10,blank=True,null=True)
    # wishlist = models.ManyToManyField(Courses)


    courses_enrolled = models.ManyToManyField(Courses)
    def __str__(self):
        return self.name