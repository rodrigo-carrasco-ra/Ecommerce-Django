from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# For user activation:
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)  #
        if form.is_valid():  # Valida que los datos ingresados sean correctos
            first_name = form.cleaned_data[
                'first_name']  # form.cleaned_data returns a dictionary of validated form input fields and their values, where string primary keys are returned as objects.
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[
                0]  # split divide el string en una lista, en este caso se divide en dos, el nombre de usuario y el dominio ('@
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                               password=password, username=username)
            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request) # get the domain name
            email_subject = 'Activate your account in Great Kart Store'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user, # user is the object of the model Account
                'domain': current_site, # current_site is the domain name of the website
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # user.pk is the primary key of the user. urlsafe_base64_encode is a
                # function that encodes the primary key of the user. force_bytes is a function that converts the encoded primary key to bytes.
                'token': default_token_generator.make_token(user), # default_token_generator is a function that generates a token for the user
            })
            to_email = email # the email of the user
            send_email = EmailMessage(email_subject, message, to=[to_email]) # send_email is an object of the class EmailMessage
            send_email.send() # send the email
            #messages.success(request, 'Check your email to activate your account. Thank you.')
            return redirect('/accounts/login/?command=verification&email=' + email) 
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":  # Si el metodo es POST, es decir, se envio un formulario
        email = request.POST['email']  # Se obtiene el email del formulario
        password = request.POST['password']  # Se obtiene el password del formulario

        user = auth.authenticate(email=email, password=password)  # Se autentica el usuario

        if user is not None: # Si el usuario existe
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')  # Se renderiza la pagina de login

@login_required(login_url='login')  # Si el usuario no esta logueado, lo redirige a la pagina de login
def logout(request): # Si el usuario esta logueado, lo desloguea y lo redirige a la pagina de login
    auth.logout(request)
    messages.success(request, 'You are now logged out.')
    return redirect('login')

def activate (request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # decode the uidb64 to get the uid
        user = Account._default_manager.get(pk=uid) # get the user object using the uid
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None # if the user does not exist, set the user to None

    if user is not None and default_token_generator.check_token(user, token): # if the user exists and the token is valid
        user.is_active = True # activate the user
        user.save()
        messages.success(request, 'Your account was activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
    
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists(): # If the email exists in the database
            user = Account.objects.get(email__exact=email)  # Get the user object
            # Reset Password Email
            current_site = get_current_site(request) # get the domain name
            email_subject = 'Reset your password in Great Kart Store' # subject of the email
            message = render_to_string('accounts/reset_password_email.html', { # render the email template
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email # the email of the user
            send_email = EmailMessage(email_subject, message, to=[to_email]) # send_email is an object of the class EmailMessage
            send_email.send() # send the email
            messages.success(request, 'Password reset email has been sent to your email address.')  # send a success message to the user
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist. Try again.')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # decode the uidb64 to get the uid
        user = Account._default_manager.get(pk=uid) # get the user object using the uid
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None # if the user does not exist, set the user to None

    if user is not None and default_token_generator.check_token(user, token):# if the user exists and the token is valid
        request.session['uid'] = uid # store the uid in the session
        messages.success(request, 'Please reset your password.') # send a success message to the user
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has expired.') # send an error message to the user
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid') # get the uid from the session
            user = Account.objects.get(pk=uid) # get the user object using the uid
            user.set_password(password) # set the password of the user
            user.save() # save the user object
            messages.success(request, 'Password reset successful.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password')
    else:
        return render(request, 'accounts/reset_password.html')