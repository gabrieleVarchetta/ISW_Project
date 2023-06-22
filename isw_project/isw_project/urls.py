from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from store import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.RegistrationView.as_view(), name='register'),
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('products/', views.FilterProductsView.as_view(), name='products'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('shopping_cart/', views.CartView.product_list, name='shopping_cart'),
    path('order_summary/', views.CheckoutView.summary, name='order_summary'),
    path('checkout/', views.CheckoutView.checkout, name='checkout'),
    path('add_shipping_address/', views.CheckoutView.add_shipping_address, name='add_shipping_address'),
    path('add_payment_method/', views.CheckoutView.add_payment_method, name='add_payment_method'),
    url(r'ˆadd_to_cart/(?P<product_id>[-\w]+)/$', views.CartView.add_to_cart, name='add_to_cart'),
    url(r'delete_from_cart/(?P<product_id>[-\w]+)/$', views.CartView.delete_from_cart, name='delete_from_cart'),
    url(r'increase_product_quantity/(?P<product_id>[-\w]+)/$', views.CartView.increase_product_quantity, name='increase_product_quantity'),
    url(r'decrease_product_quantity/(?P<product_id>[-\w]+)/$', views.CartView.decrease_product_quantity, name='decrease_product_quantity')
]