from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CarritoProducto, Carrito, Producto

def _recalcular_total(carrito):
    total = sum(cp.producto.precio * cp.cantidad
                for cp in carrito.items.select_related('producto'))
    carrito.total = total
    carrito.save(update_fields=['total'])
    
@receiver(post_save, sender=CarritoProducto)
def carrito_item_saved(sender, instance, **kwargs):
    _recalcular_total(instance.carrito)

@receiver(post_delete, sender=CarritoProducto)
def carrito_item_deleted(sender, instance, **kwargs):
    _recalcular_total(instance.carrito)
