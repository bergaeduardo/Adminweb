from atexit import register
from django import template

register = template.Library()
@register.filter(name='has_group')
def has_group(user, group_name):
    grupo = user.groups.filter(name__exact=group_name).exists()
    return grupo


@register.filter(name='group_id') 
def group_id(user, idgroup):
    grupo = user.groups.filter(id__exact=idgroup).exists() 
    # print(grupo)
    return grupo

@register.filter(name='has_any_group')
def has_any_group(user, groups):
    """Verifica si el usuario pertenece a alguno de los grupos especificados."""
    if not user or not user.is_authenticated:
        return False
    group_list = groups.split(',')
    return user.groups.filter(name__in=group_list).exists()

@register.filter(name='get_user_groups')
def get_user_groups(user):
    """Obtiene una lista de los nombres de los grupos a los que pertenece el usuario."""
    if not user or not user.is_authenticated:
        return []
    return [group.name for group in user.groups.all()]


@register.filter(name='has_sup_group')
def has_sup_group(user):
    """Retorna True si el usuario pertenece a algún grupo terminado en '_sup'/'_Sup' o es admin."""
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name='admin').exists() or \
           user.groups.filter(name__iendswith='_sup').exists()