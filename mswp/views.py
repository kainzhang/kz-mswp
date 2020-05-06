from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Invalid username or password')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(max_length=16, min_length=6, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}
    ))
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}
    ))
    password = forms.CharField(max_length=24, min_length=8, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))
    confirm_password = forms.CharField(max_length=24, min_length=8, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}
    ))

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')

        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email has been registered')

        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')

        return self.cleaned_data


def index(request):
    return render(request, "index.html")


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = form.cleaned_data['user']
        auth.login(request, user)
        return redirect(request.GET.get('from', reverse('index')))

    data = {'form': form}
    return render(request, 'login.html', data)


def logout(request):
    auth.logout(request)
    return redirect((request.GET.get('from', reversed('index'))))


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = RegForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = User.objects.create_user(username, email, password)
        user.save()

        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        return redirect(request.GET.get('from', reverse('index')))

    data = {'form': form}
    return render(request, 'register.html', data)
