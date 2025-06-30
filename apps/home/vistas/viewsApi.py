from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from apps.settingsUrls import *
from apps.home.SQL.Sql_Tango import validar_factManualCargada
from rest_framework import viewsets, permissions
from consultasTango.models import EB_facturaManual
from django.db.models import F
from consultasTango.serializers import facturaManual
from consultasTango.forms import DateForm
from consultasLakersBis.models import Direccionario
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes,parser_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta


@api_view(['GET'])
def login(request):
    username = request.META.get('HTTP_USERNAME')
    password = request.META.get('HTTP_PASSWORD')

    if username is None or password is None:
        return Response({'error': 'Falta proporcionar el nombre de usuario o la contraseña'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Nombre de usuario o contraseña inválidos'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si el usuario pertenece al grupo "Adm01"
    if not user.groups.filter(name='admin').exists():
        return Response({'error': 'El usuario no pertenece a un grupo autorizado'}, status=status.HTTP_400_BAD_REQUEST)

    # Verificar si el usuario está activo
    if not user.is_active:
        return Response({'error': 'El usuario no está activo'}, status=status.HTTP_400_BAD_REQUEST)

    # token_date = date.today().strftime("%Y%m%d")
    if Token.objects.filter(user=user).exists():
        token = Token.objects.get(user=user)
        validacion = validate_token(Token.objects.get(user=user).key)
        # print('Token valido: ',validacion[0])
        if validacion[0] == False:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
        # Crear el token
        # token = Token.objects.create(user=user)

        # Obtener la fecha y hora actual en la zona horaria del servidor
        current_datetime = timezone.now()

        # Establecer la fecha y hora del token con la fecha y hora actual
        token.created = current_datetime
        token.save()

    return Response({'token': token.key}, status=status.HTTP_200_OK)

def validate_token(token):
    vilidateToken = True
    msgError = ''
    try:
        token = Token.objects.get(key=token)
    except Token.DoesNotExist:
        msgError = 'Token inválido'
        vilidateToken = False

    token_date = token.created
    c_dateTime = datetime.now().replace(tzinfo=timezone.utc) + timedelta(hours=3)
    c_date = c_dateTime.date()
    t_date = token_date.date()
    # Calcula la diferencia de tiempo
    diferencia_time = c_dateTime - token_date
    # Convierte la diferencia de tiempo a segundos
    diferencia_segundos = diferencia_time.seconds
    # Calcula la diferencia en horas
    diferencia_horas = diferencia_segundos // 3600
    # Si deseas obtener un valor absoluto (sin signo), puedes usar abs()
    diferencia_horas_abs = abs(diferencia_horas)
    # Finalmente, asigna el valor entero de la diferencia de horas
    diferencia_horas_entero = int(diferencia_horas_abs)

    if t_date != c_date:
        msgError = 'Token expirado'
        vilidateToken = False
    
    if diferencia_horas_entero > 3:
        msgError = 'Token expirado'
        vilidateToken = False

    return vilidateToken,msgError


def facturas_por_fecha(request):
    form = DateForm(request.GET)
    suc = Direccionario.objects.filter(canal__in=['PROPIOS', 'EXTERIOR'])
    listSuc = suc.values_list('nro_sucursal', flat=True)
    imagenes_por_sucursal = {}
    facturas_con_imagenes = []
    elemtosSuc =[]
    estado = {}
    cargaTango = {}
    vencePronto = False
    aux1 = 0

    if form.is_valid():
        date = form.cleaned_data['date'] 
        facturas = EB_facturaManual.objects.filter(fechaRegistro__date=date).values('numeroSucursal').annotate(count=Count('numeroSucursal'))
        facNum = EB_facturaManual.objects.filter(fechaRegistro__date=date).values('numeroSucursal').annotate(factManual=F('numeroFactura'))
        fact= 0
        contFact = 0
        for factura in facNum:
            fact_manual = factura['factManual']
            aux= validar_factManualCargada(str(factura['numeroSucursal']),fact_manual)
            
            if aux1 != factura['numeroSucursal']:
                fact = 0
                if aux == 1:
                    fact = fact + aux
                    cargaTango[factura['numeroSucursal']] = fact
            else:
                if aux == 1:
                    fact = fact + aux
                    cargaTango[factura['numeroSucursal']] = fact
            aux1 = factura['numeroSucursal']
        # print('cargaTango: ',cargaTango)
        for factura in facturas:
            numero_sucursal = factura['numeroSucursal']
            imagenes = list(EB_facturaManual.objects.filter(numeroSucursal=numero_sucursal,fechaRegistro__date=date).exclude(imgFactura=None).values_list('imgFactura', flat=True))
            tipoFac = list(EB_facturaManual.objects.filter(numeroSucursal=numero_sucursal,fechaRegistro__date=date).exclude(tipoFactura=None).values_list('tipoFactura', flat=True))
            vencimiento = list(EB_facturaManual.objects.filter(numeroSucursal=numero_sucursal,fechaRegistro__date=date).exclude(fechaVencimiento=None).values_list('fechaVencimiento', flat=True))
            fecha_actual = date.today()

            cant = facturas[contFact]['count']
            for i in range(cant):
                diferencia_dias = (vencimiento[i] - fecha_actual).days

                if diferencia_dias < 45:
                    vencePronto = True
                    estado[numero_sucursal] = vencePronto
                elemtosSuc.append((imagenes[i],tipoFac[i]))
   
            imagenes_por_sucursal[numero_sucursal] = dict(elemtosSuc)
            elemtosSuc.clear()
            contFact += 1
        
        vencePronto = False
        total_imagenes = {}
        for numero_sucursal in listSuc:
            total_imagenes[numero_sucursal] = len(imagenes_por_sucursal.get(numero_sucursal, {}))
        
        for numero_sucursal in listSuc:
            sucursal = Direccionario.objects.get(nro_sucursal=numero_sucursal)
            facturas_con_imagenes.append((numero_sucursal, total_imagenes.get(numero_sucursal, 0), sucursal.desc_sucursal, estado.get(numero_sucursal, False)))
            
        # print(facturas_con_imagenes)

    return render(request, 'appConsultasTango/listarFacturasManuales.html', {'form': form, 'facturas': facturas_con_imagenes, 'imagenes_por_sucursal': imagenes_por_sucursal, 'cargaTango': cargaTango})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getFacturas(request, numSuc):
    user = request.user
    token = request.auth
    vilidateToken, msgError = validate_token(token)
    if vilidateToken == False:
        return Response({'error': msgError}, status=status.HTTP_401_UNAUTHORIZED)

    today = timezone.now().date()
    last_five_days = today - timedelta(days=7)
    facturas = EB_facturaManual.objects.filter(numeroSucursal=numSuc, fechaRegistro__gte=last_five_days)
    serializer = facturaManual(facturas, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([JSONParser, MultiPartParser])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def postFactura(request):
    datos = request.data
    # print(datos)
    # Acceder al archivo adjunto (imagen de factura)
    img_factura = request.FILES.get('imgFactura')
    # return Response({'ok': 'ok'}, status=status.HTTP_200_OK)
    # Verificar si el número de factura ya existe para el día actual
    today = timezone.now().date()
    facturas_existentes = EB_facturaManual.objects.filter(
        numeroFactura=datos['numeroFactura'],
        tipoFactura=datos['tipoFactura'],
        fechaRegistro__date=today
    )
    
    if facturas_existentes.exists():
        return Response({'error': 'Número de factura ya existe para el día actual'}, status=status.HTTP_400_BAD_REQUEST)
    
    token = request.auth
    vilidateToken, msgError = validate_token(token)
    if vilidateToken == False:
        print('Error al obtener el token')
        return Response({'error': msgError}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = facturaManual(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class uploadFactura(viewsets.ModelViewSet):
#     queryset = EB_facturaManual.objects.all()
#     serializer_class = facturaManual
#     # permission_classes = [permissions.IsAuthenticated]
    

def altaFactura(request,IdSuc):
    return render(request, 'appConsultasTango/altaFactura.html')

