# -*- encoding: utf-8 -*-
"""
Endpoints servidor-a-servidor para que el proyecto PHP (app.xl.com.ar) valide
usuarios contra Django: por credenciales (login propio de PHP) o por el ticket
de SSO (sso_ticket) que Django emite al loguearse.
"""
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle

_signer = TimestampSigner(salt='sso_ticket')


class HasPhpApiKey(BasePermission):
    """Autentica al llamador (el servidor PHP), no a un usuario final."""

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_X_PHP_API_KEY')
        return bool(settings.PHP_SSO_API_KEY) and api_key == settings.PHP_SSO_API_KEY


class PhpSsoThrottle(SimpleRateThrottle):
    scope = 'php_sso'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request),
        }


def generar_sso_ticket(user):
    return _signer.sign(str(user.pk))


def _user_payload(user):
    return {
        'valid': True,
        'user_id': user.id,
        'username': user.username,
        'groups': list(user.groups.values_list('name', flat=True)),
    }


@api_view(['POST'])
@permission_classes([HasPhpApiKey])
@throttle_classes([PhpSsoThrottle])
def validar_credenciales(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'valid': False}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is None or not user.is_active:
        return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(_user_payload(user), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([HasPhpApiKey])
@throttle_classes([PhpSsoThrottle])
def validar_sso(request):
    ticket = request.data.get('ticket')
    if not ticket:
        return Response({'valid': False}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_id = _signer.unsign(ticket, max_age=settings.SSO_TICKET_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.filter(pk=user_id, is_active=True).first()
    if user is None:
        return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(_user_payload(user), status=status.HTTP_200_OK)
