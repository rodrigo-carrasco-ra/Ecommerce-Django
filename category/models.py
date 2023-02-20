from django.db import models
from django.urls import reverse

# Create your models here.

class Category (models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    category_image= models.ImageField(upload_to='photos/categories', blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta: #this is a class that contains the meta data for the model
        verbose_name = 'category' #this is the singular name of the model
        verbose_name_plural = 'categories' #this is the plural name of the model

    def get_url(self): #this is a method that returns the url for the category
        return reverse ('products_by_category', args=[self.slug]) #this is the url for the category
    

    def __str__(self):
        return self.category_name