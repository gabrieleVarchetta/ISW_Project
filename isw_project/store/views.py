from django.contrib.auth import login
from django.db import transaction, IntegrityError
from django.views.generic import FormView, ListView
from django.db.models.functions import Lower
from django.urls import reverse, reverse_lazy
from .forms import RegisterForm, AddressForm, PaymentMethodForm
from django.contrib.auth.models import User
from .models import Customer, ResidentialAddress, Product, ShoppingCart, CartProduct, Order, OrderProduct, \
    ShippingAddress, PaymentMethod
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect


class CustomerLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('products')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.request.user)
        return response


class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    @transaction.atomic
    def form_valid(self, form):
        try:
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
        except IntegrityError:
            messages.error(self.request, 'Choose a different username.')
            return redirect(reverse('register'))

        customer = Customer.objects.create(
            user=user,
            birth_day=form.cleaned_data['birth_day']
        )
        ResidentialAddress.objects.create(
            country=form.cleaned_data['country'],
            region=form.cleaned_data['region'],
            city=form.cleaned_data['city'],
            street_address=form.cleaned_data['street_address'],
            postal_code=form.cleaned_data['postal_code'],
            province=form.cleaned_data['province'],
            customer=customer
        )
        ShippingAddress.objects.create(
            country=form.cleaned_data['country'],
            region=form.cleaned_data['region'],
            city=form.cleaned_data['city'],
            street_address=form.cleaned_data['street_address'],
            postal_code=form.cleaned_data['postal_code'],
            province=form.cleaned_data['province'],
            customer=customer,
            default_shipping_address=True
        )
        PaymentMethod.objects.create(
            card_number=form.cleaned_data['card_number'],
            cardholder_name=form.cleaned_data['cardholder_name'],
            expiration_month=form.cleaned_data['expiration_month'],
            expiration_year=form.cleaned_data['expiration_year'],
            cvv=form.cleaned_data['cvv'],
            customer=customer,
            default_payment_method=True
        )

        messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)


class CartView(View):
    @classmethod
    def product_list(cls, request):
        customer = Customer.objects.get(user=request.user)
        shopping_cart, _ = ShoppingCart.objects.get_or_create(
            customer=customer)  # Assumi che l'utente sia autenticato
        context = {
            'cart': shopping_cart
        }

        return render(request, 'shopping_cart.html', context)

    @classmethod
    def add_to_cart(cls, request, product_id):
        product = Product.objects.get(id=product_id)
        shopping_cart, _ = ShoppingCart.objects.get_or_create(customer=Customer.objects.get(user=request.user))
        cart_product, created = CartProduct.objects.get_or_create(shoppingcart=shopping_cart.id, product=product)
        if not created:
            cart_product.quantity += 1
            cart_product.save()

        shopping_cart.products.add(cart_product)
        messages.info(request, 'Product added to cart!')
        return redirect(reverse('products'))

    @classmethod
    def delete_from_cart(cls, request, product_id):
        product = CartProduct.objects.get(id=product_id)
        if product:
            product.delete()
            messages.info(request, 'Product has been deleted!')
        return redirect(reverse('shopping_cart'))

    @classmethod
    def increase_product_quantity(cls, request, product_id):
        product = CartProduct.objects.get(id=product_id)
        product.quantity += 1
        product.save()
        return redirect(reverse('shopping_cart'))

    @classmethod
    def decrease_product_quantity(cls, request, product_id):
        product = CartProduct.objects.get(id=product_id)
        if product.quantity > 1:
            product.quantity -= 1
            product.save()
        else:
            cls.delete_from_cart(request, product_id)

        return redirect(reverse('shopping_cart'))


