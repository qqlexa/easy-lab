from django.contrib import admin
from .models import Student, Subject, Teacher, Group
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Subject)


