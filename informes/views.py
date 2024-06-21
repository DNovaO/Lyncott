from django.shortcuts import render
from .models import *

def report_view(request):
    categoria_reporte = request.GET.get('categoria_reporte')
    tipo_reporte = request.GET.get('tipo_reporte')

    if request.method == 'POST':
        post_data = get_parametros(request.POST)

        context = {
            **post_data,
            'categoria_reporte': categoria_reporte,
            'tipo_reporte': tipo_reporte,
            'sucursales': get_sucursales(),
            'clientes': get_clientes(),
        }
        return render(request, 'informes/reportes.html', context)
    else:
        context = {
            'categoria_reporte': categoria_reporte,
            'tipo_reporte': tipo_reporte,
            'sucursales': get_sucursales(),
            'clientes': get_clientes(),
        }
        return render(request, 'informes/reportes.html', context)

def get_parametros(post_data):
    fields_to_extract = [
        'fecha_inicial', 'fecha_final', 'sucursal', 'cliente_inicial', 'cliente_final',
        'producto_inicial', 'producto_final', 'sucursal_inicial', 'sucursal_final',
        'vendedor_inicial', 'vendedor_final', 'linea_inicial', 'linea_final',
        'familia_inicial', 'familia_final', 'marca_inicial', 'marca_final',
        'grupoCorporativo_inicial', 'grupoCorporativo_final', 'grupoCorporativo',
        'segmento_inicial', 'segmento_final', 'status', 'zona', 'sucursal', 'grupo',
        'familia', 'region',
    ]

    extracted_data = {field: post_data.get(field, None) for field in fields_to_extract}
    return extracted_data

def get_sucursales():
    sucursales = Kdms.objects.values('clave_sucursal', 'descripcion').distinct().order_by('clave_sucursal')
    return sucursales

#Optimizacion de consultas, paginacion, indexado y asincronia
def get_clientes():
    clientes = Kdud.objects.values('clave_cliente', 'nombre_cliente').distinct().order_by('clave_cliente')
    return clientes
