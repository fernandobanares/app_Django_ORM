from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Arrendador, Arrendatario, Inmueble
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# forms.py

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
    email = forms.EmailField(max_length=100, required=True)  # Asegurándote de que el campo email esté presente
    mail = forms.EmailField(max_length=100, required=False)  # Campo mail para la persona (Arrendador/Arrendatario)
    
    class Meta:
        model = User
        fields = ['email']  # Incluir el campo email del modelo User
    
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
            persona.mail = self.cleaned_data.get('mail', persona.mail)
            if commit:
                persona.save()  # Guardar la instancia de Arrendador/Arrendatario
        if commit:
            user.save()
        return user

class ArrendadorEditForm(forms.ModelForm):
    class Meta:
        model = Arrendador
        fields = ['direccion', 'telefono', 'mail']

class ArrendatarioEditForm(forms.ModelForm):
    class Meta:
        model = Arrendatario
        fields = ['direccion', 'telefono', 'mail']