from django import template

register = template.Library()

# @register.filter
# def get_value(value, key):
#     if (key in value.keys()):
#         return value[key]
#     else:
#         return ""

@register.filter
def get_value(value, key):
    if value is not None and isinstance(value, dict) and key in value.keys():
        return value[key]
    else:
        return ""