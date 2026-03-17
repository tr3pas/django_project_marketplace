from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm, AddressForm
from .models import Profile, Address
from products.context_proccesor import _get_category_context
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit

CATEGORY_CACHE_TIL = 60 * 30  # 30 хвилин в секундах


@ratelimit(key="ip", rate="100/m", method="POST", block=True)
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("accounts:profile")
    else:
        form = LoginForm(request)
    context = _get_category_context(request)
    return render(request, "accounts/login.html", {**context, "form": form})


def logout_view(request):
    logout(request)
    return redirect("products:home")


@ratelimit(key="ip", rate="100/m", method="POST", block=True)
def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Реєстрацію завершено! Ласкаво просимо до Крамниці!"
            )
            return redirect("products:home")
    else:
        form = RegistrationForm()
    context = _get_category_context(request)
    return render(request, "accounts/register.html", {**context, "form": form})


@login_required
def profile_view(request):
    profile = cache.get(f"profile_{request.user.id}")
    if not profile:
        profile = get_object_or_404(Profile, user=request.user)
        cache.set(f"profile_{request.user.id}", profile, CATEGORY_CACHE_TIL)
    context = _get_category_context(request)
    return render(request, "accounts/profile.html", {**context, "profile": profile})


@login_required
@ratelimit(key="ip", rate="100/m", method="POST", block=True)
def edit_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    # Ensure address exists
    if profile.address is None:
        address = Address.objects.create(
            user=request.user, street="", city="", postal_code="", country=""
        )
        profile.address = address
        profile.save()
    else:
        address = profile.address

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        address_form = AddressForm(request.POST, instance=address)
        if user_form.is_valid() and profile_form.is_valid() and address_form.is_valid():
            user_form.save()
            profile_form.save()
            address_form.save()
            messages.success(request, "Профіль успішно оновлено!")
            return redirect("accounts:profile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        address_form = AddressForm(instance=address)
    context = _get_category_context(request)
    return render(
        request,
        "accounts/edit_profile.html",
        {
            **context,
            "user_form": user_form,
            "profile_form": profile_form,
            "address_form": address_form,
        },
    )


@login_required
@ratelimit(key="ip", rate="100/m", method="POST", block=True)
def delete_profile_view(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Ваш акаунт успішно видалено.")
        return redirect("products:home")
    context = _get_category_context(request)
    return render(request, "accounts/delete_profile.html", {**context})
