from django import template

register = template.Library()


@register.filter(name='to_inter')
def to_inter(value):
    return int(value)



