from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Arrendador, Arrendatario, Inmueble, Comuna

class CustomUserCreationForm(UserCreationForm):
    TIPO_USUARIO_CHOICES = [
        ('arrendador', 'Arrendador'),
        ('arrendatario', 'Arrendatario'),
    ]
    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO_CHOICES, required=True, label="Tipo de Usuario")
    
    # Campos adicionales para arrendatarios
    ingresos_mensuales = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label="Ingresos Mensuales")
    ocupacion = forms.CharField(required=False, max_length=100, label="Ocupación")
    referencias = forms.CharField(required=False, widget=forms.Textarea, label="Referencias")
    
    # Campos de Persona
    nombres = forms.CharField(max_length=100, label="Nombres")
    apellidos = forms.CharField(max_length=100, label="Apellidos")
    rut = forms.CharField(max_length=12, label="RUT")
    direccion = forms.CharField(max_length=200, label="Dirección")
    telefono = forms.CharField(max_length=15, label="Teléfono")
    mail = forms.EmailField(max_length=100, required=False, label="Correo Electrónico")  # Campo añadido

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'tipo_usuario', 'nombres', 'apellidos', 'rut', 'direccion', 'telefono', 'mail')

    def save(self, commit=True):
        user = super().save(commit=False)
        tipo_usuario = self.cleaned_data['tipo_usuario']
        mail = self.cleaned_data['mail']  # Obtenemos el correo electrónico

        # Crear el objeto Arrendador o Arrendatario después de crear el User
        if tipo_usuario == 'arrendador':
            persona = Arrendador(
                user=user,
                nombres=self.cleaned_data['nombres'],
                apellidos=self.cleaned_data['apellidos'],
                rut=self.cleaned_data['rut'],
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                mail=mail,  # Asignamos el correo al Arrendador
            )
        else:  # Si es arrendatario
            persona = Arrendatario(
                user=user,
                nombres=self.cleaned_data['nombres'],
                apellidos=self.cleaned_data['apellidos'],
                rut=self.cleaned_data['rut'],
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                mail=mail,  # Asignamos el correo al Arrendatario
                ingresos_mensuales=self.cleaned_data['ingresos_mensuales'],
                ocupacion=self.cleaned_data['ocupacion'],
                referencias=self.cleaned_data['referencias'],
            )

        if commit:
            user.save()
            persona.save()  # Guardar la instancia de Persona
        
        return user


# forms.py

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, required=True)
    mail = forms.EmailField(max_length=100, required=False)  # Campo mail para la persona

    class Meta:
        model = User
        fields = ['email']  # Solo incluir el campo email del modelo User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Actualizar el email del User

        # Guardar el correo también en la instancia de Arrendador/Arrendatario
        persona = None
        if hasattr(user, 'arrendador'):
            persona = user.arrendador
        elif hasattr(user, 'arrendatario'):
            persona = user.arrendatario
        
        if persona:
            persona.mail = self.cleaned_data['mail']  # Actualizar el correo del modelo Arrendador/Arrendatario

        if commit:
            user.save()  # Guardar el usuario
            if persona:
                persona.save()  # Guardar la instancia de Persona (Arrendador/Arrendatario)

        return user

class ArrendadorEditForm(forms.ModelForm):
    class Meta:
        model = Arrendador
        fields = ['direccion', 'telefono', 'mail']

class ArrendatarioEditForm(forms.ModelForm):
    class Meta:
        model = Arrendatario
        fields = ['direccion', 'telefono', 'mail']

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = [
            'nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'estacionamientos',
            'habitaciones', 'banos', 'direccion', 'comuna', 'tipo_inmueble', 'precio_mensual'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'm2_construidos': forms.NumberInput(attrs={'class': 'form-control'}),
            'm2_totales': forms.NumberInput(attrs={'class': 'form-control'}),
            'estacionamientos': forms.NumberInput(attrs={'class': 'form-control'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'banos': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.Select(attrs={'class': 'form-control'}),
            'tipo_inmueble': forms.Select(attrs={'class': 'form-control'}),
            'precio_mensual': forms.NumberInput(attrs={'class': 'form-control'}),
        }
