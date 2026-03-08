from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm, AddressForm
from .models import Profile, Address


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('account:profile')
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('products:home')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрацію завершено! Ласкаво просимо до Крамниці!')
            return redirect('products:home')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def edit_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    # Ensure address exists
    if profile.address is None:
        address = Address.objects.create(
            user=request.user, street='', city='', postal_code='', country=''
        )
        profile.address = address
        profile.save()
    else:
        address = profile.address

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        address_form = AddressForm(request.POST, instance=address)
        if user_form.is_valid() and profile_form.is_valid() and address_form.is_valid():
            user_form.save()
            profile_form.save()
            address_form.save()
            messages.success(request, 'Профіль успішно оновлено!')
            return redirect('account:profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        address_form = AddressForm(instance=address)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': address_form,
    })


@login_required
def delete_profile_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)    
        user.delete()
        messages.success(request, 'Ваш акаунт успішно видалено.')
        return redirect('products:home')
    return render(request, 'accounts/delete_profile.html')
