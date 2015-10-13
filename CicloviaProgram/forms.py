from django import forms

class UploadForm(forms.Form):
    filename = forms.CharField(max_length=100, label='Nombre del archivo')
    docfile = forms.FileField(
        label='Selecciona un archivo'
    )

# class NewUserForm(forms.Form):
#     username = forms.CharField(max_length=100, label='Nombre de usuario')
# ##    email = forms.EmailField(label='Correo electronico')
#     password = forms.CharField(label='Contrasena')

