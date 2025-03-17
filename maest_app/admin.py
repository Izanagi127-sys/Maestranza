from django.contrib import admin
from .models import Categoria, Marca, Producto, Etiqueta, ProductoEtiqueta, AlertaStockBajo,HistorialPrecios

# Registrar modelos en el admin
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Producto)
admin.site.register(Etiqueta)
admin.site.register(ProductoEtiqueta)
admin.site.register(AlertaStockBajo)
admin.site.register(HistorialPrecios)
