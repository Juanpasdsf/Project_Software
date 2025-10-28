from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarritoViewSet, CategoriaViwSet, ProductoViewSet, CarritoProductoViewSet

router = DefaultRouter()
router.register(r'caategorias',CategoriaViwSet)
router.register(r'productos', ProductoViewSet)
router.register(r'carrito', CarritoViewSet, basename='carritos')
router.register(r'carrito-productos', CarritoProductoViewSet)

urlpatterns = [
    path('',include(router.urls))
]