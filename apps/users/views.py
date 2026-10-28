from django.shortcuts import render

from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer,ForgotPasswordSerializer,ResetPasswordSerializer,UserListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self, request): 
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        User = get_user_model()

        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
        ).first()

        if user and user.has_usable_password():
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)

            reset_link = (
                f"{settings.FRONTEND_URL}/reset-password"
                f"?uid={uid}&token={token}"
            )

            send_mail(
                subject="Reset your CRM password",
                message=(
                    "You requested a password reset.\n\n"
                    f"Reset your password using this link:\n{reset_link}\n\n"
                    "If you did not request this, ignore this email."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

        return Response(
            {
                "message": (
                    "If an account exists with this email, "
                    "a password reset link has been sent."
)
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        # Decode user ID
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(
                pk=user_id,
                is_active=True,
            )
        except (
            TypeError,
            ValueError,
            OverflowError,
            UnicodeDecodeError,
            get_user_model().DoesNotExist,
        ):
            return Response(
                {"error": "Invalid or expired reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Verify reset token
        token_generator = PasswordResetTokenGenerator()

        if not token_generator.check_token(user, token):
            return Response(
                {"error": "Invalid or expired reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate password against this user
        try:
            validate_password(new_password, user=user)
        except ValidationError as exc:
            return Response(
                {"new_password": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save new password securely
        user.set_password(new_password)
        user.save(update_fields=["password"])

        return Response(
            {"message": "Password reset successfully."},
            status=status.HTTP_200_OK,
        )

User = get_user_model()


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by("first_name", "last_name")