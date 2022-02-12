from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import LoginForm, SignupForm, PasswordChangingForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/profile/')
            else:
                messages.error(request, 'invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home(request):

    return render(request, 'home.html')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')

    else:
        return HttpResponseRedirect('/login/')


def user_register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


#  change password

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')

            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangingForm(request.user)
    # form= PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {'form1': form})
