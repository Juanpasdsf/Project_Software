from django.shortcuts import render
from rest_framework import viewsets
from .models import Categoria, Producto, Carrito, CarritoProducto
from .serializers import CategoriaSerializer, ProductoSerializer, CarritoSerializer, CarritoProductoSerializer

# Create your views here.
class CategoriaViwSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class= ProductoSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class CarritoProductoViewSet(viewsets.ModelViewSet):
    queryset = CarritoProducto.objects.all()
    serializer_class = CarritoProductoSerializer