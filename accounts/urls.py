from django.urls import path
from .views import (
    RegisterApiView, user_login, UpdateAccessApiView, PasswordResetConfirmView,
    LogoutApiView, ChangePasswordView, PersonalDataApiView, PasswordResetApiView,)


urlpatterns = [
    path("register/", RegisterApiView.as_view()),
    path("login/", user_login),
    path("update-token/", UpdateAccessApiView.as_view()),
    path("logout/", LogoutApiView.as_view()),
    path(' /', ChangePasswordView.as_view()),
    path('password_reset/', PasswordResetApiView.as_view()),
    path('personal-data/', PersonalDataApiView.as_view()),
    path('password-confirm/', PasswordResetConfirmView.as_view()),

]
