from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from .models import *

def report_view(request):
    categoria_reporte = request.GET.get('categoria_reporte', 'default_categoria')
    tipo_reporte = request.GET.get('tipo_reporte', 'default_tipo')
    
    clientes = Kdud.objects.values('clave_cliente', 'nombre_cliente').distinct().order_by('clave_cliente')
    
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    clients_page = paginator.get_page(page_number)
    
    clients_list = list(clients_page)
    
    if request.method == 'POST':
        try:
            jsonData = json.loads(request.body)
            
            return JsonResponse({
                'Clientes': clients_list,
                'Pagination': get_pagination_html(clients_page),  # Aquí envías los datos de paginación
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    context = {
        'clients': clients_page,
        'categoria_reporte': categoria_reporte,
        'tipo_reporte': tipo_reporte,
    }
    return render(request, 'informes/reportes.html', context)

def get_pagination_html(page_obj):
    # Esta función obtiene los datos de paginación para enviar al frontend
    pagination_html = {
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'number': page_obj.number,
        'num_pages': page_obj.paginator.num_pages,
    }
    return pagination_html

def get_parametros(post_data):
    # Función para extraer parámetros específicos del formulario POST
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

#Corregir 
def sucursales_view(request):
    sucursales = Kdms.objects.values('clave_sucursal', 'descripcion').distinct().order_by('clave_sucursal')
    paginator = Paginator(sucursales, 20)  # 20 items por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.is_ajax():
        return render(request, 'informes/sucursales_list.html', {'page_obj': page_obj})

    return render(request, 'informes/sucursales_popup.html', {'page_obj': page_obj})

