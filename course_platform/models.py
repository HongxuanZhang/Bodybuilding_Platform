from django.db import models
from django.contrib.auth.models import AbstractUser
from .UUIDTools import UUIDTools

class User(AbstractUser):
    tel = models.CharField(max_length=20)
    email = models.EmailField()
    age = models.IntegerField()
    sex = models.CharField(max_length=2)
    status = models.CharField(max_length=10)
    isAdmin = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

class Course(models.Model):
    name = models.CharField(max_length=30)
    id = models.UUIDField(primary_key=True, default=UUIDTools.uuid1_hex, editable=False)
    description = models.TextField()
    online_date = models.DateField(auto_now_add=True)
    student_num = models.IntegerField()
    star_rate = models.FloatField()
    tag = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class ClassHour(models.Model):
    name = models.CharField(max_length=30)
    chapter = models.IntegerField()
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    time = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

class CourseReview(models.Model):
    username = models.CharField(max_length=20)
    content = models.TextField()
    star = models.IntegerField()
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)

