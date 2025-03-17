from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Producto, AlertaStockBajo

@receiver(post_save, sender=Producto)
def generar_sku(sender, instance, created, **kwargs):
    if created:
        # Generar SKU
        sku = (
            instance.nom_producto[:4].upper() +
            instance.id_marca.nombre[:3].upper() +
            str(instance.id)
        )
        instance.sku = sku
        instance.save()

@receiver(post_save, sender=Producto)
def verificar_stock_bajo(sender, instance, **kwargs):
    if instance.stock < instance.umbral_stock_bajo:
        AlertaStockBajo.objects.create(id_prod=instance, stock_actual=instance.stock)
