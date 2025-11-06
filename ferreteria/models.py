from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

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
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    stock_minimo = models.PositiveIntegerField(default=5)
    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='carritos')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    activo = models.BooleanField(default=True)
    def __str__(self):
        return f"Carrito de {self.user.username} - {self.fecha:%Y-%m-%d %H:%M}"
    def calcular_total(self):
        items = self.carritoproducto_set.all()
        total = sum(item.producto.precio * item.cantidad for item in items)
        return total
    
    @property
    def total(self):
        return self.calcular_total()

    def __str__(self):
        return f"Carrito de {self.user.username} - ${self.total}"

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito,on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE, related_name='en_carritos')
    cantidad = models.PositiveIntegerField()
    class Meta:
        unique_together = ('carrito', 'producto')
    
    def subtotal(self):
        return self.producto.precio * self.cantidad
    def __str__(self):
        return f"Carrito de {self.cantidad} - {self.producto.nombre} (Carrito #{self.carrito.id})"

class Orden(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'ordenes')
    fecha = models.DateTimeField(auto_now_add= True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    def __str__(self):
        return f"Orden #{self.id} - {self.user.username} - {self.fecha:%Y-%m-%d}"

class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places = 2)
    def subtotal(self):
        return self.precio_unitario * self.cantidad
