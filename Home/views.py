from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from . models import Products,Item, OrderItem, Order,BillingAddress, LNMOnline
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm,Mpesa_checkout, Mpesa_c2b_checkout
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import LNMOnlineSerializer
from djangoProject.mpesa.LipaNaMpesa import lipa_na_mpesa
from rest_framework.response import Response
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
# Create your views here

def callback1_variables(result_code, amount):
    result = result_code
    amount = amount

    if result:
        return (result, amount)
    else:
        return None
@csrf_exempt
def validate_mpesa_code(request):
    order = Order.objects.get(user = request.user,  ordered = False)
    amount = order.get_total()
    
    # form = Mpesa_checkout(request.POST or None)
    # form2 = Mpesa_c2b_checkout(request.POST or None)
    data = {}  
    mpesa_code = request.GET.get('mpesa_code', None)
    if mpesa_code:
        result1 = LNMOnline.objects.filter( MpesaReceiptNumber__iexact=mpesa_code, paid = False).exists()
        print(result1)

        # data["message"] = "Mpesa Code Does exist"
                
        # return JsonResponse(data)
        if result1 == True: 

            result = LNMOnline.objects.get(MpesaReceiptNumber = mpesa_code, paid = False)
            
            result.paid = True

            result.save()

            order.ordered = True
            order.items.ordered = True
            # order.items.ordered = True
            order.save()

            data["message"] = "Transaction Successful"
            
            return JsonResponse(data)

        else:

            data["message"] = "Mpesa Code Does not exist"
                
            return JsonResponse(data)
    else:
        data["message"] = "Enter Mpesa Code"
                
        return JsonResponse(data)

       

@csrf_exempt
def lnm_validate_post(request):
    order = Order.objects.get(user = request.user,  ordered = False)
    amount = order.get_total()
    # form = Mpesa_checkout(request.POST or None)
    # form2 = Mpesa_c2b_checkout(request.POST or None)
    data = {}  
    phone_number = request.GET.get('phone_number', None)
    if phone_number:
        
        try: 
            lipa_na_mpesa(phone_number = phone_number, amount = amount, AccountReference = "123456" )

            data["message"] = "Stk-push Successful!! \n Enter The mpesa code "
                
            return JsonResponse(data)
           
                
        except:
            # messages.warning(request, " Type in the correct Phone Number ")
            data[" err_message"] =  " Type in the correct Phone Number "
            return JsonResponse(data)
    else :
        # messages.warning(request, " The form is not valid ")
        data[" err_message"] =  " Type in the correct Phone Number "
        return JsonResponse(data)



class LNMCallbackUrl(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer

    permission_classes = [AllowAny]


    def create(self, request):
        print(request.data, "this is data")
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]

        try:
            if result_description != "[STK_CB - ]DS timeout.":

                merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
                print(merchant_request_id)
                checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
                print(checkout_request_id)
                result_code = request.data["Body"]["stkCallback"]["ResultCode"]
                print(result_code)
                result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
                print(result_description)
                amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
                print(amount)
                mpesa_reciept_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"] 
                print(mpesa_reciept_number)
                # balance = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][2]["Value"]
                # print(balance)
                transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
                print(transaction_date)
                phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
                print(phone_number) 

            else:
                print('the result descrption is timeout')
        except:
            print("error")

        from datetime import datetime
        str_transaction_date = str(transaction_date)
        print(str_transaction_date)
        transaction_datetime = datetime.strptime(str_transaction_date,"%Y%m%d%H%M%S")
        print(transaction_datetime) 

        transaction = LNMOnline.objects.create(
            MerchantRequestID  = merchant_request_id,
            CheckoutRequestID = checkout_request_id,
            ResultCode = result_code,
            ResultDesc = result_description,
            Amount = amount,
            MpesaReceiptNumber = mpesa_reciept_number,
            Balance = 0,
            TranscationDate = transaction_datetime,
            PhoneNumber = phone_number
        )
        
        transaction.save() 
        
        data = {
             "result_code" :result_code ,
             "amount": amount

                 }

        callback1_variables(result_code, amount)

        return Response(data)
    

def see_example(request):


    return render(request, 'example.html')
    

# class view_for_mpesa(generic.View):

