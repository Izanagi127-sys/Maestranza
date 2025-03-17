from django import forms
from .models import *

class ProductoForm(forms.ModelForm):
    id_categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), label='Categoría')
    id_marca = forms.ModelChoiceField(queryset=Marca.objects.all(), label='Marca')
    ubicacion = forms.ChoiceField(choices=Producto.UBICACION_CHOICES, label='Ubicación')

    class Meta:
        model = Producto
        fields = ['nom_producto', 'modelo', 'descripcion', 'precio', 'stock', 'umbral_stock_bajo', 'id_categoria', 'id_marca', 'ubicacion', 'imagen']

class FiltroProductoForm(forms.Form):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False, label='Categoría')
    marca = forms.ModelChoiceField(queryset=Marca.objects.all(), required=False, label='Marca')
    precio_min = forms.IntegerField(required=False, label='Precio Mínimo')
    precio_max = forms.IntegerField(required=False, label='Precio Máximo')

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ['nombre', 'descripcion']

class AsignarEtiquetaForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), label='Producto')
    etiqueta = forms.ModelChoiceField(queryset=Etiqueta.objects.all(), label='Etiqueta')

class RestarStockForm(forms.ModelForm):
    cantidad = forms.IntegerField(label='Cantidad a restar', min_value=1)

    class Meta:
        model = Producto
        fields = ['cantidad']

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'email', 'direccion', 'giro', 'modalidad_pago', 'inhabilitado']
        widgets = {
            'modalidad_pago': forms.Select(choices=Proveedor.MODALIDAD_PAGO_CHOICES),
        }

class FiltroProveedorForm(forms.Form):
    MODALIDAD_PAGO_CHOICES = [
        ('', 'Todas'),
        ('Cheque', 'Cheque'),
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
    ]

    ESTADO_CHOICES = [
        ('', 'Todos'),
        (True, 'Inhabilitado'),
        (False, 'Habilitado')
    ]

    nombre = forms.CharField(max_length=100, required=False, label='Nombre del Proveedor')
    modalidad_pago = forms.ChoiceField(choices=MODALIDAD_PAGO_CHOICES, required=False, label='Modalidad de Pago')
    inhabilitado = forms.ChoiceField(choices=ESTADO_CHOICES, required=False, label='Estado')