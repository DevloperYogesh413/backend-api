from django.urls import path
from . import api
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", api.SignupAPI.as_view(), name="api-signup"),
    path("login/", api.LoginAPI.as_view(), name="api-login"),
    path("logout/", api.LogoutAPI.as_view(), name="api-logout"),
    path("reset-password/", api.PasswordResetAPI.as_view(), name="api-reset-password"),
    path("reset-password-confirm/", api.PasswordResetConfirmAPI.as_view(), name="api-reset-password-confirm"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
