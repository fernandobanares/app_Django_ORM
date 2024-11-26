from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # URL para el registro
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # URL para iniciar sesión
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
]
