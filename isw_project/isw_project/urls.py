"""isw_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from store import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('shopping_cart/', views.CartView.product_list, name='shopping_cart'),
    url(r'ˆadd_to_cart/(?P<product_id>[-\w]+)/$', views.CartView.add_to_cart, name='add_to_cart'),
    url(r'delete_from_cart/(?P<product_id>[-\w]+)/$', views.CartView.delete_from_cart, name='delete_from_cart'),
    url(r'increase_product_quantity/(?P<product_id>[-\w]+)/$', views.CartView.increase_product_quantity, name='increase_product_quantity'),
    url(r'decrease_product_quantity/(?P<product_id>[-\w]+)/$', views.CartView.decrease_product_quantity, name='decrease_product_quantity')
]
