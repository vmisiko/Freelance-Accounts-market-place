from django import template
from Home.models import Order
from dashboard.models import AccountsModel
from django.utils.html import format_html



register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user = user, ordered = False)
        if qs.exists():
            return qs[0].items.count()

    return 0

@register.filter
def account_cash(user):
    if user.is_authenticated:
        qs = AccountsModel.objects.get(user= user)
        amount= qs.amount
        return amount

@register.simple_tag(takes_context=True)
def live_notify_list(context, list_class='live_notify_list'):
    user = user_context(context)
    if not user:
        return ''

    notifications = user.notifications.unread()
    # print(notifications[1])
    notifications_li = "\n\n"
    for notification in notifications[:10]:
        
        notifications_li += f'<li style="border-left:5px solid green; " class="list-group-item pb-2">{notification}</li>\n'
    notifications_li += "\n"
    html = "<ul class='{list_class}'>{notifications_li}</ul>".format(list_class=list_class, notifications_li=notifications_li)

    return format_html(html)

def user_context(context):
    if 'user' not in context:
        return None

    request = context['request']
    user = request.user
    try:
        user_is_anonymous = user.is_anonymous()
    except TypeError:  # Django >= 1.11
        user_is_anonymous = user.is_anonymous

    if user_is_anonymous:
        return None
    return user