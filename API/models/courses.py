from django.db import models



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
