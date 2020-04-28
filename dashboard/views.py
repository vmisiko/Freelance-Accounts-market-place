from django.shortcuts import render
from .models import WithdrawPayouts,Refund
from .forms import PayoutForm
from django.views import generic
from django.http import JsonResponse
from dashboard.models import AccountsModel
from Home.models import Order, Item
from django.views.decorators.csrf import csrf_exempt


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
        amount = form.cleaned_data.get("amount")
        phone_number = form.cleaned_data.get("phone_number")
        payment_mode = form.cleaned_data.get("payment_mode")
        email = form.cleaned_data.get("email")
        

        
        if int(amount) <= int(amount1):

            payout = WithdrawPayouts.objects.create(
                user = request.user,
                last_name = last_name,
                amount = amount,
                phone_number = phone_number,
                payment_mode = payment_mode,
                email = email,

            )
            payout.save()

            
            account.amount = int(amount1) - int(amount)
            account.save()
            data["message"] =  "Withdrawal successful, your money is pending awaiting release"
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

    amount1 = int(order.amount) - int(amount)

    order.released = True

    order.save()

    account.amount = int(amount1)

    account.save()

    seller_account = AccountsModel.objects.get(user__username=seller )
    amount2 = seller_account.amount
    amount3 = int(amount2) + int(amount)

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
    message = request.GET["select"]
    other = request.GET["other"]
    mode = request.GET["mode"]
    data = {}

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

    





    