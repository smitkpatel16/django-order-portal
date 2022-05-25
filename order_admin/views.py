from django.http import HttpResponse
from django.shortcuts import render
from order_admin.models import Product


def home(request):
    return render(request, 'index.html')


def product(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})
