from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from dairy.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):

    numbers=[1, 2, 3, 4, 5, 6]
    name = 'SIXPOUNDER'

    args={'name': name, 'numbers': numbers}
    return render(request, 'home.html', args)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dairy')
    else:
        form = RegistrationForm()
        args={'form':form}
        return render(request,'reg_form.html', args)


@login_required
def view_profile(request):


    args = {'user' : request.user}
    return render(request, 'profile.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/dairy/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form' : form}
        return render(request, 'edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/dairy/profile')
        else:
            return redirect('/dairy/change-password/')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form' : form}
        return render(request, 'change_password.html', args)
