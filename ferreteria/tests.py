from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Categoria, Producto, Carrito, CarritoProducto
from .serializers import CategoriaSerializer, ProductoSerializer, CarritoSerializer
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
import json

#pruebas para los modelos
class ModelTests(TestCase):
    def setUp(self): #configuracion inicial para todas las pruebas
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.categoria = Categoria.objects.create(
            nombre='Herramientas',
            descripcion='Herramientas de construcción'
        )
        
        # Crear una imagen temporal para pruebas
        self.image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        
        self.producto = Producto.objects.create(
            nombre='Martillo',
            descripcion='Martillo de acero',
            precio=25.50,
            stock=10,
            imagen=self.image,
            categoria=self.categoria
        )
        
        self.carrito = Carrito.objects.create(
            user=self.user
        )

    def test_creacion_categoria(self): #prueba la creacion de una categoria
        self.assertEqual(self.categoria.nombre, 'Herramientas')
        self.assertEqual(self.categoria.descripcion, 'Herramientas de construcción')
        self.assertTrue(self.categoria.activo)
        self.assertEqual(str(self.categoria), 'Herramientas')

    def test_creacion_producto(self): #prueba la creacion de un producto
        self.assertEqual(self.producto.nombre, 'Martillo')
        self.assertEqual(self.producto.precio, 25.50)
        self.assertEqual(self.producto.stock, 10)
        self.assertEqual(self.producto.categoria, self.categoria)
        self.assertTrue(self.producto.activo)
        self.assertIn('Martillo', str(self.producto))

    def test_creacion_carrito(self): #prueba la creacion de un carrito
        self.assertEqual(self.carrito.user, self.user)
        self.assertTrue(self.carrito.activo)
        self.assertIsNotNone(self.carrito.fecha_creacion)
        self.assertIn('testuser', str(self.carrito))

    def test_carrito_total_calculation(self): #prueba el calculo automatico del total del carrito
        # Crear items en el carrito
        CarritoProducto.objects.create(
            carrito=self.carrito,
            producto=self.producto,
            cantidad=2
        )
        
        producto2 = Producto.objects.create(
            nombre='Destornillador',
            descripcion='Destornillador plano',
            precio=15.00,
            stock=5,
            categoria=self.categoria
        )
        
        CarritoProducto.objects.create(
            carrito=self.carrito,
            producto=producto2,
            cantidad=1
        )
        
        total_esperado = (25.50 * 2) + (15.00 * 1)
        self.assertEqual(self.carrito.total, total_esperado)

    def test_carritoproducto_subtotal(self):#prueba la funcion del subtotal del carrito
        carrito_producto = CarritoProducto.objects.create(
            carrito=self.carrito,
            producto=self.producto,
            cantidad=3
        )
        
        subtotal_esperado = 25.50 * 3
        self.assertEqual(carrito_producto.subtotal(), subtotal_esperado)

    def test_producto_stock_validation(self): #prueba que no se cree un stock negativo
        with self.assertRaises(Exception):
            Producto.objects.create(
                nombre='Producto Inválido',
                descripcion='Test',
                precio=10.00,
                stock=-5,  # Stock negativo debería fallar
                categoria=self.categoria
            )



# Create your tests here.
