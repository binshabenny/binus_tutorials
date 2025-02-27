
from django.urls import path
from . import views
from .views import razorpay_webhook

urlpatterns = [
    path('<str:order_id>/<int:fee>/', views.payment_page, name='payment_page'),
    path('<str:order_id>/<int:fee>/payment_success/', views.payment_success, name='payment_success'),
    path('<str:order_id>/<int:fee>/payment_failed/', views.payment_failed, name='payment_failed'),
    path('webhook/razorpay/', razorpay_webhook, name='razorpay_webhook'),
]
