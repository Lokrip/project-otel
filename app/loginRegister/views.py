import uuid
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils.text import slugify
from .forms import AddUserForm, CreateUserForm
from django.urls import reverse
from app.settings import EMAIL_HOST_USER
from config.models import Profile
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import account_activation_token


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:blog-page')
        form = AddUserForm()
        context = {
            'title': 'Авторизация',
            'form': form
        }
        return render(request, 'loginRegister/login/login.html', context)
    
    def post(self, request):
        form = AddUserForm(data=request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:blog-page')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
        
        context = {
            'title': 'Произошла Ошибка',
            'form': form
        }
        return render(request, 'loginRegister/login/login.html', context)
    
def ViewsLogout(request):
    logout(request)
    return redirect('accounts:login')

class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        context = {
            'title': 'Регистрация',
            'form': form
        }
        return render(request, 'loginRegister/register/register.html', context)
    
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            
            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Такой Логин Уже Существует')
                elif Profile.objects.filter(user__username=username).exists():
                    messages.error(request, 'Профиль с таким Логином уже существует')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Пользователь с такой почтой уже существует')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.is_active = False
                    user.save()
    
                    # Generate unique slug
                    unique_id = uuid.uuid4().hex[:6]
                    slug = slugify(f"{username}-{unique_id}")
                    
                    # Create profile with user and slug
                    profile = Profile.objects.create(user=user, slug=slug)
    
                    # Send activation email
                    mail_subject = 'Активация вашего аккаунта'
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = account_activation_token.make_token(user)
                    activation_link = reverse('loginRegister:activate', kwargs={'uidb64': uid, 'token': token})
                    activation_url = request.build_absolute_uri(activation_link)
    
                    message = f'Привет, {user.username},\n\nПожалуйста, перейдите по ссылке ниже для активации вашего аккаунта:\n{activation_url}'
                    try:
                        send_mail(mail_subject, message, EMAIL_HOST_USER, [email])
                        messages.success(request, 'Please confirm your email address to complete the registration')
                        return redirect('accounts:login')
                    except Exception as e:
                        messages.error(request, f'Ошибка при отправке письма: {str(e)}')
        
        context = {
            'title': 'Произошла Ошибка',
            'form': form
        }
        return render(request, 'loginRegister/register/register.html', context)
    
    
class ActivateAccount(View):  # Создаем класс представления для активации аккаунта
    def get(self, request, uidb64, token):  # Метод для обработки GET-запросов
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))  # Декодируем ID пользователя
            user = User.objects.get(pk=uid)  # Получаем пользователя по ID
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):  # Обрабатываем возможные ошибки
            user = None
        
        if user is not None and account_activation_token.check_token(user, token):  # Проверяем токен активации
            user.is_active = True  # Активируем пользователя
            user.save()  # Сохраняем пользователя
            login(request, user)  # Выполняем вход пользователя
            messages.success(request, 'Ваш аккаунт был успешно активирован')
            return redirect('blog:blog-page')  # Перенаправляем на страницу блога
        else:
            messages.error(request, 'Ссылка активации недействительна')
            return redirect('accounts:login')  # Перенаправляем на страницу входа