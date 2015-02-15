from django import forms
from django.contrib.auth.models import User
from presupuestacion.models import Proyecto,Poste, UserProfile


class ProyectoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=128, help_text="Por Favor Ingrese El Nombre del Proyecto")
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Proyecto
        fields = ('nombre',)


class PosteForm(forms.ModelForm):
    nombre = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    # url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    # views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Poste

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('proyecto',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nombres', 'apellidos')