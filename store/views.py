from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from cart.views import the_cart_id
from cart.models import CartItem
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.

def store(request, category_slug=None):
    categories = None 
    products = None 

    #if there is a category slug, then filter the products by the category slug

    if category_slug != None:
        
        categories = get_object_or_404(Category, slug=category_slug) #this is a function that returns an object or a 404 error if the object is not found
        products = Product.objects.filter(category=categories, is_available=True) #filtering the products by the category and if they are available
        paginator = Paginator(products, 1) #this is used to paginate the products. 6 products per page
        page = request.GET.get('page') #getting the page number from the url
        paged_products = paginator.get_page(page) #getting the products for the page
        product_count = products.count() #counting the number of products that are available
    
    #if there is no category slug, then show all the products
    else:

        products = Product.objects.all().filter(is_available=True).order_by('id') #filtering the products that are available
        paginator = Paginator(products, 2) #this is used to paginate the products. 6 products per page
        page = request.GET.get('page') #getting the page number from the url
        paged_products = paginator.get_page(page) #getting the products for the page
        product_count = products.count() #counting the number of products that are available
    
    context = {
        'products': paged_products ,
        'product_count': product_count,
    } #context is a dictionary that contains the products that are available
    return render (request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug) #getting the product by the category slug and the product slug. The category slug is used to get the category and then the product slug is used to get the product. The category slug is used to get the category because the product has a foreign key to the category. field__lookuptype=value is the example used to get the category slug
        in_cart = CartItem.objects.filter(cart__cart_id=the_cart_id(request), product=single_product).exists() #checking if the product is in the cart. Video 46. Exist() is used to check if the product is in the cart. If the product is in the cart, then the add to cart button will not be displayed

    except Exception as e:
        raise e #this is used to raise an exception if the product is not found

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    } #context is a dictionary that contains the product that is available
    return render (request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET: #if the keyword is in the request.GET, then filter the products by the keyword
        keyword = request.GET['keyword'] #getting the keyword from the url
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(name__icontains=keyword) | Q( description__icontains=keyword))#filtering the products by the keyword and ordering them by the created date in descending order #icontains is used to filter the products by the keyword #
            product_count= products.count() #counting the number of products that are available 
    context = {
        'products': products,
        'product_count': product_count,
    } #context is a dictionary that contains the products that are available
    return render(request, 'store/store.html', context)