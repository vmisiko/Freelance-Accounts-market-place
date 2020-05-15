from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "dashboard"

urlpatterns = [
  path('withdraw/', views.WithdrawalView.as_view(), name = "withdraw"),
  path('validate_withdraw/', views.validate_widthrawal, name = "Validate_withdraw"),
  path('transactions/', views.TransactionsView.as_view(), name = "transactions"),
  path('release_payment/', views.Release_Payment.as_view(), name='Release_Payment'),
  path("validate_release/", views.validate_release, name = "validate_release"),
  path("refund/", views.RefundView.as_view(), name = "refund"),
  path("valid_refund/", views.validate_refund, name = "valid_refund"),
  path("notifications", views.order_notification, name ="order_notification"),

]