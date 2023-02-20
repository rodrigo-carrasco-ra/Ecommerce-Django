from django.db import models
from store.models import Product, Variation

# Create your models here.

class Cart (models.Model):
    cart_id = models.CharField(max_length=500, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id # This will return the cart_id as the name of the cart

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations= models.ManyToManyField(Variation,blank=True) # This is a many to many relationship with the Variation model
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity 

    def __unicode__(self):
        return self.product