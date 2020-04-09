from django import template
from allauth.account.forms import LoginForm

register = template.Library()

@register.inclusion_tag('logins/login_form.html')
def login_form_tag(current_page=None):
    return {'loginform': LoginForm(),
            'redirect_to': current_page}
