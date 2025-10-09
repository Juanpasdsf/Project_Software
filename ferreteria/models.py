from django.db import models

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique = True)
    descripcion = models.TextField()

class Producto(models.Model):
    nombre = models.CharField(max_length= 100, unique=True)
    descripcion = models.TextField()
    precio = models.FloatField()
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

