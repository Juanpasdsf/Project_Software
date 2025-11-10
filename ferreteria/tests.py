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

# Create your tests here.
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

#pruebas para los serializadores
class SerializerTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='Electricidad',
            descripcion='Productos eléctricos'
        )
        
        self.producto_data = {
            'nombre': 'Cable Eléctrico',
            'descripcion': 'Cable de cobre 2.5mm',
            'precio': 45.00,
            'stock': 20,
            'categoria': self.categoria.id
        }
    def test_categoria_serializer(self): #se hace las pruebas del serializador de categorias
        serializer = CategoriaSerializer(instance=self.categoria)
        data = serializer.data
        
        self.assertEqual(data['nombre'], 'Electricidad')
        self.assertEqual(data['descripcion'], 'Productos eléctricos')
        self.assertTrue(data['activo'])

    def test_producto_serializer_valid_data(self):#prueba el serializador de productos con datos validos
        serializer = ProductoSerializer(data=self.producto_data)
        self.assertTrue(serializer.is_valid())

    def test_producto_serializer_invalid_data(self):#se prueba el serializador con datos invalidos
        invalid_data = self.producto_data.copy()
        invalid_data['precio'] = -10.00  # Precio negativo
        
        serializer = ProductoSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('precio', serializer.errors)
            



# fin de las pruebas.

# Ejecutar todas las pruebas
python manage.py test

# Ejecutar pruebas específicas
python manage.py test ferreteria.tests.ModelTests
python manage.py test ferreteria.tests.APITests
python manage.py test ferreteria.tests.IntegrationTests

# Ejecutar con verbosidad aumentada
python manage.py test -v 2

# Ejecutar pruebas y generar reporte de cobertura
coverage run manage.py test
coverage report
