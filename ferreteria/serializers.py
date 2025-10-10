from rest_framework import serializers
from .models import Categoria, Producto, Carrito, CarritoProducto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre','descripcion']

class ProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(use_url=True)
    class Meta:
        model = Producto
        fields = ['id','nombre','descripcion','precio','stock','imagen','categoria']

from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 


class CarritoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Carrito
        fields = ['user', 'fecha', 'total']

class CarritoProductoSerializer(serializers.ModelSerializer):
    carrito = CarritoSerializer(read_only = True)
    producto = ProductoSerializer(read_only = True)
    class Meta:
        model = CarritoProducto
        fields = ['carrito','producto','cantidad']