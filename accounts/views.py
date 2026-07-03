from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    SignupSerializer,
)

User = get_user_model()


class IndexView(APIView):
    def get(self, request):
        return render(request, "accounts/index.html", {"user": request.user})


class SignupView(APIView):
    def get(self, request):
        return render(request, "accounts/signup.html")

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect("login")
        return render(request, "accounts/signup.html", {"errors": serializer.errors, "data": request.data})


class LoginView(APIView):
    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            return redirect("index")
        return render(request, "accounts/login.html", {"errors": serializer.errors, "data": request.data})


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect("login")


class PasswordResetView(APIView):
    def get(self, request):
        return render(request, "accounts/password_reset.html")

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user:
                current_site = get_current_site(request)
                subject = "Password Reset for Shopline"
                message = render_to_string(
                    "accounts/password_reset_email.txt",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                    },
                )
                send_mail(subject, message, None, [email])
            return render(request, "accounts/password_reset_done.html")
        return render(request, "accounts/password_reset.html", {"errors": serializer.errors, "data": request.data})


class PasswordResetConfirmView(APIView):
    def get(self, request, uidb64, token):
        return render(request, "accounts/password_reset_confirm.html", {"uidb64": uidb64, "token": token})

    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data={**request.data, "uidb64": uidb64, "token": token})
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is None or not default_token_generator.check_token(user, token):
                return render(request, "accounts/password_reset_confirm.html", {"errors": {"token": ["Invalid link."]}})
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return render(request, "accounts/password_reset_complete.html")
        return render(request, "accounts/password_reset_confirm.html", {"errors": serializer.errors, "data": request.data, "uidb64": uidb64, "token": token})
