from django import template


register = template.Library()


@register.filter
def price(pence):
    """
    A filter to convert pence to pounds
    """
    try:
        value = int(pence)
        return f"{value // 100}.{value % 100:02}"
    except (ValueError, ZeroDivisionError):
        return None
