from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """从字典中获取指定键的值"""
    return dictionary.get(key) if dictionary else None
