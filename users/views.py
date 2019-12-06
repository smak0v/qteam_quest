from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from users.models import User


def login_view(request):
    """Login view function"""

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            context = {
                'error': 'Пользователя с такими учетными данными не существует!',
                'username': username,
            }
            return render(request=request, template_name='users/login.html', context=context)
        if user.staff is True:
            login(request=request, user=user)
            return redirect(to='dashboard:dashboard')
        context = {
            'error': 'Вы не являетесь персоналом команды! Запросите доступ у администрации сервиса!',
            'username': username,
        }
        return render(request=request, template_name='users/login.html', context=context)
    return render(request=request, template_name='users/login.html')


def signup_view(request):
    """Signup view function"""

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                if not password1 or not password2 or password1 != password2:
                    context = {
                        'error': 'Пароли не совпадают или не были введены!',
                        'username': username,
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                    }
                    return render(request=request, template_name='users/signup.html', context=context)
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.set_password(password2)
                user.staff = True
                user.save()
                user = authenticate(username=username, password=password2)
                login(request=request, user=user)
                return redirect(to='dashboard:dashboard')
        context = {
            'error': 'Пользователь с таким именем или почтой уже существует!',
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }
        return render(request=request, template_name='users/signup.html', context=context)
    return render(request=request, template_name='users/signup.html')


def logout_view(request):
    """Logout view function"""

    logout(request=request)
    return redirect(to='accounts:login')
