from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from .models import *

def report_view(request):
    categoria_reporte = request.GET.get('categoria_reporte', 'default_categoria')
    tipo_reporte = request.GET.get('tipo_reporte', 'default_tipo')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data_type = data.get('data_type')
            
            # Para propósitos de depuración, podemos imprimir el data_type recibido
            print("Received data_type:", data_type)
            
            if data_type:
                print('Hola desde el data type y el handle')
                return handle_data(request, data_type)    
            else:            
                # Retornar el data_type en la respuesta JSON como prueba
                response_data = {
                    'status': 'success',
                    'data_type': data_type,
                }
                return JsonResponse(response_data)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:    
        context = {
            'categoria_reporte': categoria_reporte,
            'tipo_reporte': tipo_reporte,
        }
        return render(request, 'informes/reportes.html', context)


# Función para manejar datos según el tipo recibido
def handle_data(request, data_type):
    # Verifica si el tipo de dato está en el diccionario data_type_handlers
    if data_type in data_type_handlers:
        # Llama a la función de manejo correspondiente con los parámetros necesarios
        return data_type_handlers[data_type](request, data_type)
    else:
        # Manejo para tipo de dato no reconocido, por ejemplo, retornar un error
        return JsonResponse({'error': f'Tipo de dato no reconocido: {data_type}'}, status=400)

def handle_cliente(request,data_type):
    clientes = Kdud.objects.values('clave_cliente', 'nombre_cliente').distinct().order_by('clave_cliente')
    clientes_paginados  = objPaginator(request, clientes);
    
    response_data = {
        'data_type': data_type,
        'clientes' : list(clientes),
        'clientesPaginados': clientes_paginados ,
    }
    
    return JsonResponse(response_data) 

def handle_producto(request, data_type):
    productos = Kdii.objects.values('clave_producto', 'descripcion_producto', 'linea_producto').distinct().order_by('clave_producto')
    productos_paginados = objPaginator(request, productos)
    
    response_data = {
        'data_type': data_type,
        'productos' : list(productos),
        'productosPaginados': productos_paginados ,
    }
    
    return JsonResponse(response_data) 

def handle_sucursal(request, data_type):
    sucursales = Kdms.objects.values('clave_sucursal', 'descripcion').distinct().order_by('clave_sucursal')
    sucursales_paginados = objPaginator(request, sucursales)
    
    response_data = {
        'data_type': data_type,
        'sucursales' : list(sucursales),
        'sucursalesPaginados': sucursales_paginados ,
    }
    
    return JsonResponse(response_data) 
    
def handle_vendedor(request):
    return 0

def handle_linea(request):
    return 0
    
def handle_familia(request):
    return 0

def handle_marca(request):
    return 0
    
def handle_grupo_corporativo(request):
    return 0

def handle_segmento(request):
    return 0

def handle_status(request):
    return 0

def handle_zona(request):
    return 0

def handle_grupo(request):
    return 0

def handle_region(request):
    return 0
    
    
data_type_handlers = {
    'cliente_inicial': handle_cliente,
    'cliente_final': handle_cliente,
    'producto_inicial': handle_producto,
    'producto_final': handle_producto,
    'sucursal_inicial': handle_sucursal,
    'sucursal_final': handle_sucursal,
    'vendedor_inicial': handle_vendedor,
    'vendedor_final': handle_vendedor,
    'linea_inicial': handle_linea,
    'linea_final': handle_linea,
    'familia_inicial': handle_familia,
    'familia_final': handle_familia,
    'marca_inicial': handle_marca,
    'marca_final': handle_marca,
    'grupoCorporativo_inicial': handle_grupo_corporativo,
    'grupoCorporativo_final': handle_grupo_corporativo,
    'grupoCorporativo': handle_grupo_corporativo,
    'segmento_inicial': handle_segmento,
    'segmento_final': handle_segmento,
    'status': handle_status,
    'zona': handle_zona,
    'sucursal': handle_sucursal,
    'grupo': handle_grupo,
    'familia': handle_familia,
    'region': handle_region,
}

def objPaginator(request, obj_to_paginate):
    paginator = Paginator(obj_to_paginate, 10)
    page_number = request.GET.get('page')
    query_page = paginator.get_page(page_number)
    objList = list(query_page)
    
    pagination_data = {
        'objList': objList,
        'pagination_info': get_pagination_html(query_page),
    }
    
    return pagination_data

def get_pagination_html(page_obj):
    return {
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'number': page_obj.number,
        'num_pages': page_obj.paginator.num_pages,
    }
    
# def get_parametros(post_data):
#     fields_to_extract = [
#         'fecha_inicial', 'fecha_final', 'sucursal', 'cliente_inicial', 'cliente_final',
#         'producto_inicial', 'producto_final', 'sucursal_inicial', 'sucursal_final',
#         'vendedor_inicial', 'vendedor_final', 'linea_inicial', 'linea_final',
#         'familia_inicial', 'familia_final', 'marca_inicial', 'marca_final',
#         'grupoCorporativo_inicial', 'grupoCorporativo_final', 'grupoCorporativo',
#         'segmento_inicial', 'segmento_final', 'status', 'zona', 'sucursal', 'grupo',
#         'familia', 'region',
#     ]

#     extracted_data = {field: post_data.get(field, None) for field in fields_to_extract}
#     return extracted_data