# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from .forms import LoginForm, SignUpForm
from django.contrib import messages
from .api_views import generar_sso_ticket


def _set_sso_cookie(response, user):
    response.set_cookie(
        settings.SSO_COOKIE_NAME,
        generar_sso_ticket(user),
        max_age=settings.SSO_TICKET_MAX_AGE,
        domain=settings.SSO_COOKIE_DOMAIN or None,
        secure=settings.SSO_COOKIE_SECURE,
        httponly=True,
        samesite='Lax',
    )
    return response


class LogoutView(DjangoLogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.delete_cookie(settings.SSO_COOKIE_NAME, domain=settings.SSO_COOKIE_DOMAIN or None)
        return response


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None
    #esta parte recolecta lo de next para hacer la redireccion claro si hay un next
    try:
        meta = request.META['QUERY_STRING'].split('=')[1]
    except IndexError:
        meta = None
    
    # print('Meta: ' + meta)
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response = redirect(meta) if meta is not None else redirect("/")
                return _set_sso_cookie(response, user)
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            # Usar messages framework para un mensaje flash
            messages.success(request, 'User created successfully!')
            
            # Redireccionar a login con un flag para mostrar SweetAlert2
            return redirect("/login?next=/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})