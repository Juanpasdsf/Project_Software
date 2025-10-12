from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarritoViewSet, CategoriaViwSet, ProductoViewSet, CarritoProductoViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViwSet)
router.register(r'productos', ProductoViewSet)
router.register(r'carrito', CarritoViewSet)
router.register(r'carrito-productos', CarritoProductoViewSet)

urlpatterns = [
    path('',include(router.urls))
]