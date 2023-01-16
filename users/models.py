from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _

class CastomUser(AbstractUser):
    ...


class Teacher(CastomUser):
    class Meta:
        verbose_name = _("teacher")
        verbose_name_plural = _("teachers")


class Subject(models.Model):
    title = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Group(models.Model):
    title = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.title


class Student(CastomUser):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")
