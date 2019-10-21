from django.contrib import admin
from django.urls import path
from . import views

app_name = "Home"

urlpatterns = [
    path('', views.index.as_view(), name = "home"),
    path('home/', views.index.as_view(), name = "home"),
    path('payment/', views.view_paypal, name = 'payment'),
    path('payment-done/', views.payment_done, name= 'payment-done'),
    path('payment-cancelled/', views.payment_canceled, name = 'payment-cancelled'),
    path('product/<slug>', views.Product.as_view(), name = "product" ),
    path('checkout/', views.Checkout.as_view(), name = 'checkout'),
    path('order-summary/', views.OrderSummaryView.as_view(), name = 'order-summary'),
    path('add_to_cart/<slug>', views.add_to_cart, name = 'add_to_cart'),
    path('remove_from_cart/<slug>', views.remove_from_cart, name = 'remove_from_cart'),
    path('remove_item_from_cart/<slug>', views.remove_single_item_from_cart, name = 'remove_item_from_cart'),
    path('help/', views.see_example, name= 'help'),
]
