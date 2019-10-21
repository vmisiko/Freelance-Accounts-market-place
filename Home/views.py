from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from . models import Products,Item, OrderItem, Order,BillingAddress
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def see_example(request):
    return render(request, 'example.html')

@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')


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
                    messages.info(self.request, "Mpesa payment Mode Not yet Implemented")
                    return redirect("Home:checkout")  
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect("Home:checkout")
      
                self.request.session['order_id'] = order.id 

        except ObjectDoesNotExist:

            messages.error(self.request, "you do not have an Order")
            return redirect("/")

        




@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_item,created = OrderItem.objects.get_or_create(item = item ,user = request.user, ordered = False)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
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
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order

        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item = item ,user = request.user, ordered = False)[0]

            order.items.remove(order_item)
            messages.info(request, "This item was removed to your cart ")
        else:
            #add a amessage saying your order does not contain this an orderItem
            messages.info(request, "This item was not in your cart!!")
            return redirect("Home:order-summary" )

    else:
        #add a amessage saying the user doesnt have an order
        messages.info(request, "You do not have an active order ")
        return redirect("Home:order-summary" )

    return redirect("Home:order-summary" )

def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order

        if order.items.filter(item__slug = item.slug).exists():
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
