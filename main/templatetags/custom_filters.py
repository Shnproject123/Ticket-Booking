from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """Splits a string by the given delimiter"""
    if not value:
        return []
    return value.split(delimiter)
