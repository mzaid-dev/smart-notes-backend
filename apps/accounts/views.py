import logging
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from .serializers import UserRegistrationSerializer, VerifyOTPSerializer
from .models import User
from .services import create_user_with_otp, send_otp_email

# Get an instance of a logger
logger = logging.getLogger('accounts')

class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Use the Service Layer!
                user = create_user_with_otp(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password']
                )
                logger.info(f"New user registered: {user.email}")
                
                return Response({
                    "message": "Registration successful. Check email for OTP.",
                    "email": user.email
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Registration failed for {serializer.validated_data.get('email')}: {str(e)}")
                return Response({"error": "Internal Server Error"}, status=500)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(views.APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            entered_otp = serializer.validated_data['otp']
            
            try:
                user = User.objects.get(email=email)
                if user.otp == entered_otp:
                    user.is_email_verified = True
                    user.otp = None 
                    user.save()
                    logger.info(f"User verified: {email}")
                    return Response({"message": "Account verified! You can now login."}, status=status.HTTP_200_OK)
                else:
                    logger.warning(f"Invalid OTP attempt for: {email}")
                    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request):
        login_input = request.data.get('login')
        password = request.data.get('password')

        if not login_input or not password:
            return Response({"error": "Please provide both login and password"}, status=status.HTTP_400_BAD_REQUEST)

        email_to_auth = None
        if '@' in login_input:
            email_to_auth = login_input
        else:
            try:
                user_obj = User.objects.get(username=login_input)
                email_to_auth = user_obj.email
            except User.DoesNotExist:
                pass

        if not email_to_auth:
             return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email_to_auth, password=password)

        if user:
            if not user.is_email_verified:
                 return Response({"error": "Email is not verified. Please verify OTP first."}, status=status.HTTP_403_FORBIDDEN)

            token, _ = Token.objects.get_or_create(user=user)
            logger.info(f"User logged in: {user.email}")
            return Response({
                "token": token.key,
                "user_id": user.id,
                "email": user.email
            }, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Failed login attempt for: {login_input}")
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class ResendOTPView(views.APIView):
    # Protect this endpoint!
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp_request'

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            if user.is_email_verified:
                return Response({"message": "Account is already verified. Please login."}, status=status.HTTP_200_OK)
            
            # Use Service
            send_otp_email(user, "Resend OTP")
            logger.info(f"OTP Resent to: {email}")
            return Response({"message": "New OTP sent to your email."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

class RequestPasswordResetView(views.APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp_request'

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            send_otp_email(user, "Reset Password")
            logger.info(f"Password reset requested for: {email}")
            return Response({"message": "Password reset OTP sent to email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        
        if not email or not otp or not new_password:
             return Response({"error": "Email, OTP, and New Password are required"}, status=status.HTTP_400_BAD_REQUEST)
             
        try:
            user = User.objects.get(email=email)
            if user.otp != otp:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.otp = None
            user.save()
            logger.info(f"Password reset successful for: {email}")
            return Response({"message": "Password has been reset successfully. Please login."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class RequestDeleteAccountView(views.APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'otp_request'

    def post(self, request):
        user = request.user
        send_otp_email(user, "Confirm Delete Account")
        logger.info(f"Delete account requested for: {user.email}")
        return Response({"message": "OTP sent to your email. Please verify to confirm deletion."}, status=status.HTTP_200_OK)

class ConfirmDeleteAccountView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        entered_otp = request.data.get('otp')

        if not entered_otp:
            return Response({"error": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.otp == entered_otp:
            # 1. Capture the email before the user is deleted
            user_email = user.email
            
            # 2. Send the "Goodbye" email
            try:
                send_mail(
                    subject="Account Deleted Successfully",
                    message="We are sorry to see you go. Your account and all associated data have been permanently deleted from Smart Notes.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log if email fails, but continue with deletion
                logger.error(f"Goodbye email failed for {user_email}: {str(e)}")

            # 3. Now delete the user
            user.delete()
            
            logger.info(f"Account permanently deleted: {user_email}")
            # Note: 204 status usually shows no body in Postman, 
            # so you won't see the "message" text.
            return Response({"message": "Account permanently deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)