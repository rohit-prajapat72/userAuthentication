from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.conf import settings 
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User



# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
               
        if not username or not password:
            messages.error(request, "Please provide both username and password")
            return render(request, 'login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")        
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name'] 
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            try:
                user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name, email=email, password=password)
                user.save()
                messages.success(request, "Account created successfully!")
                return redirect('login')
            except IntegrityError:
                messages.error(request, "Username already exists. Please choose another one.")
    
    return render(request, 'register.html')

def user_logout(request):
    logout(request)
    return redirect('login')



def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        
        if associated_users.exists():
            for user in associated_users:
                # Generate token and uid
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Build reset link
                reset_link = f"{request.scheme}://{request.get_host()}/password-reset-confirm/{uid}/{token}/"
                
                # Prepare email
                subject = "Password Reset Request"
                email_body = render_to_string(
                    'users/password_reset_email.html',
                    {
                        'user': user,
                        'reset_link': reset_link,
                        'site_name': settings.SITE_NAME,
                    }
                )
                
                # Send email
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            
            return redirect('password_reset_done')
        
        messages.error(request, "No account found with that email address.")
    
    return render(request, 'users/password_reset.html')

def password_reset_done(request):
    return render(request, 'users/password_reset_done.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = SetPasswordForm
    success_url = '/password-reset-complete/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your password has been reset successfully!")
        return response

def password_reset_complete(request):
    return render(request,'users/password_reset_complete.html')

