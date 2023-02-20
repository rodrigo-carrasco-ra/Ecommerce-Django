from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #on_delete=models.CASCADE, means that if the category is deleted, the product will be deleted too !!!
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name



    
class VariationManager(models.Manager): # VariationManager is a class that inherits from models.Manager
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True) # super() is a function that returns a temporary object of the parent class. We use super() to make a method call to the parent class. In this case, we call the filter() method of the parent class, which is models.Manager. We pass the variation_category='color' and is_active=True arguments to the filter() method. The filter() method returns a QuerySet of all the objects that match the filter arguments. We then return the QuerySet.
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    
class Variation(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=150, choices=(('color', 'color'), ('size', 'size')))
    variation_value = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.variation_value
    
    objects = VariationManager()    