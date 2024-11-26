from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # URL para el registro
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # URL para iniciar sesión
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', views.home, name='home'),
    path('perfil/', views.perfil, name='perfil'),
    path('agregar-inmueble/', views.agregar_inmueble, name='agregar_inmueble'),
    path('inmueble-exitoso/', views.inmueble_exitoso, name='inmueble_exitoso'),
    path('inmueble/<int:pk>/editar/', views.editar_inmueble, name='editar_inmueble'),
    path('inmueble/<int:pk>/eliminar/', views.eliminar_inmueble, name='eliminar_inmueble'),
    path('inmuebles/', views.lista_inmuebles, name='lista_inmuebles'),
    path('disponibles/', views.lista_disponibles, name='lista_disponibles'),
]
