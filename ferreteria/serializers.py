from rest_framework import serializers
from .models import Categoria, Producto, Carrito, CarritoProducto, Orden, OrdenItem
from django.contrib.auth.models import User

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id','nombre','descripcion']

class ProductoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(use_url=True)
    class Meta:
        model = Producto
        fields = ['id','nombre','descripcion','precio','stock','stock_minimo','imagen','categoria']
    
    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puedo ser negativo")
        return value
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email'] 

class CarritoProductoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoProducto
        field = ['id', 'producto', 'cantidad']
    
    def validate(self, data):
        producto = data['producto']
        cantidad = data['cantidad']
        if cantidad <= 0:
            raise serializers.ValidationError("La cantidad debe de ser mayor que 0")
        if cantidad > producto.stock:
            raise serializers.ValidationError("No hay stock suficiente")
        return data

class CarritoProductoReadSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only = True)
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = CarritoProducto
        field = ['id','producto','cantidad','subtotal']    
    
    def get_subtotal(self,obj):
        return obj.subtotal()

class CarritoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = CarritoProductoReadSerializer(many =True, read_only = True)
    class Meta:
        model = Carrito
        fields = ['id','user', 'fecha', 'total','activo', 'items']

class OrdenItemSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only = True)
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = OrdenItem
        fields = ['producto','cantidad','precio_unitario', 'subtotal']
    def get_subtotal(self,obj):
        return obj.subtotal()

class OrdenSerializer(serializers.ModelSerializer):
    items = OrdenItemSerializer(many = True, read_only = True)
    class Meta:
        model = Orden
        fields = ['id','fecha','total','items']      