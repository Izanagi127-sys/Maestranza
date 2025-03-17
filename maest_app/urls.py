from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 
from django.urls import path
from .views import listar_informes

app_name = 'maest_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('reginventario/', views.registrar_inventario, name='reginventario'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('listar_alertas/', views.listar_alertas, name='listar_alertas'),
    path('asignar_etiqueta/', views.asignar_etiqueta, name='asignar_etiqueta'),
    path('editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('vista_comercio/', views.vista_comercio, name='vista_comercio'),
    path('crear_etiqueta/', views.crear_etiqueta, name='crear_etiqueta'),
    path('listar_etiquetas/', views.listar_etiquetas, name='listar_etiquetas'),
    path('editar_etiqueta/<int:etiqueta_id>/', views.editar_etiqueta, name='editar_etiqueta'),
    path('eliminar_etiqueta/<int:etiqueta_id>/', views.eliminar_etiqueta, name='eliminar_etiqueta'),
    path('alertas/', views.listar_alertas, name='listar_alertas'),
    path('notificaciones/', views.obtener_notificaciones, name='obtener_notificaciones'),
    path('obtener_notificaciones/', views.obtener_notificaciones, name='obtener_notificaciones'),
    path('marcar_notificacion_como_leida/', views.marcar_notificacion_como_leida, name='marcar_notificacion_como_leida'),
    path('regproveedor/', views.registrar_proveedor, name='regproveedor'),
    path('listar_proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('editar_proveedor/<int:proveedor_id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar_proveedor/<int:proveedor_id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('informe_tendencia/', views.generar_informe_tendencia, name='informe_tendencia'),
    path('generar_informes/', views.generar_informes, name='generar_informes'),
    path('informe_tendencia/', views.generar_informe_tendencia, name='informe_tendencia'),
    path('informe_niveles_stock/', views.generar_informe_niveles_stock, name='informe_niveles_stock'),
    path('exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('historial_precio_producto/<int:id>/', views.historial_precio_producto, name='historial_precio_producto'),
    path('listar_informes/', listar_informes, name='listar_informes'),
   

    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
