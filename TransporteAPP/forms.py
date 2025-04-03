from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Residencia
from .models import ResidenciaImagen
from .models import Ruta, CupoDia
from .models import Solicitud
from .models import Calificacion

class CustomUserCreationForm(forms.ModelForm):  # Se usa ModelForm en lugar de UserCreationForm
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith('@ucundinamarca.edu.co'):
            raise ValidationError("Solo se permiten correos @ucundinamarca.edu.co")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if not password1:
            raise forms.ValidationError("Este campo es obligatorio.")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Guarda la contraseña correctamente
        if commit:
            user.save()
        return user
    
class ResidenciaForm(forms.ModelForm):
    class Meta:
        model = Residencia
        fields = ['titulo', 'descripcion', 'ubicacion']

class ResidenciaImagenForm(forms.ModelForm):
    class Meta:
        model = ResidenciaImagen
        fields = ['imagen']

class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ['title', 'description', 'vehiculo', 'cupos', 'usuario']
    

class CupoPorDiaForm(forms.ModelForm):
    class Meta:
        model = CupoDia
        fields = ['dia', 'hora_ida', 'hora_vuelta']

CupoPorDiaFormSet = forms.inlineformset_factory(Ruta, CupoDia, form=CupoPorDiaForm, extra=1, can_delete=True)

class AplicarRutaForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['dia', 'tipo_viaje']
        widgets = {
            'dia': forms.Select(attrs={'class': 'form-control'}),  # Asegúrate de que este campo sea adecuado para el tipo de dato
            'tipo_viaje': forms.Select(attrs={'class': 'form-control'}),
        }
        
class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['estrellas', 'comentario']
        widgets = {
            'estrellas': forms.RadioSelect(),
            'comentario': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        
from .models import Calificacion

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['estrellas', 'comentario']
        widgets = {
            'estrellas': forms.RadioSelect(),
            'comentario': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }