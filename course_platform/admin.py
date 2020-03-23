from django.contrib import admin
from .models import *

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(ClassHour)
class ClassHourAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
