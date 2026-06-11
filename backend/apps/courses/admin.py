from django.contrib import admin
from .models import Course, Semester


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_current', 'created_at']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'credit', 'class_ref', 'teacher', 'semester']
