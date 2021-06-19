from django import template
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from recipes.models import Favorite


register = template.Library()
User = get_user_model()


@register.filter 
def to_list(value, arg):
    value_list = value.order_by('-pub_date').all()
    return value_list[:int(arg)]


@register.filter
def less_or_equal(value, arg):
    return value <= int(arg)


@register.filter 
def to_str(value):
    return str(value)


@register.filter 
def remove_tag(value, arg):
    value_list = list(value)
    if arg in value_list:
        value_list.remove(arg)
    return ''.join(value_list)


@register.filter 
def add_tag(value, arg):
    value_list = str(value).split()
    value_list.append(arg)
    return ''.join(value_list)


@register.filter
def append_url_param(url, param):
    param = 'page=' + str(param)
    url_list = url.split('?')

    if len(url_list) > 1:
        param_list = url_list[1].split('&')
        param_dict = {}
        parameter_name = param.split('=')[0]

        for parameter in param_list:
            name = parameter.split('=')[0]
            param_dict.update({f'{name}': parameter})
        
        if parameter_name in param_dict:
            param_list.remove(param_dict[parameter_name])
        
        param = '?' + '&'.join(param_list) + '&' + param
    else:
        param = '?' + param

    return url_list[0] + param


@register.filter
def page(value):
    return f'page={value}'
