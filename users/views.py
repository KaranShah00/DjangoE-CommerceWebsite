from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from shopping.models import Product
from .models import Cart, Order, OrderDetails
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserAddressForm
from django.template import RequestContext
def calcPrice(order, items):
	total = 0
	for item in items:
		temp = item.product.cost * item.quantity
		OrderDetails.objects.create(order=order, product=item.product, quantity=item.quantity, subtotal=temp)
		total += temp
	order.amount = total
	order.save()


@login_required
def payment(request,tot):
    return render(request, 'users/paymentgateway.html',{'total':tot})
@login_required
def credit_card(request):
	return render(request, 'users/creditcard.html',{})
@login_required
def debit_card(request):
	return render(request, 'users/debitcard.html',{})
@login_required
def cod(request):
	return render(request,'users/cod.html',{})
def placeOrder(request):
	items = Cart.objects.filter(user=request.user)
	order = Order.objects.create(customer=request.user)
	calcPrice(order, items)

class viewOrder(LoginRequiredMixin, ListView):
	model = Order
	template_name = 'users/orders.html'
	context_object_name = 'orders'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(viewOrder, self).get_context_data()
		orders = Order.objects.filter(customer=self.request.user).order_by('-id')
		items = []
		for order in orders:
			items.append(OrderDetails.objects.filter(order=order))
		context['zipped'] = zip(items, orders)
		return context

def register(request):
	if request.method=='POST':
		form=UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, "users/register.html", {'form': form})

@login_required
def updateProfile(request):
	if request.method=='POST':
		u_form = UserUpdateForm(request.POST, instance = request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
		if(u_form.is_valid() and p_form.is_valid()):
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance = request.user)
		p_form = ProfileUpdateForm(instance = request.user.profile)
	context = {
	'u_form' : u_form,
	'p_form' : p_form
	}

	return render(request, "users/profile.html", context)	

def addToCart(user, product):
	new_cart_row = Cart(user=user, product=product)
	new_cart_row.save()

@login_required
def updateCart(request, par1, par2):
	user = request.user
	product = Product.objects.filter(title = par2).first()
	cart_row = Cart.objects.filter(user= user).filter(product = product).first()
	if par1=='add':
		#print("in here 1")
		if cart_row is None:
			addToCart(user, product)
			#print("in here")
		else:
			cart_row.quantity = cart_row.quantity+1
			cart_row.save()
			print("in here 123")
	elif par1=='remove':
		if cart_row is None:
			pass
		else:
			cart_row.quantity = cart_row.quantity-1
			cart_row.save()
			if cart_row.quantity==0:
				cart_row.delete()

	if len(Cart.objects.filter(user=user))==0:
		is_empty = True
	else:
		is_empty = False
		
	return render(request, 'users/cart.html', {'items':Cart.objects.filter(user=user),'add':'add','remove':'remove','is_empty':is_empty})

@login_required
def viewCart(request):
	user = request.user
	if len(Cart.objects.filter(user=user))==0:
		is_empty=True
	else:
		is_empty=False
	return render(request, 'users/cart.html', {'items':Cart.objects.filter(user=user), 'add':'add', 'remove':'remove','is_empty':is_empty})

@login_required
def checkout(request):
	user = request.user
	total = 0.0
	items = Cart.objects.filter(user = user)
	l = len(items)
	if(l == 0):
		is_empty = True
	else:
		is_empty = False
	for item in items:
		total += (item.product.cost * item.quantity)
	if(request.method == 'POST'):
		form = UserAddressForm(request.POST, instance = request.user.profile)
		if(form.is_valid()):
			form.save()
			return redirect('checkout')
	else:
		form = UserAddressForm(instance = request.user.profile)
	ftotal=total
	return render(request, 'users/checkout.html', {'items': items, 'total': total, 'form': form, 'is_empty': is_empty})