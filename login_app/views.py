from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):

    return render(request, "index.html")


def register(request):

    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'],
                        email = request.POST['email'], password=pw_hash, birth_date = request.POST['birth_date'])

    user = User.objects.filter(email = request.POST['email'])
    logged_user = user[0]
    request.session['user_id'] = logged_user.id
    request.session['name'] = logged_user.first_name + " " + logged_user.last_name

    return redirect("/wall")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            request.session['name'] = logged_user.first_name + " " + logged_user.last_name
            return redirect("/wall")
        else:
            errors = User.objects.login_validator(request.POST)
            errors['wrong_password'] = "Wrong password!"
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
            return redirect("/")

def logout(request):
    del request.session['user_id']
    # request.session.clear()
    request.session.save()
    return redirect("/")