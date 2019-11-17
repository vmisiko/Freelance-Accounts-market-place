from django.contrib import admin
from django.urls import path
from . import views

app_name = "Home"

urlpatterns = [

    path('', views.index.as_view(), name = "home"),
    path('home/', views.index.as_view(), name = "home"),
    path('payment/', views.view_paypal, name = 'payment'),
    path('validate_payment/', views.lnm_validate_post, name = 'validate_payment'),
    path('validate_stk_code/', views.validate_mpesa_code, name = 'validate_mpesa_code'),
    path('lnm/', views.LNMCallbackUrl.as_view(), name = 'lnm-callbackurl'),
    path('payment-done/', views.payment_done, name= 'payment-done'),
    path("lnm_payment/", views.view_for_mpesa, name = "mpesa_payment"),
    path('payment-cancelled/', views.payment_canceled, name = 'payment-cancelled'),
    path('product/<int:pk>/', views.Product.as_view(), name = "product" ),
    path('checkout/', views.Checkout.as_view(), name = 'checkout'),
    path('order-summary/', views.OrderSummaryView.as_view(), name = 'order-summary'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name = 'add_to_cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name = 'remove_from_cart'),
    path('remove_item_from_cart/<int:pk>/', views.remove_single_item_from_cart, name = 'remove_item_from_cart'),
    path('help/', views.see_example, name= 'help'),
    path('sell-account/', views.Sell_item.as_view(), name= "sell_account"),
    path('edit-account/<int:pk>/', views.Sell_item_Update.as_view(), name= "edit_account"),
]
