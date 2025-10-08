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
    """Formatea una dimensión con 'cm' si tiene valor (ya en cm)"""
    if value and value != 0:
        try:
            return f"{float(value):.1f} cm"
        except (ValueError, TypeError):
            return "-"
    return "-"

@register.filter
def valor_cm(value):
    """Retorna el valor en cm (datos ya almacenados en cm)"""
    if value and value != 0:
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    return None

@register.filter
def mm_a_cm(value):
    """Alias de valor_cm para compatibilidad con templates existentes"""
    return valor_cm(value)

@register.filter
def cm3_a_m3(value):
    """Convierte cm³ a m³"""
    if value and value != 0:
        try:
            # 1 m³ = 1,000,000 cm³
            return round(float(value) / 1000000, 6)
        except (ValueError, TypeError):
            return None
    return None

@register.filter
def calcular_volumen_m3(articulo, tipo='embalaje'):
    """Calcula volumen en m³ desde dimensiones en cm"""
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
            # Volumen en cm³ (datos vienen en cm de la BD)
            volumen_cm3 = float(alto) * float(ancho) * float(largo)
            # Convertir a m³ (dividir por 1,000,000)
            volumen_m3 = volumen_cm3 / 1000000
            return round(volumen_m3, 6)
    except (ValueError, TypeError, AttributeError):
        pass
    return None

@register.filter
def calcular_densidad_kg_m3(articulo):
    """Calcula densidad en kg/m³ desde dimensiones en cm y peso en gramos"""
    try:
        peso_real = articulo.get('pesoReal') or 0
        alto = articulo.get('altoReal') or 0
        ancho = articulo.get('anchoReal') or 0
        largo = articulo.get('largoReal') or 0
        
        if peso_real and alto and ancho and largo:
            # Volumen en m³ (desde cm³)
            volumen_cm3 = float(alto) * float(ancho) * float(largo)
            volumen_m3 = volumen_cm3 / 1000000
            
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
    """Calcula la densidad del artículo (peso/volumen) desde dimensiones en cm"""
    try:
        peso = articulo.get('pesoReal', 0) or 0
        alto = articulo.get('altoReal', 0) or 0
        ancho = articulo.get('anchoReal', 0) or 0
        largo = articulo.get('largoReal', 0) or 0
        
        if peso > 0 and alto > 0 and ancho > 0 and largo > 0:
            # Volumen en cm³ (dimensiones ya en cm)
            volumen_cm3 = alto * ancho * largo
            densidad = peso / volumen_cm3  # g/cm³
            return round(densidad, 2)
        return 0
    except (TypeError, ZeroDivisionError):
        return 0