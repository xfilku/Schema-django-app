from django import template

register = template.Library()

@register.filter
def get_icon(icon_dict, name):
    return icon_dict.get(name, 'fa-circle')
