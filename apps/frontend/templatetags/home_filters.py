from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string by the given delimiter and return a list."""
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter) if item.strip()]

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary."""
    return dictionary.get(key)

@register.filter
def join_with(value, delimiter=', '):
    """Join a list with the given delimiter."""
    if not value:
        return ''
    return delimiter.join(str(item) for item in value) 