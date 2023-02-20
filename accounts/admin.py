from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.

class AdminAccount(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'date_joined', 'last_login', 'is_admin', 'is_staff') #Para que se muestren los campos para cambiar en el sitio admin 
    list_display_links = ('email', 'username', 'first_name', 'last_name') 
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',) #Para que se muestren los mas recientes primero
    filter_horizontal   = ()
    list_filter         = ()
    fieldsets           = ()

admin.site.register(Account, AdminAccount)


