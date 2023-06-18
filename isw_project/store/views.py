from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from django.urls import reverse, reverse_lazy
from .forms import RegisterForm
from django.contrib.auth.models import User
from .models import Customer, ResidentialAddress, Product, ShoppingCart, CartProduct
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views import View
from django.shortcuts import render


class ProductListView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'products.html'
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(user=self.request.user)
        return context


class CustomerLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('products')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return self.render_to_response(self.get_context_data(form=form))

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
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name']
        )
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


class SearchView(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'search.html'
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        search_product = self.request.GET.get('search_product')
        queryset = super().get_queryset()
        if search_product:
            queryset = queryset.filter(name__icontains=search_product).order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = Customer.objects.get(user=self.request.user)
        return context
