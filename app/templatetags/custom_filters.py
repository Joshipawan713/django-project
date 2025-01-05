from django import template

register = template.Library()

@register.filter(name='subtract')
def subtract(value, arg):
    """Subtract the arg from the value."""
    try:
        return int(float(value)) - int(float(arg))
    except (ValueError, TypeError):
        return value

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return int(float(value) * float(arg))
    except (ValueError, TypeError):
        return value
