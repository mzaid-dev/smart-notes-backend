from django.urls import path
from .views import RegisterView , VerifyOTPView ,LoginView , ResendOTPView , RequestDeleteAccountView , ConfirmDeleteAccountView , RequestPasswordResetView, ResetPasswordView

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    path('login/', LoginView.as_view(), name='login'),
    
    # Password Reset
    path('password-reset-request/', RequestPasswordResetView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', ResetPasswordView.as_view(), name='password-reset-confirm'),

    # Delete Account
    path('delete-account-request/', RequestDeleteAccountView.as_view(), name='delete-request'),
    path('delete-account-confirm/', ConfirmDeleteAccountView.as_view(), name='delete-confirm'),
]

