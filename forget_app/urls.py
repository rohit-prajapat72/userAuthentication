from django.urls import path
from .views import home, user_login, register, user_logout ,password_reset_request,password_reset_done, CustomPasswordResetConfirmView,password_reset_complete
# forget_app/urls.py
urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
   # Password reset URLs
    path('password-reset/',password_reset_request, name='password_reset'),
    path('password-reset/done/', password_reset_done, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
        password_reset_complete, 
         name='password_reset_complete'),
]   