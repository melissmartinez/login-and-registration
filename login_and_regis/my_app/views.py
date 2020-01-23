from django.shortcuts import render, redirect
from .models import *
import bcrypt

def welcome(request):
    request.session.clear()
    return render(request, "logreg.html")

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    errors = User.objects.validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    user_in_db = User.objects.filter(email = request.POST['email']).first()

    if user_in_db:
        messages.error(request, "Invalid credentials")
        return redirect('/')

    hashedpw = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(first_name=request.POST['fname'],last_name = request.POST['lname'],email = request.POST['email'],password = hashedpw)

    request.session['user_id'] = new_user.id
    return redirect('/success')

def success(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        messages.error(request, "Please log in or register")
        return redirect('/')

    context = {
        "user":User.objects.get(id=user_id)
    }
    return render(request, 'success.html', context)

def login(request):
    found_user = User.objects.filter(email = request.POST['email'])
    print('&'*100)
    print(found_user)
    if len(found_user)>0:
        user_from_db = found_user[0]
        
        is_pw_correct = bcrypt.checkpw(
            request.POST['password'].encode(),
            user_from_db.password.encode()
        )
        if is_pw_correct:
            request.session['user_id'] = user_from_db.id
            return redirect('/success')
    messages.error(request, "Invalid cradentials")
    return redirect('/')