class FilterProductsView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'product_list'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('id')
        search_product = self.request.GET.get('search_product')
        if search_product:
            queryset = queryset.filter(name__icontains=search_product)

        filter_category = self.request.GET.get('filter_category')
        if filter_category and filter_category != 'None':
            queryset = queryset.filter(category=filter_category)

        order_by = self.request.GET.get('order_by')
        if order_by and order_by != 'None':
            if 'name' in order_by:
                if order_by.startswith('-'):
                    queryset = queryset.order_by(Lower('name')).reverse()
                else:
                    queryset = queryset.order_by(Lower('name'))
            else:
                queryset = queryset.order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Passa i parametri di ricerca e filtro al template
        context['search_product'] = self.request.GET.get('search_product')
        context['filter_category'] = self.request.GET.get('filter_category')
        context['order_by'] = self.request.GET.get('order_by')

        # Recupera le categorie dei prodotti
        context['categories'] = Product.objects.values_list('category', flat=True).distinct()
        print(context['categories'])
        context['customer'] = Customer.objects.get(user=self.request.user)
        return context


class CheckoutView(View):
    @classmethod
    def summary(cls, request):
        customer = Customer.objects.get(user=request.user)
        shopping_cart = ShoppingCart.objects.get(customer=customer)
        order, _ = Order.objects.get_or_create(customer=customer, pending=True)
        customer_shipping_addresses = ShippingAddress.objects.filter(customer=customer)
        customer_payment_methods = PaymentMethod.objects.filter(customer=customer)

        for product in shopping_cart.get_cart_products():
            quantity = product.quantity
            product = Product.objects.get(id=product.product.id)
            OrderProduct.objects.create(product=product, order=order, quantity=quantity)

        order.price = shopping_cart.get_cart_total()
        order.save()

        context = {
            'product_list': shopping_cart.get_cart_products(),
            'total': order.price,
            'address_form': AddressForm(),
            'payment_method_form': PaymentMethodForm(),
            'shipping_addresses': customer_shipping_addresses,
            'payment_methods': customer_payment_methods
        }

        return render(request, 'checkout.html', context)

    @classmethod
    def checkout(cls, request):
        customer = Customer.objects.get(user=request.user)
        default_shipping_address = ShippingAddress.objects.get(customer=customer, default_shipping_address=True)
        default_payment_method = PaymentMethod.objects.get(customer=customer, default_payment_method=True)
        shipping_address_id = request.POST.get('shipping_address')
        payment_method_id = request.POST.get('payment_method')
        order, _ = Order.objects.get_or_create(customer=customer, pending=True)

        if shipping_address_id and payment_method_id:
            shipping_address = ShippingAddress.objects.get(customer=customer, id=shipping_address_id)
            payment_method = PaymentMethod.objects.get(customer=customer, id=payment_method_id)
            order.shipping_address = shipping_address
            order.payment_method = payment_method
        else:
            order.shipping_address = default_shipping_address
            order.payment_method = default_payment_method

        shopping_cart = ShoppingCart.objects.get(customer=customer)

        for product in shopping_cart.get_cart_products():
            product.delete()

        order.pending = False
        order.save()
        messages.info(request, 'Order completed successfully')

        return redirect(reverse('products'))

    @classmethod
    def add_shipping_address(cls, request):
        customer = Customer.objects.get(user=request.user)

        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                ShippingAddress.objects.get_or_create(
                    country=form.cleaned_data['country'],
                    region=form.cleaned_data['region'],
                    city=form.cleaned_data['city'],
                    street_address=form.cleaned_data['street_address'],
                    postal_code=form.cleaned_data['postal_code'],
                    province=form.cleaned_data['province'],
                    customer=customer
                )

        return redirect(reverse('order_summary'))

    @classmethod
    def add_payment_method(cls, request):
        customer = Customer.objects.get(user=request.user)

        if request.method == 'POST':
            form = PaymentMethodForm(request.POST)
            if form.is_valid():
                PaymentMethod.objects.get_or_create(
                    card_number=form.cleaned_data['card_number'],
                    cardholder_name=form.cleaned_data['cardholder_name'],
                    expiration_month=form.cleaned_data['expiration_month'],
                    expiration_year=form.cleaned_data['expiration_year'],
                    cvv=form.cleaned_data['cvv'],
                    customer=customer
                )

        return redirect(reverse('order_summary'))
