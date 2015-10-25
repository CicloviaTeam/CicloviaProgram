# coding=utf-8
from django import forms
from models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class UploadForm(forms.Form):
    filename = forms.CharField(max_length=100, label='Nombre del archivo')
    docfile = forms.FileField(
        label='Selecciona un archivo'
    )

class NewUserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ('username','email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def clean_username(self):
        if len(User.objects.filter(username=self.cleaned_data['username'])) is not 0:
            raise forms.ValidationError(_('user already exists.'),code='used username')

        return self.cleaned_data['username']

    def clean_email(self):
        if len(User.objects.filter(email=self.cleaned_data['email'])) is not 0:
            raise forms.ValidationError(_('email already exists.'),code='used email')
        elif self.cleaned_data['email'] == '':
            raise forms.ValidationError(_('This field is required.'),code='empty email')

        return self.cleaned_data['email']

# Change user values.
class UserChangeFormUniqueEmail(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name','email']

# Form to modify a ciclovia.
class cicloviaForm(forms.ModelForm):
    class Meta:
        model=Ciclovia
        fields=['user','name','place','start_hour','end_hour','num_tracks']



