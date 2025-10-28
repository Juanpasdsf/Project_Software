from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from .models import Categoria, Producto, Carrito, CarritoProducto, OrdenItem, Orden
from .serializers import CategoriaSerializer, ProductoSerializer, CarritoSerializer, CarritoProductoWriteSerializer, OrdenSerializer

# Create your views here.
class CategoriaViwSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAdminUser]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class= ProductoSerializer
    #Lectura para todos escritura solo para los admin
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    
    def get_queryset(self):
        return Carrito.objects.filter(user = self.request.user)
    
    def perform_create(self,serializer):#solo un carrito activo por usuario
        Carrito.objects.filter(user = self.request.user, activo = True).update(activo = False)
        serializer.save(user = self.request.user, activo = True) 
    
    @action (detail=False, methods=['gets'], permission_classes = [IsAuthenticated]) 
    def activo(self,request):
        carrito, _ =Carrito.objects.get_or_create(user = request.user, activo = True)
        return Response(self.get_serializer(carrito).data)    
    
    @action (detail=True, methods=['post'], permission_classes = [IsAuthenticated])
    def add_item(self, request, pk=None):
        carrito = self.get_object()
        ser = CarritoProductoWriteSerializer 
        ser.is_valid(raise_exception=True)
        prod = ser.validated_data['producto']
        cant = ser.validated_data['cantidad']
        item, created = CarritoProducto.objects.get_or_create(carrito=carrito, producto = prod, defaults = {'cantidad':cant})
        if not created:
            nueva = item.cantidad + cant
            if nueva > prod.stock:
                return Response({"detial" : "No hay stock suficiente"}, status=400)
            item.cantidad = nueva
            item.save(update_fields=['cantidad'])
        return Response(self.get_serializer(carrito).data, status=201)
    
    @action(detail=True, methods=['post'], permission_classes = [IsAuthenticated])
    def remove_item(self, request, pk=None):
        carrito = self.get_object()
        prod_id = request.data.get('producto')
        item = get_object_or_404(CarritoProducto, carrito = carrito, producto_id = prod_id)
        item.delete()
        return Response(self.get_serializer(carrito).data)
    
    @action(detail = True, methods=['post'], permission_classes = [IsAuthenticated])
    def clear(self, request, pk=None):
        carrito = self.get_object()
        carrito.items.all().delete()
        return Response(self.get_serializer(carrito).data)
    
    @action(detail=True, methods=['post'], permission_classes = [IsAuthenticated])
    def checkout(self, request, pk= None):
        carrito = self.get_object()
        if not carrito.item.exist():
            return Response({"detail":"El carrito esa vacio"}, status=400)
        
        #Crear orden
        orden = Orden.objects.create(user=request.user, total=carrito.total)
        alertas = []
        
        for it in carrito.items.select_related('producto'):
            OrdenItem.objects.create(
                orden = orden,
                producto = it.producto,
                cantidad = it.cantidad,
                precio_unitario = it.producto.precio
            )
            #Descontar stock
            it.producto.stock -= it.cantidad
            it.prodcuto.save(update_fields=['stock'])
            
            #Alerta si el stock es bajo
            if it.producto.stock < it.producto.stock_minimo:
                alertas.append({
                    "producto": it.produtco.nombre,
                    "stock": it.producto.stock,
                    "stock_minimo" : it.producto.stock_minimo
                })
        
        #Cerramos carrito y limpiamos los items
        carrito.activo = False
        carrito.items.all().delete()
        carrito.save(update_fields = ['activo'])
        
        data = OrdenSerializer(orden).data
        if alertas : 
            data["alertas_stock_bajo"] = alertas
        return Response(data, status=status.HTTP_201_CREATED)    

class CarritoProductoViewSet(viewsets.ModelViewSet):
    queryset = CarritoProducto.objects.all()
    http_method_names = ['get', 'head', 'options']