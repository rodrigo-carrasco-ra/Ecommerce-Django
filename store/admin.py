from django.contrib import admin
from .models import Product, Variation

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_available', 'category', 'modified_date')
    prepopulated_fields = {'slug': ('name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product_name', 'variation_category', 'variation_value') 

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)