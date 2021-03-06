from atexit import register
from django import template

register = template.Library()
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name__exact=group_name).exists()