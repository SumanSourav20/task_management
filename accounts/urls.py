from django.urls import path
from .views import (
    PasswordResetRequestView,
    PasswordResetVerifyView,
    ActivateUserView,
)

urlpatterns = [
    path('accounts/verify-email/<str:token>/', ActivateUserView.as_view(), name='verify-email'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/verify/', PasswordResetVerifyView.as_view(), name='password-reset-verify'),
]