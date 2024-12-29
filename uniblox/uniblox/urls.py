"""uniblox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from Products.views import ProductView
from Orders.views import OrdersView, get_admin_orders, get_admin_products
from Discounts.views import DiscountView, get_admin_discounts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', ProductView.as_view(), name='products'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('discounts/', DiscountView.as_view(), name='discounts'),
    path('adminorders/', get_admin_orders, name='admin_orders'),
    path('adminproducts/', get_admin_products, name='admin_products'),
    path('admindiscounts/', get_admin_discounts, name='admin_discounts'),
]
