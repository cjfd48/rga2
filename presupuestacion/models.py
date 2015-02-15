from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

class Proyecto(models.Model):
    nombre=models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    likes=models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre)
        super(Proyecto, self).save(*args, **kwargs)

    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.nombre
# Create your models here.

class Poste(models.Model):
    proyecto=models.ForeignKey(Proyecto)
    nombre=models.CharField(max_length=128)
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.proyecto.nombre+" - "+self.nombre

class Items(models.Model):
    descripcion=models.CharField(max_length=128, unique=True)
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.nombre

class ItemPorPoste(models.Model):
    poste=models.ForeignKey(Poste)
    item=models.ForeignKey(Items)
    cantidad=models.FloatField()
    def __str__(self):  #For Python 2, use __str__ on Python 3
        return self.cantidad #self.poste.nombre+" - "+self.item.descripcion


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    nombres=models.CharField(max_length=128)
    apellidos=models.CharField(max_length=128)
    direccion=models.CharField(max_length=128)
    telefono=models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        usern=(self.nombres[:1]+self.apellidos).lower().replace(' ','')
        self.user.username=usern
        self.user.set_password(usern)
        self.user.save()
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username