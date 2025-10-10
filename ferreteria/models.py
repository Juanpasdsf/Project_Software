from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique = True)
    descripcion = models.TextField()
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length= 100, unique=True)
    descripcion = models.TextField()
    precio = models.FloatField()
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    def __str__(self):
        return f"Carrito de {self.user.username} - {self.fecha}"


class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    def __str__(self):
        return f"Carrito de {self.user.username} - {self.fecha}"
