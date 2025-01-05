from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from django.db.models import Q
from .forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        laptop = Product.objects.filter(category='L')
        mobiles = Product.objects.filter(category='M')
        twbw = Product.objects.filter(Q(category='TW') | Q(category='BW'))
        return render(request, 'app/home.html', {'topwears':topwears, 'laptop': laptop, 'mobiles': mobiles, 'twbw': twbw})

class ProductDetailView(View):
    def get(self, request, pk=None):
        if pk is None:
            return redirect('home')
        
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return redirect('home')
        return render(request, 'app/productdetail.html', {'product':product})

@login_required(login_url='login')
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        if product_id:
            product = Product.objects.get(id=product_id)
            cart_item = Cart.objects.filter(user=user, product=product).first()
            if cart_item:
                cart_item.quantity += 1
                cart_item.save()
            else:
                Cart(user=user, product=product).save()
            messages.success(request, 'Product added to cart successfully!')
            return redirect('product-detail', pk=product_id)
        return redirect('home')
    else:
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        shipping_amount = 70.0 if amount else 0
        total_amount = amount + shipping_amount if amount else 0
        context = {
            'cart_items': cart_items,
            'amount': amount,
            'shipping_amount': shipping_amount,
            'total_amount': total_amount,
        }
        return render(request, 'app/addtocart.html', context)

@login_required(login_url='login')
def buy_now(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id')
        if product_id:
            product = Product.objects.get(id=product_id)
            cart_item = Cart.objects.filter(user=user, product=product).first()
            if cart_item:
                cart_item.quantity += 1
                cart_item.save()
            else:
                Cart(user=user, product=product).save()
            return redirect('checkout')
    return redirect('home')

@login_required(login_url='login')
def address(request):
    address = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'address': address, 'active': 'btn-primary'})

@login_required(login_url='login')
def orders(request):
    return render(request, 'app/orders.html')

def mobile(request, data=None):
    try:
        base_query = Product.objects.filter(category='M')
        brands = Product.objects.filter(category='M').values_list('brand', flat=True).distinct().order_by('brand')
        context = {
            'data': data,
            'brands': brands,
            'has_error': False
        }
        if data is None:
            filmobile = base_query
        elif data in brands:
            filmobile = base_query.filter(brand=data)
        elif data == 'below':
            filmobile = base_query.filter(discounted_price__lt=40000)
        elif data == 'above':
            filmobile = base_query.filter(discounted_price__gt=25000)
        else:
            filmobile = base_query
            context['filter_error'] = f"Invalid filter: {data}"
        filmobile = filmobile.order_by('discounted_price')
        if not filmobile.exists():
            context['no_data'] = True
            if data:
                context['empty_message'] = f"No mobile phones found for: {data}"
            else:
                context['empty_message'] = "No mobile phones available at the moment"
        context['filmobile'] = filmobile
        return render(request, 'app/mobile.html', context)
    except Exception as e:
        context = {
            'has_error': True,
            'error_message': 'An error occurred while fetching products.',
            'filmobile': [],
            'data': data,
            'brands': []
        }
        return render(request, 'app/mobile.html', context)

class CustomerRegistrationView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
        
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! Registration Successful')
        return render(request, 'app/customerregistration.html', {'form':form})
        
@login_required(login_url='login')
def checkout(request):
    user = request.user
    addresses = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    shipping_amount = 70.0 if amount else 0
    total_amount = amount + shipping_amount if amount else 0
    
    context = {
        'addresses': addresses,
        'cart_items': cart_items,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': total_amount,
    }
    return render(request, 'app/checkout.html', context)

class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    authentication_form = LoginForm
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

def logout_view(request):
    logout(request)
    return redirect('login')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        if prod_id:
            user = request.user
            cart_item = Cart.objects.get(user=user, product__id=prod_id)
            cart_item.quantity += 1
            cart_item.save()
            
            # Get updated cart totals
            cart_items = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            shipping_amount = 70.0 if amount else 0
            total_amount = amount + shipping_amount
            
            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': total_amount
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'})

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        if prod_id:
            user = request.user
            cart_item = Cart.objects.get(user=user, product__id=prod_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            
            # Get updated cart totals
            cart_items = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            shipping_amount = 70.0 if amount else 0
            total_amount = amount + shipping_amount
            
            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': total_amount
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'})

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        if prod_id:
            user = request.user
            Cart.objects.filter(user=user, product__id=prod_id).delete()
            
            # Get updated cart totals
            cart_items = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
            shipping_amount = 70.0 if amount else 0
            total_amount = amount + shipping_amount
            
            data = {
                'amount': amount,
                'totalamount': total_amount
            }
            return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'})