from django.shortcuts import render
from .models import WithdrawPayouts,Refund
from .forms import PayoutForm
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.models import User
from dashboard.models import AccountsModel
from Home.models import Order, Item
from django.views.decorators.csrf import csrf_exempt

from django.db.models.signals import post_save
import time
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
# from django.dispatch import receiver

ord_notif ={}
def order_placed(sender, instance, **kwargs):
    seller=""
    order_id = instance.id
    buyer = instance.user.username
    if instance.seller:
        seller = instance.seller.get_username()
    else:
        seller = instance.seller 
    ordered = instance.ordered
    released = instance.released
    refund = instance.refund

     
    ord_notif["order_id"] = order_id
    ord_notif["buyer"] = buyer
    ord_notif["ordered"] = ordered
    ord_notif["seller"] = seller
    ord_notif["released"] =  released
    ord_notif["refund"] = refund
    
    print(ord_notif)

    return ord_notif

post_save.connect(order_placed, sender=Order)


def order_notification(request):
    # print(ord_notif)
    data = {}
    for i in range(5):
        if "seller" in ord_notif:
            seller = ord_notif["seller"]
            buyer = ord_notif["buyer"]
            s= User.objects.get(username=seller)
            b = User.objects.get(username=seller)
            seller_email = s.email
            buyer_email = b.email
            ordered = ord_notif["ordered"]
            released = ord_notif["released"]
            refund = ord_notif["refund"]
            order1 ={}
            order2 = {}
            email_host = settings.EMAIL_HOST_USER
            
            if ordered ==True and released==False and refund == False:

                order1 = {

                    "title" : "Your Item has been Ordered!!",
                    "text" : f"Your product has been ordered by buyer {buyer}.Kindly visit your account to check for your orders and transactions "
                }

                order2 = {
                
                    "title" : "You have Ordered!!",
                    "text" : f"Your have Ordered a product from Seller {seller}.Kindly visit your account to check for your orders and transactions "
                }

            elif ordered ==True and released==True and refund == False:
                order1 = {

                    "title" : "Your cash has been Released!!",
                    "text" :  f"Your cash has been released by buyer {buyer}.Kindly visit your account to check your account balance, orders and transactions "
                }

                order2 = {
                
                    "title" : "Amount released!!",
                    "text" : f"Your cash has been released to seller {seller}. Kindly visit your account to check your account balance,orders and transactions"
                }
            elif ordered==True and released==True and refund == True:

                order1 = {

                    "title" : "Order cancelled!!",
                    "text" :  f"The order to your product has been cancelled by {buyer}.Kindly visit your account and email us immidiately if you have complains pertaining this action."
                }

                order2 = {
                    
                    "title" : "Order cancelled!!",
                    "text" : f"Your have cancelled your order to by from {seller}. Kindly visit your account to check your account balance,orders and transactions"
                }
            else:
                order1.clear()
                order2.clear()


            print(order1)
            print(order2)

            # subject = order1["title"]
            # html_message = render_to_string('dashboard/email.html', {'order': order1})

            # plain_message = strip_tags(html_message)

            # from_email = 'noreply@freelancingaccounts.com'
            # to = seller_email

            # mail.send_mail(subject, plain_message, from_email, [to], fail_silently=False, html_message=html_message)

            try:
                subject2 = order2["title"]
                html_message2 = render_to_string('dashboard/email.html', {'order': order2})

                plain_message2 = strip_tags(html_message)

                from_email2 = email_host
                to2 = buyer_email 
                print(subject2, from_email2, "print email 2")

                subject = order1["title"]
                html_message = render_to_string('dashboard/email.html', {'order': order1})

                plain_message = strip_tags(html_message)

                from_email = email_host
                to = seller_email

                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                mail.send_mail(subject2, plain_message2, from_email2, [to2],fail_silently=False, html_message=html_message2 )
                order1.clear()
                order2.clear()

            except:
                print( 'mail not sent')
            
            try:
                subject = order1["title"]
                html_message = render_to_string('dashboard/email1.html', {'order': order2})

                plain_message = strip_tags(html_message)

                from_email = 'victormisiko.vm@gmail.com'
                to = buyer_email

                mail.send_mail(subject, plain_message, from_email, [to],fail_silently=False, html_message=html_message )
                order2.clear()

            except:
                print( 'mail not sent')

            if ord_notif["seller"] == seller:


                data = { "order_id": ord_notif["order_id"],
                        "buyer" : buyer,
                        "ordered": ordered,
                        "seller":seller,
                        "released":released,
                        "refund":refund,
                        }

                print(data, "this is data")

    # time.sleep(1)
    ord_notif.clear()
    return JsonResponse(data)


