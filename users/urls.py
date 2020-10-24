from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.register, name="register"),
    path('checkout/<str:tot>',views.payment,name="payment-gateway")  ,
    path('creditcard/',views.credit_card,name="credit-card") ,
    path('debitcard/',views.debit_card,name="debit-card"),
    path('cod/',views.cod,name="cod")

]