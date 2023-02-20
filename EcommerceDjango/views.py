from django.shortcuts import render
from store.models import Product
from django.http import HttpResponse

def home(request):
    products = Product.objects.all().filter(is_available=True) #filtering the products that are available
    
    context = {
        'products': products,
    } #context is a dictionary that contains the products that are available

    return render (request, 'home.html', context)

