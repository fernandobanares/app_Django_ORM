from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ArrendadorEditForm, ArrendatarioEditForm, UserEditForm, InmuebleForm
from .models import Arrendador, Arrendatario, Inmueble
from django.contrib import messages


@login_required
def home(request):
    return render(request, "home.html")

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Arrendador, Arrendatario  # Asegúrate de importar tus modelos

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Arrendador, Arrendatario  # Asegúrate de importar tus modelos

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo usuario
            user = form.save()

            # Verificar el tipo de usuario y crear la instancia correspondiente
            tipo_usuario = form.cleaned_data.get('tipo_usuario')

            # Verificar si ya existe un arrendatario o arrendador para el usuario
            if tipo_usuario == 'arrendatario':
                if not Arrendatario.objects.filter(user=user).exists():
                    arrendatario = Arrendatario(user=user)
                    arrendatario.save()
            elif tipo_usuario == 'arrendador':
                if not Arrendador.objects.filter(user=user).exists():
                    arrendador = Arrendador(user=user)
                    arrendador.save()

            # Redirigir al perfil del usuario
            return redirect('perfil')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})




# Vista para inicio de sesión
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("perfil")  # Redirige a la página de perfil
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

@login_required
def perfil(request):
    user = request.user

    # Crear el formulario para editar datos del usuario
    user_form = UserEditForm(request.POST or None, instance=user)

    # Verificar si el usuario es Arrendador o Arrendatario
    if hasattr(user, 'arrendador'):
        persona = user.arrendador
        persona_form = ArrendadorEditForm(request.POST or None, instance=persona)
    elif hasattr(user, 'arrendatario'):
        persona = user.arrendatario
        persona_form = ArrendatarioEditForm(request.POST or None, instance=persona)

    # Manejar la edición de perfil
    if request.method == 'POST':
        if user_form.is_valid() and persona_form.is_valid():
            # Guardar el formulario del usuario (User)
            user_form.save()

            # Guardar los datos de la persona (Arrendador/Arrendatario)
            persona_form.save()

            messages.success(request, 'Datos actualizados correctamente.')
            return redirect('perfil')  # Redirigir a la página de perfil para mostrar los cambios

    return render(request, 'perfil.html', {'user_form': user_form, 'persona_form': persona_form, 'user': user})

def agregar_inmueble(request):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            # Guarda el inmueble y asocia al arrendador actual
            inmueble = form.save(commit=False)
            inmueble.arrendador = request.user.arrendador  # Asegura que el arrendador esté asociado
            inmueble.save()
            return redirect('inmueble_exitoso')  # Redirige a una página de éxito, puedes crearla
    else:
        form = InmuebleForm()
    
    return render(request, 'agregar_inmueble.html', {'form': form})

def inmueble_exitoso(request):
    return render(request, 'inmueble_exitoso.html')

@login_required
def editar_inmueble(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk, arrendador=request.user.arrendador)

    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance=inmueble)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inmueble actualizado con éxito.')
            return redirect('home')  # Ajusta la redirección según tu aplicación
    else:
        form = InmuebleForm(instance=inmueble)

    return render(request, 'editar_inmueble.html', {'form': form, 'inmueble': inmueble})

@login_required
def eliminar_inmueble(request, pk):
    inmueble = get_object_or_404(Inmueble, pk=pk, arrendador=request.user.arrendador)

    if request.method == 'POST':
        inmueble.delete()
        messages.success(request, 'Inmueble eliminado con éxito.')
        return redirect('home')  # Ajusta la redirección según tu aplicación

    return render(request, 'eliminar_inmueble.html', {'inmueble': inmueble})

@login_required
def lista_inmuebles(request):
    # Filtrar inmuebles solo del arrendador actual, si es necesario
    inmuebles = Inmueble.objects.filter(arrendador=request.user.arrendador)
    return render(request, 'lista_inmuebles.html', {'inmuebles': inmuebles})

@login_required
def lista_disponibles(request):
    # Filtrar inmuebles disponibles
    inmuebles_disponibles = Inmueble.objects.filter(arrendador__isnull=False)  # Ajusta el filtro según tu modelo
    return render(request, 'lista_disponibles.html', {'inmuebles': inmuebles_disponibles})