# Create your views here.
class WithdrawalView(generic.ListView):
    model = WithdrawPayouts
    template_name = "dashboard/withdraw.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        payouts = WithdrawPayouts.objects.filter(user = self.request.user).order_by("-date")
        account = AccountsModel.objects.get(user = self.request.user)
        print(account.amount)
        context = super(WithdrawalView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        form = PayoutForm()
        amount = account.amount
                
        context = {"form": form,
                    "payouts": payouts,
                }
        if int(amount)!= 0:
            context["amount"] = "True"
        else:
            context["amount"] = "False"
        
        

        return context

def validate_widthrawal(request):

    data = {}  
    # profile = Account.objects.get(user = request.user)
    
    
    form = PayoutForm(request.POST or None)
    account = AccountsModel.objects.get(user__username=request.user)

    amount1 = account.amount
    
    if form.is_valid():
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        amount = form.cleaned_data.get("amount_requested")
        phone_number = form.cleaned_data.get("phone_number")
        payment_mode = form.cleaned_data.get("payment_mode")
        email = form.cleaned_data.get("email")
        
        amount_dispensed= 0
        data1 = {}
       
        # data["percentage"] = "2"
        # data['span'] = span
        # data['gross'] = amount
        # data["tcharges"]= dp
        # data["net"] = amount_dispensed

        dp = 0
        percentage = 0
        if int(amount) <= int(amount1):

            if payment_mode == "M":
                dp = 0.01*int(amount)
                amount_dispensed = amount - dp
                percentage = 0.01
            else:
                dp = 0.02*int(amount)
                amount_dispensed = amount - dp
                percentage = 0.02
            
            data1 = {
                "percentage":percentage,
                "tcharges":dp,
                "gross": amount,
                "net":amount_dispensed,
            }

            payout = WithdrawPayouts.objects.create(
                user = request.user,
                last_name = last_name,
                amount_requested = amount,
                amount_dispensed = amount_dispensed,
                phone_number = phone_number,
                payment_mode = payment_mode,
                email = email,

            )
            payout.save()

            
            account.amount = int(amount1) - int(amount)
            account.save()
            data["message"] =  "Withdrawal successful, your money is pending awaiting release"
            data["data1"] = data1
        else:

            data["message"] =  "Request declined, You requested more than you have in your account."
            data["more"] = "Request declined, You requested more than you have in your account."
        
        return JsonResponse(data)

    else:
        
        data["message"] =  "Not successful, form not valid"

        data["errors"] = form.errors.as_json()

        return JsonResponse(data)

class TransactionsView(generic.ListView):
    model = WithdrawPayouts
    template_name = "dashboard/view_transactions.html"

    def get_context_data(self, **kwargs):
        context = super(TransactionsView, self).get_context_data(**kwargs)

        order = Order.objects.filter(seller = self.request.user).order_by("-ordered_date")

        items = Item.objects.filter(created_by = self.request.user).order_by("-created_at")

        context["items"] = items

        context["order"] = order

        return context

class Release_Payment(generic.ListView):

    model = Order
    template_name = "dashboard/release_payment.html"

    def get_context_data(self, **kwargs):
        context = super(Release_Payment, self).get_context_data(**kwargs)
        
        order1 = Order.objects.filter(user = self.request.user, ordered= True, released = False)
        
        if order1:
            order = Order.objects.filter(user = self.request.user, ordered= True, released = False)
            self.order = order
            context["order"] = order

            return context

        return context
    
  
@csrf_exempt      
def validate_release(request):
    print(request.GET)

    account = AccountsModel.objects.get(user__username=request.user)

    amount = request.GET["amount"]
    order_id  = request.GET["id"]
    seller = request.GET["seller"]
    order = Order.objects.get(id=order_id )

    amount1 = int(account.amount) - int(amount)

    order.released = True

    for org in order.items.all():
        item_id = org.item.id

        item = Item.objects.get(id=item_id )
        item.sold = True
        item.save()


    order.save()

    account.amount = int(amount1)

    account.save()

    seller_account = AccountsModel.objects.get(user__username = seller )

    amount2 = seller_account.amount
    amount_deduct = int(amount) - 2
    print(amount, amount_deduct, "this is deducted amounts")
    amount3 = int(amount2) + int(amount_deduct)

    seller_account.amount = amount3

    seller_account.save()

    data = {"message":"true"}

    return JsonResponse(data)

class RefundView(generic.ListView):

    model = Order
    template_name = "dashboard/refund.html"

    def get_queryset(self):
        queryset =  super(RefundView, self).get_queryset()

        queryset = queryset.filter(user = self.request.user, ordered= True, refund=False, released =False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(RefundView, self).get_context_data(**kwargs)

        refund = Refund.objects.filter(user = self.request.user).order_by("-date")

        context["refund"] = refund

        return context



@csrf_exempt 
def validate_refund(request):
    orderid = request.GET["orderid"]
    amount = request.GET["amount"]
    seller = request.GET["seller"]
    item = request.GET["item"]
    message = request.GET["select"]
    other = request.GET["other"]
    mode = request.GET["mode"]
    data = {}
    print(item, "item")
    message1 = ''

    if other:
        message1 = other
    else:
        message1= message
    
    try:
        order =  Order.objects.get(id=orderid)
        order.refund= True
        order.save()
        
        refund = Refund.objects.create(
            user = request.user,
            item = item,
            seller = seller,
            amount = amount,
            reason = message1,
            orderid = orderid,
            mode = mode

            )
    

        data["message"] = "successful"
        print("success")

    except:

        data["message"] = "Not successful"
        print("failure")
    return JsonResponse(data)

def email_template(request):


    order = {
        "title": " Your Product  has been Ordered!!",
        "text": "Kindly visit your account to check for your orders and transactions "
    }

    context = {
        "order": order
    }

    return render(request, "dashboard/email.html", context)
    





    