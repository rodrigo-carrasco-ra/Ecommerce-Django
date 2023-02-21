from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.

def register (request):
    if request.method == 'POST': 
        form = RegistrationForm(request.POST) #
        if form.is_valid():#Valida que los datos ingresados sean correctos
            first_name = form.cleaned_data['first_name'] # form.cleaned_data returns a dictionary of validated form input fields and their values, where string primary keys are returned as objects.
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0] #split divide el string en una lista, en este caso se divide en dos, el nombre de usuario y el dominio ('@
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Congratulations! You have successfully registered')
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form
        }
    return render(request, 'accounts/register.html',context)

def login (request):
    return render(request, 'accounts/login.html')

def logout (request):
    return 