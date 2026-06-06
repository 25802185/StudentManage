from django.contrib import admin
from .models import ClassInfo


@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade', 'major', 'student_count', 'created_at']
