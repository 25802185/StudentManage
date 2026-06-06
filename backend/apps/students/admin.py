from django.contrib import admin
from .models import Student, InfoChangeRequest


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_no', 'name', 'gender', 'class_ref', 'status']


@admin.register(InfoChangeRequest)
class InfoChangeRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'field_name', 'status', 'created_at']
