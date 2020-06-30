from django.shortcuts import render
from .models import WithdrawPayouts,Refund, Email_notifications,Conversion
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
from .tasks import send_email_notifications, refund_order_save,order_save_notifications

ord_notif ={}
def order_placed(sender, instance, **kwargs):

    seller=""
    order_id = instance.id
    buyer = instance.user.username
    print(instance.seller, "this is instance .seller")
    if instance.seller:
        print(instance.seller, "this is instance .seller")
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
    
    order_save_notifications.delay(ord_notif)

    # if "seller" in ord_notif:
    #     seller = ord_notif["seller"]
    #     buyer = ord_notif["buyer"]
    #     s= User.objects.get(username=seller)
    #     b = User.objects.get(username=seller)
    #     seller_email = s.email
    #     buyer_email = b.email
    #     ordered = ord_notif["ordered"]

    #     released = ord_notif["released"]
    #     refund = ord_notif["refund"]
    #     order1 ={}
    #     order2 = {}
    #     email_host = settings.EMAIL_HOST_USER
            
    #     if ordered ==True and released==False and refund == False:

    #         order1 = {

    #             "title" : "Your Item has been Ordered!!",
    #             "text" : f"Your product has been ordered by buyer {buyer}.Kindly visit your account to check for your orders and transactions "
    #         }

    #         order2 = {
                
    #         "title" : "You have Ordered!!",
    #         "text" : f"Your have Ordered a product from Seller {seller}.Kindly visit your account to check for your orders and transactions "
    #     }

    #     elif ordered ==True and released==True and refund == False:
    #         order1 = {

    #             "title" : "Your cash has been Released!!",
    #             "text" :  f"Your cash has been released by buyer {buyer}.Kindly visit your account to check your account balance, orders and transactions "
    #         }

    #         order2 = {
            
    #             "title" : "Amount released!!",
    #             "text" : f"Your cash has been released to seller {seller}. Kindly visit your account to check your account balance,orders and transactions"
    #         }

    #     elif ordered==True and released==False and refund == True:

    #         order1 = {
                    
    #             "title" : "Order cancelled!!",
    #             "text" :  f"The order to your product has been cancelled by {buyer}.Kindly visit your account and email us immidiately if you have complains pertaining this action."
    #         }

    #         order2 = {
                    
    #             "title" : "Order cancelled!!",
    #             "text" : f"Your have cancelled your order to by from {seller}. Kindly visit your account to check your account balance,orders and transactions"
    #         }

    #     elif ordered==False and released==False and refund == False:

    #         order1 = {
                    
    #             "title" : "Order in Progress!!",
    #             "text" :  f"The order to your product is in progress by {buyer}."
    #         }

    #         order2 = {
                    
    #             "title" : "Order In Progress",
    #             "text" : f"Your have initiated an order from {seller}. Kindly select the payment option of your choice and complite your order"
    #         }
            

    #     else:
    #         order1.clear()
    #         order2.clear()


    #     print(order1)
    #     print(order2)

    #     email_notif1 = Email_notifications.objects.create(
    #         seller = seller,
    #         buyer = buyer,
    #         title = order1["title"],
    #         message= order1["text"],
    #         seller_email = seller_email,
    #         buyer_email = buyer_email

    #     )

    #     email_notif1.save()

    #     email_notif2 = Email_notifications.objects.create(
            
    #         seller = seller,
    #         buyer = buyer,
    #         title = order2["title"],
    #         message= order2["text"],
    #         seller_email = seller_email,
    #         buyer_email = buyer_email,

    #     )
        
    #     email_notif2.save()

    #     # try:
    #     #     send_email_notifications.delay()
    #     # except:
    #     #     pass

      

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

        if float(amount)!= 0:
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
    conversion = Conversion.objects.all()
    rate = [con.rate for con in conversion][0]
    charges = 0
    
    if form.is_valid():
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        amount = form.cleaned_data.get("amount_requested")
        phone_number = form.cleaned_data.get("phone_number")
        payment_mode = form.cleaned_data.get("payment_mode")
        email = form.cleaned_data.get("email")
        
        amount_dispensed= 0
        data1 = {}
       
        
        dp = 0
        percentage = 0
        if float(amount) <= float(amount1):


            if payment_mode == "M":
                amount_converted = float(amount) * rate
                if amount_converted <= 1000:
                    charges = 15.27
                    dp = float(charges) / float(rate)
                    amount_dispensed = float(amount) - round(float(dp), 2)
                    percentage = 1

                if amount_converted >= 10001:
                    charges = 22.40
                    dp = float(charges) / float(rate)
                    amount_dispensed = float(amount) - round(float(dp), 2)
                    percentage = 1

                if amount_converted >= 70001:
                    data["message"] =  "You have exceeded Mpesa withdrawal limit"

                    data["more"] = "You have exceeded Mpesa withdrawal limit,\n" + "You can withrwaw a to a maximum limit of KES 70,000 per transaction and Kes. 140,000 per day."
        
                    return JsonResponse(data)
               


            else:
                dp = 0.025*float(amount)
                amount_dispensed = amount - dp
                percentage = 2.5
            
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
        
        order1 = Order.objects.filter(user = self.request.user, ordered= True, released = False ,refund=False)
        
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

        queryset = queryset.filter(user = self.request.user, ordered= True, refund=False, released=False)

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
        # order =  Order.objects.get(id=orderid)
        # order.refund= True
        # order.save()
        refund_order_save.delay(orderid)
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
    





    