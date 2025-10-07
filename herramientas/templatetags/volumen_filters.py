from django import template

register = template.Library()

@register.filter
def mul(value, multiplier):
    """Multiplica dos valores"""
    try:
        return float(value) * float(multiplier)
    except (ValueError, TypeError):
        return 0

@register.filter
def sub(value, subtrahend):
    """Resta dos valores"""
    try:
        return float(value) - float(subtrahend)
    except (ValueError, TypeError):
        return 0

@register.filter
def calcular_volumen(dimensiones):
    """Calcula el volumen dados alto, ancho y largo como diccionario"""
    try:
        alto = dimensiones.get('alto', 0) or 0
        ancho = dimensiones.get('ancho', 0) or 0
        largo = dimensiones.get('largo', 0) or 0
        return alto * ancho * largo
    except (AttributeError, TypeError):
        return 0

@register.filter
def formato_dimension(value):
    """Formatea una dimensión con 'cm' si tiene valor (convierte de mm)"""
    if value and value != 0:
        try:
            cm_value = round(float(value) / 10, 2)
            return f"{cm_value} cm"
        except (ValueError, TypeError):
            return "-"
    return "-"

@register.filter
def mm_a_cm(value):
    """Convierte milímetros a centímetros"""
    if value and value != 0:
        try:
            return round(float(value) / 10, 2)
        except (ValueError, TypeError):
            return None
    return None

@register.filter
def mm3_a_m3(value):
    """Convierte mm³ a m³"""
    if value and value != 0:
        try:
            # 1 m³ = 1,000,000,000 mm³
            return round(float(value) / 1000000000, 6)
        except (ValueError, TypeError):
            return None
    return None

@register.filter
def calcular_volumen_m3(articulo, tipo='embalaje'):
    """Calcula volumen en m³ desde dimensiones en mm"""
    try:
        if tipo == 'embalaje':
            alto = articulo.get('altoEmbalaje') or 0
            ancho = articulo.get('anchoEmbalaje') or 0
            largo = articulo.get('largoEmbalaje') or 0
        else:  # real
            alto = articulo.get('altoReal') or 0
            ancho = articulo.get('anchoReal') or 0
            largo = articulo.get('largoReal') or 0
            
        if alto and ancho and largo:
            # Volumen en mm³
            volumen_mm3 = float(alto) * float(ancho) * float(largo)
            # Convertir a m³ (dividir por 1,000,000,000)
            volumen_m3 = volumen_mm3 / 1000000000
            return round(volumen_m3, 6)
    except (ValueError, TypeError, AttributeError):
        pass
    return None

@register.filter
def calcular_densidad_kg_m3(articulo):
    """Calcula densidad en kg/m³"""
    try:
        peso_real = articulo.get('pesoReal') or 0
        alto = articulo.get('altoReal') or 0
        ancho = articulo.get('anchoReal') or 0
        largo = articulo.get('largoReal') or 0
        
        if peso_real and alto and ancho and largo:
            # Volumen en m³
            volumen_mm3 = float(alto) * float(ancho) * float(largo)
            volumen_m3 = volumen_mm3 / 1000000000
            
            # Peso en kg (convertir de gramos)
            peso_kg = float(peso_real) / 1000
            
            # Densidad = kg/m³
            densidad = peso_kg / volumen_m3
            return round(densidad, 2)
    except (ValueError, TypeError, AttributeError, ZeroDivisionError):
        pass
    return None
    return None

@register.filter
def formato_peso(value):
    """Formatea un peso con 'g' si tiene valor"""
    if value and value != 0:
        return f"{value} g"
    return "-"

@register.filter
def tiene_dimensiones_completas(articulo, tipo='embalaje'):
    """Verifica si un artículo tiene todas las dimensiones completas"""
    if tipo == 'embalaje':
        return all([
            articulo.get('altoEmbalaje'),
            articulo.get('anchoEmbalaje'), 
            articulo.get('largoEmbalaje')
        ])
    else:  # real
        return all([
            articulo.get('altoReal'),
            articulo.get('anchoReal'),
            articulo.get('largoReal')
        ])

@register.filter
def calcular_densidad(articulo):
    """Calcula la densidad del artículo (peso/volumen)"""
    try:
        peso = articulo.get('pesoReal', 0) or 0
        alto = articulo.get('altoReal', 0) or 0
        ancho = articulo.get('anchoReal', 0) or 0
        largo = articulo.get('largoReal', 0) or 0
        
        if peso > 0 and alto > 0 and ancho > 0 and largo > 0:
            # Convertir mm³ a cm³ y calcular densidad
            volumen_cm3 = (alto * ancho * largo) / 1000
            densidad = peso / volumen_cm3
            return round(densidad, 2)
        return 0
    except (TypeError, ZeroDivisionError):
        return 0