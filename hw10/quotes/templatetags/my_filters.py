from django import template

register = template.Library()

@register.filter
def stylized_quotes(value):
    return f'«{value}»'
