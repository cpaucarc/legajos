from django.urls import path
from apps.login.views import LoginView, LogoutView, Error403View, InicioView, UsuarioChangePasswordView

app_name = 'login'
urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', UsuarioChangePasswordView.as_view(), name='password-change'),
    path('403/', Error403View.as_view(), name='403'),
]
