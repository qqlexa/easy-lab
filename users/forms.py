from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Student, Group, Teacher
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    class Meta:
        model = Teacher
        fields = ('username', 'password')


class NewStudentForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(Group.objects.all())

    class Meta:
        model = Student
        fields = ("username", "email", "group", "password1", "password2")

    def save(self, commit=True):
        student = super(NewStudentForm, self).save(commit=False)
        student.email = self.cleaned_data['email']
        if commit:
            student.save()
        return student


class NewTeacherForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Teacher
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        teacher = super(NewTeacherForm, self).save(commit=False)
        teacher.email = self.cleaned_data['email']
        if commit:
            teacher.save()
        return teacher
