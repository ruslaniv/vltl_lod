from django import template
register = template.Library()


@register.filter(name='percentize')
def percentize(value):
    return value * 100