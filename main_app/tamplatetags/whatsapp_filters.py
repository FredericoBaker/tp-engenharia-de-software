from django import template

register = template.Library()

@register.filter(name='format_whatsapp')
def format_whatsapp(value):
    value = ''.join(filter(str.isdigit, value))
    if len(value) == 10:
        return f"({value[:2]}) {value[2:6]}-{value[6:]}"
    elif len(value) == 11:
        return f"({value[:2]}) {value[2:7]}-{value[7:]}"
    else:
        return value  
