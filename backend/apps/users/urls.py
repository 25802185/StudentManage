from django.urls import path
from .views import LoginView, LogoutView, UserInfoView, ChangePasswordView, ResetPasswordView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('userinfo/', UserInfoView.as_view()),
    path('password/', ChangePasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
]
