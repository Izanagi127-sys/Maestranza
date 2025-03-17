from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    UBICACION_CHOICES = [
        (f'{letter}{number}', f'{letter}{number}')
        for letter in 'ABCDEFGHIJ'
        for number in range(1, 6)
    ]

    sku = models.CharField(max_length=20, blank=True, null=True)
    nom_producto = models.CharField(max_length=60)
    modelo = models.CharField(max_length=20, blank=True, null=True)
    descripcion = models.TextField(max_length=400, blank=True, null=True)
    precio = models.IntegerField()
    stock = models.IntegerField()
    umbral_stock_bajo = models.IntegerField(default=10)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=3, choices=UBICACION_CHOICES, default='A1')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nom_producto

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre

class ProductoEtiqueta(models.Model):
    id_prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id_prod', 'id_etiqueta'),)

class AlertaStockBajo(models.Model):
    id_prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_alerta = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    stock_actual = models.IntegerField()

    def __str__(self):
        return f'Alerta: {self.id_prod.nom_producto} - {self.stock_actual}'

class Proveedor(models.Model):
    MODALIDAD_PAGO_CHOICES = [
        ('Cheque', 'Cheque'),
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
    ]

    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    giro = models.CharField(max_length=400, blank=True, null=True)
    modalidad_pago = models.CharField(max_length=20, choices=MODALIDAD_PAGO_CHOICES, default='Efectivo')
    inhabilitado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    


class HistorialPrecios(models.Model):
    producto = models.ForeignKey(Producto, related_name='precios', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nom_producto} - {self.fecha} - {self.precio}"
    
    # models.py
from django.db import models

class Informe(models.Model):
    nombre_archivo = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='informes/')
