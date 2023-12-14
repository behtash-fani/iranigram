from django import template

register = template.Library()


def response_count(value):
    return value.response_set.filter(status='approved').count()


register.filter('response_count', response_count)