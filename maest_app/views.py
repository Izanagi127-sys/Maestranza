from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import *
from .forms import *
from django.http import JsonResponse
import json
from django.http import HttpResponse
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import F
from django.urls import reverse

def home(request):
    return render(request, 'maest_app/home.html')

def registrar_inventario(request):
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('maest_app:reginventario') + '?success=true')
    else:
        form = ProductoForm()
    
    success = request.GET.get('success', False)
    return render(request, 'maest_app/reginventario.html', {'form': form, 'marcas': marcas, 'categorias': categorias, 'success': success})

def listar_productos(request):
    productos = Producto.objects.all()
    form = FiltroProductoForm(request.GET or None)

    if form.is_valid():
        if form.cleaned_data['categoria']:
            productos = productos.filter(id_categoria=form.cleaned_data['categoria'])
        if form.cleaned_data['marca']:
            productos = productos.filter(id_marca=form.cleaned_data['marca'])
        if form.cleaned_data['precio_min'] is not None:
            productos = productos.filter(precio__gte=form.cleaned_data['precio_min'])
        if form.cleaned_data['precio_max'] is not None:
            productos = productos.filter(precio__lte=form.cleaned_data['precio_max'])

    productos_etiquetas = ProductoEtiqueta.objects.select_related('id_prod', 'id_etiqueta')
    
    for producto in productos:
        producto.etiquetas = [pe.id_etiqueta for pe in productos_etiquetas if pe.id_prod == producto]
        if producto.stock >= producto.umbral_stock_bajo * 2:
            producto.stock_status = 'success'
        elif producto.stock > producto.umbral_stock_bajo:
            producto.stock_status = 'warning'
        else:
            producto.stock_status = 'danger'

    return render(request, 'maest_app/listar_productos.html', {
        'productos': productos,
        'form': form
    })

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            nuevo_precio = form.cleaned_data['precio']
            form.save()

            # Guardar el historial de precios
            HistorialPrecios.objects.create(
                producto=producto,
                precio=nuevo_precio
            )

            return redirect('maest_app:listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'maest_app/editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        producto.delete()
        return redirect('maest_app:listar_productos')
    return redirect('maest_app:listar_productos')

def vista_comercio(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        producto = get_object_or_404(Producto, id=producto_id)
        form = RestarStockForm(request.POST, instance=producto)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            producto.stock -= cantidad
            producto.save()
            return redirect('maest_app:vista_comercio')
    else:
        form = RestarStockForm()
    return render(request, 'maest_app/vista_comercio.html', {'productos': productos, 'form': form})

def asignar_etiqueta(request):
    if request.method == "POST":
        form = AsignarEtiquetaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            etiqueta = form.cleaned_data['etiqueta']
            ProductoEtiqueta.objects.create(id_prod=producto, id_etiqueta=etiqueta)
            return redirect('maest_app:listar_productos')
    else:
        form = AsignarEtiquetaForm()
    return render(request, 'maest_app/asignar_etiqueta.html', {'form': form})

def crear_etiqueta(request):
    if request.method == "POST":
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maest_app:listar_etiquetas')
    else:
        form = EtiquetaForm()
    return render(request, 'maest_app/crear_etiqueta.html', {'form': form})

def listar_etiquetas(request):
    etiquetas = Etiqueta.objects.all()
    return render(request, 'maest_app/listar_etiquetas.html', {'etiquetas': etiquetas})


def editar_etiqueta(request, etiqueta_id):
    etiqueta = get_object_or_404(Etiqueta, id=etiqueta_id)
    if request.method == "POST":
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            return redirect('maest_app:listar_etiquetas')
    else:
        form = EtiquetaForm(instance=etiqueta)
    return render(request, 'maest_app/editar_etiqueta.html', {'form': form})

def eliminar_etiqueta(request, etiqueta_id):
    etiqueta = get_object_or_404(Etiqueta, id=etiqueta_id)
    if request.method == "POST":
        etiqueta.delete()
        return redirect('maest_app:listar_etiquetas')
    return redirect('maest_app:listar_etiquetas')

def listar_alertas(request):
    alertas = AlertaStockBajo.objects.all().order_by('-fecha_alerta')
    return render(request, 'maest_app/listar_alertas.html', {'alertas': alertas})

def obtener_notificaciones(request):
    alertas = AlertaStockBajo.objects.filter(leido=False)
    data = [{
        'id': alerta.id,
        'id_prod': {
            'nom_producto': alerta.id_prod.nom_producto,
            'sku': alerta.id_prod.sku,
        },
        'stock_actual': alerta.stock_actual,
    } for alerta in alertas]

    return JsonResponse(data, safe=False)

@require_POST
def marcar_notificacion_como_leida(request):
    data = json.loads(request.body)
    alerta_id = data.get('id')
    try:
        alerta = AlertaStockBajo.objects.get(id=alerta_id)
        alerta.leido = True
        alerta.save()
        return JsonResponse({'success': True})
    except AlertaStockBajo.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

def obtener_conteo_notificaciones(request):
    conteo = AlertaStockBajo.objects.filter(leido=False).count()
    return JsonResponse({'conteo': conteo})

def registrar_proveedor(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('maest_app:regproveedor') + '?success=true')
    else:
        form = ProveedorForm()
    
    success = request.GET.get('success', False)
    return render(request, 'maest_app/regproveedor.html', {'form': form, 'success': success})
def listar_proveedores(request):
    form = FiltroProveedorForm(request.GET)
    proveedores = Proveedor.objects.all()

    if form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        modalidad_pago = form.cleaned_data.get('modalidad_pago')
        inhabilitado = form.cleaned_data.get('inhabilitado')

        if nombre:
            proveedores = proveedores.filter(nombre__icontains=nombre)
        if modalidad_pago:
            proveedores = proveedores.filter(modalidad_pago=modalidad_pago)
        if inhabilitado in [True, False]:
            proveedores = proveedores.filter(inhabilitado=inhabilitado)

    context = {
        'form': form,
        'proveedores': proveedores,
    }
    return render(request, 'maest_app/listar_proveedores.html', context)


def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('maest_app:listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'maest_app/editar_proveedor.html', {'form': form, 'proveedor': proveedor})

def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == "POST":
        proveedor.delete()
        return redirect('maest_app:listar_proveedores')
    return redirect('maest_app:listar_proveedores')

def generar_informe_tendencia(request):
    # Simulación de datos de consumo
    productos = Producto.objects.all()
    data = {
        'Producto': [],
        'Consumo': [],
        'Mes': []
    }
    
    for producto in productos:
        for mes in range(1, 13):
            data['Producto'].append(producto.nom_producto)
            data['Consumo'].append(producto.stock - (producto.stock // (mes + 1)))  # Simulación de consumo
            data['Mes'].append(f'Mes {mes}')
    
    df = pd.DataFrame(data)
    
    # Gráfico de tendencia de consumo
    plt.figure(figsize=(10, 5))
    for producto in df['Producto'].unique():
        plt.plot(df[df['Producto'] == producto]['Mes'], df[df['Producto'] == producto]['Consumo'], label=producto)
    plt.xlabel('Mes')
    plt.ylabel('Consumo')
    plt.title('Tendencia de Consumo')
    plt.legend()
    plt.tight_layout()
    
    # Convertir gráfico a imagen base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'maest_app/informe_tendencia.html', {'graphic': graphic})

def exportar_pdf(request):
    productos = Producto.objects.all()
    template_path = 'maest_app/informe_pdf.html'
    context = {'productos': productos}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF: %s' % pisa_status.err, status=400)
    return response

def exportar_excel(request):
    productos = Producto.objects.all().values('nom_producto', 'stock', 'precio', 'ubicacion')
    df = pd.DataFrame(productos)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="informe.xlsx"'
    df.to_excel(response, index=False)
    return response

def generar_informe_niveles_stock(request):
    productos = Producto.objects.filter(stock__lte=F('umbral_stock_bajo'))
    return render(request, 'maest_app/informe_niveles_stock.html', {'productos': productos})

def generar_informes(request):
    return render(request, 'maest_app/generar_informes.html')

# views.py
import pandas as pd
import plotly.express as px
from django.shortcuts import render, get_object_or_404
from .models import Producto
import plotly.graph_objects as go

def historial_precio_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    data = {
        'Producto': [],
        'Precio': [],
        'Fecha': []
    }

    for historial in producto.precios.all():
        data['Producto'].append(producto.nom_producto)
        data['Precio'].append(historial.precio)
        data['Fecha'].append(historial.fecha)
    
    df = pd.DataFrame(data)
    
    # Asegurarse de que la columna 'Fecha' es de tipo datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    # Ordenar los datos por fecha
    df.sort_values('Fecha', inplace=True)
    
    # Gráfico de historial de precios utilizando Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Precio'],
                             mode='lines+markers',
                             name=producto.nom_producto,
                             line=dict(color='blue', width=2),
                             marker=dict(size=8)))
    
    fig.update_layout(title=f'Historial de Precios para {producto.nom_producto}',
                      xaxis_title='Fecha',
                      yaxis_title='Precio',
                      hovermode='x unified')
    
    # Convertir el gráfico a HTML
    graph_html = fig.to_html(full_html=False)
    
    return render(request, 'maest_app/historial_precio.html', {'graph_html': graph_html, 'producto': producto})

# views.py

def listar_informes(request):
    informes = Informe.objects.all().order_by('-fecha_creacion')
    return render(request, 'maest_app/listar_informes.html', {'informes': informes})
