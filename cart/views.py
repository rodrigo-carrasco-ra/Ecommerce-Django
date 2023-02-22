from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
# Create your views here.

def cart (request):
    return render(request, 'store/cart.html')

def the_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=the_cart_id(request))# get the cart using the_cart_id present in the session cookie
        cart_items = CartItem.objects.filter(cart=cart, is_active=True) # get the cart items from the cart 
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) 
            quantity += cart_item.quantity
        tax = (19 * total)/100
        approximate_tax = round(tax)
        grand_total = total + approximate_tax 
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'approximate_tax': approximate_tax,
        'grand_total': grand_total,
    } # pass the cart items to the context
    #context is a dictionary that contains the data that we want to pass to the template
    return render(request, 'store/cart.html', context)

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id) # get the product using the product_id
    product_variation = [] # create an empty list
    if request.method == 'POST':
        for item in request.POST:#request.POST is a dictionary that contains the data that is sent in the request body in the form of key-value pairs. 
            key=item #item is the value color variation_value
            value = request.POST[key] #request.POST[key] is the value of the key. It should appear as, for example color black and size small.
            try:
                variation = Variation.objects.get(product_name=product, variation_category__iexact=key, variation_value__iexact=value) # get the variation using the product, variation category and variation value.
                product_variation.append(variation)
            except:
                pass
    try:
        cart = Cart.objects.get(cart_id=the_cart_id(request)) # get the cart using the_cart_id present in the session cookie
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=the_cart_id(request)
        )
        cart.save()

    does_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists() # check if the cart item exists
    if does_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product, cart=cart) # get the cart item
        # We need to check if the cart item has variations 
        # if the cart item has variations, we need to check if the new variation is the same as the old variation
        # if the new variation is the same as the old variation, we need to increment the quantity.
        # We check using existing_variation in the database, current_variation as the product_variation.append(variation) and item_id in the database.
        existing_variation_list = [] 
        id=[]
        for item in cart_item: # loop through the cart item looking for variations
            existing_variation = item.variations.all() # get the variations of the cart item
            existing_variation_list.append(list(existing_variation)) # append the variations to the existing variation list. list(existing_variation) is a list of variations of the cart item 
            id.append(item.id) # append the id of the cart item to the id list

        if product_variation in existing_variation_list: # check if the product variation exists in the existing variation list
            # we increase the cart item quantity
            index= existing_variation_list.index(product_variation) # get the index of the product variation in the existing variation list
            item_id = id[index] # get the id of the cart item using the index of the product variation in the existing variation list
            item = CartItem.objects.get(product=product, id=item_id) # get the cart item using the product and the id
            item.quantity += 1
            item.save()
        else:
            # we create a new cart item
            item = CartItem.objects.create(product=product, quantity=1, cart=cart) 
            if len(product_variation)>0: # check if the product variation exists
                cart_item.variations.clear()   # clear the variations
                cart_item.variations.add(*product_variation) # add the variations to the cart item. * means all the variations in the product variation list
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )# create a new cart item for the product
        if len(product_variation)>0:
            cart_item.variations.clear()   # clear the variations
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('cart')

def remove_from_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=the_cart_id(request)) # get the cart using the_cart_id present in the session cookie
    product = get_object_or_404(Product, id=product_id) # get the product using the product id, if the product does not exist, return a 404 error.
    try: 
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # get the cart item using the product, cart and the cart item id
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass 
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=the_cart_id(request)) # get the cart using the_cart_id present in the session cookie
    product = get_object_or_404(Product, id=product_id) # get the product using the product id
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) # get the cart item using the product, cart and the cart item id
    cart_item.delete()
    return redirect('cart')

def checkout(request):
    return render (request, 'store/checkout.html')