def view_for_mpesa(request):
    
    order = Order.objects.get(user =request.user,  ordered = False)
    print(order.id, "this is the cool order number")
    form = Mpesa_checkout()
    form2 = Mpesa_c2b_checkout()
    
        
    context = {"form": form,
                "order":  order,
                "form2" : form2
    }
    
    return render(request, "payment_via_mpesa.html", context)

    # def post(self, *args, **kwargs):
    
    #     order = Order.objects.get(user =self.request.user,  ordered = False)
    #     print(order.id, "this is the cool order number")
    #     amount = order.get_total()
    #     form = Mpesa_checkout(self.request.POST or None)
    #     form2 = Mpesa_c2b_checkout(self.request.POST or None)
        
    #     if form.is_valid():
    #         phone_number  = form.cleaned_data.get('phone_number')
    #         print(phone_number)

    #          # registers the validate and confirmation url's for b2c
    #         # starts online checkout on given number
            
            
    #         try: 
    #             lipa_na_mpesa(phone_number = phone_number, amount = amount, AccountReference = "123456" )
                
    #             messages.info(self.request, " The form is valid ")
    #             result = callback1_variables()
    #             data = {
    #                 "result_code": result[0],
            
    #             }
                
    #             if result[0] == 0:
    #                 data['message'] = 'The transaction has been completed successfully!!'
    #             else:
    #                 data["error_message"] = "The transaction was not successful, please try again"

    #             return(data)
                
    #         except:
    #             messages.warning(self.request, " Type in the correct Phone Number ")
    #             return render(self.request, "payment_cancelled.html")
    #     else :
    #         messages.warning(self.request, " The form is not valid ")
    #         return render(self.request, "payment_cancelled.html")

@csrf_exempt
def payment_done(request):
    order = get_object_or_404(Order, user = request.user, ordered = False)

    result = callback1_variables()

    

    context = {
        "result": result
    }
    
    return render(request, 'payment_done.html' ,context)


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')


def view_paypal(request):
    
    order = Order.objects.get(user =request.user,  ordered = False)
    print(order.id, "this is the cool order number")
    host = request.get_host()
    # orderitem = OrderItem.objects.get(user =request.user,  ordered = False)
    # What you want the button to do.
    paypal_dict = {
        "business": "misikovictor123@gmail.com",
        "amount": str(order.get_total()),
        "item_name": 'Order {}'.format(order.id),
        "invoice": str(order.id),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('Home:payment-done')),
        "cancel_return": request.build_absolute_uri(reverse('Home:payment-cancelled')),
        "custom": request.user,  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form,
                "order":  order
    }

    
    return render(request, "payment.html", context)

class index(generic.ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"

class OrderSummaryView(LoginRequiredMixin, generic.View):

    def get(self, *args,**kwargs ):
        try:
            order = Order.objects.get(user = self.request.user,  ordered = False)
            context ={

                'object': order
            }

            return render( self.request, 'order_summary.html' , context )
            messages.error( self.request, "you have an Order" )

        except ObjectDoesNotExist:

            messages.error(self.request, "you do not have an Order")
            return redirect("/")


class Product(generic.DetailView):
    model = Item
    template_name = "product-page.html"


class Checkout(generic.View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user = self.request.user,  ordered = False)

        context = {
            "form": form,
            'order': order
        }
        return render(self.request, "checkout-page.html", context )


    def post(self, *args, **kwargs):
 
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user,  ordered = False)
            
            if form.is_valid():
            
                street_address  = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option =form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip_code = zip
                )

                billing_address.save()
                order.billing_address = billing_address

                if payment_option == "p":
                    return redirect("Home:payment"  )
                if payment_option =="M":
                    # messages.info(self.request, "Mpesa payment Mode Not yet Implemented")
                    return redirect("Home:mpesa_payment")  
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect("Home:checkout")
      
                self.request.session['order_id'] = order.id 

        except ObjectDoesNotExist:

            messages.error(self.request, "you do not have an Order")
            return redirect("/")



@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk= pk)
    order_item,created = OrderItem.objects.get_or_create(item = item ,user = request.user, ordered = False)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk = item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated to your cart ")
            return redirect("Home:order-summary")
        else:
            messages.info(request, "This item was added to your cart ")
            order.items.add(order_item)
            return redirect("Home:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart ")
    return redirect("Home:order-summary")

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk = pk)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order

        if order.items.filter( item__pk = item.pk ).exists():
            order_item = OrderItem.objects.filter( item = item , user = request.user, ordered = False )[0]

            order.items.remove(order_item)
            messages.info(request, "This item was removed to your cart ")
        else:
            #add a amessage saying your order does not contain this an orderItem
            messages.info( request, "This item was not in your cart!!")
            return redirect( "Home:order-summary" )

    else:
        #add a amessage saying the user doesnt have an order
        messages.info(request, "You do not have an active order ")
        return redirect("Home:order-summary" )

    return redirect("Home:order-summary" )

def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk = pk)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order

        if order.items.filter(item__pk = item.pk).exists():
            order_item = OrderItem.objects.filter(item = item ,user = request.user, ordered = False)[0]
            if order_item.quantity>1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            order_item.save()
            messages.info(request, "This item quantity was updated ")
        else:
            #add a amessage saying your order does not contain this an orderItem
            messages.info(request, "This item was not in your cart!!")
            return redirect("Home:order-summary" )

    else:
        #add a amessage saying the user doesnt have an order
        messages.info(request, "You do not have an active order ")
        return redirect("Home:order-summary")

    return redirect("Home:order-summary" )

class Sell_item(CreateView):
    model = Item
    fields = '__all__'
    template_name = "sell_item.html"


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(Sell_item, self).form_valid(form)
    
class Sell_item_Update(UpdateView):
    model = Item
    fields = '__all__'
    template_name = "sell_item.html"

