from django.shortcuts import render, redirect
from .forms import NewStudentForm, LoginForm, NewTeacherForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def register_request_student(request):
    if request.method == "POST":
        form = NewStudentForm(request.POST)
        if form.is_valid():
            student = form.save()
        login(request, student)
        messages.success(request, "Registration successful.")
        return redirect("/login")
    form = NewStudentForm()
    return render(request=request, template_name="users/register.html", context={"register_form": form})


def register_request_teacher(request):
    if request.method == "POST":
        form = NewTeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
        login(request, teacher)
        messages.success(request, "Registration successful.")
        return redirect("/login")
    form = NewTeacherForm()
    return render(request=request, template_name="users/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return render(request=request, template_name="users/index.html", context={"login_form": form})
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = LoginForm()
    return render(request=request, template_name="users/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/login")
