import random
from django.core.mail import send_mail
from django.conf import settings
from .models import User

def generate_otp():
    """Helper to create a 6-digit string"""
    return str(random.randint(100000, 999999))

def create_user_with_otp(username, email, password):
    """Creates a user and sends the verification email"""
    # 1. Create User
    user = User.objects.create_user(username=username, email=email, password=password)
    user.is_email_verified = False
    
    # 2. Generate OTP
    otp_code = generate_otp()
    user.otp = otp_code
    user.save()
    
    # 3. Send Email
    send_mail(
        'Verify Your SmartNotes Account',
        f'Your OTP code is: {otp_code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False
    )
    return user

def send_otp_email(user, subject_prefix="SmartNotes"):
    """Reusable function to generate and send OTP to any user"""
    otp_code = generate_otp()
    user.otp = otp_code
    user.save()
    
    send_mail(
        f'{subject_prefix}: OTP Verification', 
        f'Your OTP code is: {otp_code}', 
        settings.DEFAULT_FROM_EMAIL,
        [user.email],                 
        fail_silently=False
    )
    return otp_code