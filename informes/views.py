from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from .models import *
from .queries import *

def report_view(request):
    categoria_reporte = request.GET.get('categoria_reporte', 'default_categoria')
    tipo_reporte = request.GET.get('tipo_reporte', 'default_tipo')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parsea el cuerpo JSON de la solicitud
            data_type = data.get('data_type')
            selected_item = data.get('selected_item')
            fecha_inicial = data.get('fecha_inicial')
            fecha_final = data.get('fecha_final')
            
            # Ejemplo de impresión para demostración
            print("Received data_type:", data_type)
            print("Selected item:", selected_item)

            # Ejemplo de impresión para demostración
            print("Received data_type:", data_type)
            printAllSelectedItems(selected_item)
            
            if data_type:
                return handle_data(request, data_type)    
            else:            
                # Retornar el data_type en la respuesta JSON como prueba
                response_data = {
                    'status': 'success',
                    'data_type': data_type,
                }
                return JsonResponse(response_data)
        
        except json.JSONDecodeError as e:
            return JsonResponse({'error': str(e)}, status=400)
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
    
def handle_vendedor(request, data_type):
    vendedores = Kduv.objects.values('clave_vendedor','nombre_vendedor').distinct().order_by('clave_vendedor')
    vendedores_paginados = objPaginator(request, vendedores)
    
    response_data = {
        'data_type': data_type,
        'vendedores' : list(vendedores),
        'vendedoresPaginados': vendedores_paginados,
    }
    
    return JsonResponse(response_data)

def handle_linea(request, data_type):
    lineas = Kdig.objects.values('clave_linea','descripcion_linea').distinct().order_by('clave_linea')
    lineas_paginados = objPaginator(request, lineas)
    
    response_data = {
        'data_type': data_type,
        'lineas' : list(lineas),
        'lineasPaginados': lineas_paginados,
    }
    
    return JsonResponse(response_data)
    
def handle_familia(request, data_type):
    familias = Kdif.objects.values('clave_grupo','descripcion_grupo').distinct().order_by('clave_grupo')
    familias_paginados = objPaginator(request, familias)
    
    response_data = {
        'data_type': data_type,
        'familias' : list(familias),
        'familiasPaginados': familias_paginados,
    }
    
    return JsonResponse(response_data)

def handle_grupo_corporativo(request, data_type):
    gruposCorporativos = Kdcorpo.objects.values('clave_corporativo', 'descripcion_corporativo').distinct().order_by('clave_corporativo')
    gruposCorporativos_paginados = objPaginator(request, gruposCorporativos)
    
    response_data = {
        'data_type': data_type,
        'gruposCorporativos' : list(gruposCorporativos),
        'gruposCorporativosPaginados': gruposCorporativos_paginados,
    }
    
    return JsonResponse(response_data)


def handle_segmento(request, data_type):
    segmentos = Kdsegmentacion.objects.values('clave_segmentacion', 'descripcion_segmentacion').distinct().order_by('clave_segmentacion')
    segmentos_paginados = objPaginator(request, segmentos)
    
    response_data = {
        'data_type': data_type,
        'segmentos' : list(segmentos),
        'segmentosPaginados': segmentos_paginados,
    }
    
    return JsonResponse(response_data)


def handle_status(request, data_type):
    estatus = Kdpord.objects.values('estatus').distinct().order_by('estatus')
    
    # Mapeo de valores
    status_map = {
        'A': 'Activo',
        'I': 'Inactivo'
    }
    
    # Transformar los valores de estatus
    estatus_transformed = [{'estatus': status_map.get(item['estatus'], item['estatus'])} for item in estatus]
    
    estatus_paginados = objPaginator(request, estatus_transformed)
    
    response_data = {
        'data_type': data_type,
        'estatus': estatus_transformed,
        'estatusPaginados': estatus_paginados,
    }
    
    return JsonResponse(response_data)

def handle_zona(request, data_type):

    zonas = [
        {
            'zona': 'CENTRO',
            'sucursales': [
                {'clave_sucursal': '02', 'descripcion': 'Mexico Vallejo'},
                {'clave_sucursal': '03', 'descripcion': 'Guadalajara'},
                {'clave_sucursal': '04', 'descripcion': 'Monterrey'},
                {'clave_sucursal': '05', 'descripcion': 'Queretaro'},
                {'clave_sucursal': '08', 'descripcion': 'Puebla'},
                {'clave_sucursal': '10', 'descripcion': 'Acapulco'},
                {'clave_sucursal': '11', 'descripcion': 'Villahermosa'},
                {'clave_sucursal': '12', 'descripcion': 'Culiacan'},
                {'clave_sucursal': '13', 'descripcion': 'Veracruz'},
                {'clave_sucursal': '15', 'descripcion': 'Aguascalientes'},
                {'clave_sucursal': '16', 'descripcion': 'Toluca'},
            ]
        },
        {
            'zona': 'PENINSULA',
            'sucursales': [
                {'clave_sucursal': '07', 'descripcion': 'Cancun'},
                {'clave_sucursal': '18', 'descripcion': 'Merida'},
            ]
        },
        {
            'zona': 'PACIFICO',
            'sucursales': [
                {'clave_sucursal': '06', 'descripcion': 'Hermosillo'},
                {'clave_sucursal': '09', 'descripcion': 'Tijuana'},
                {'clave_sucursal': '14', 'descripcion': 'Los Cabos'},
                {'clave_sucursal': '20', 'descripcion': 'Puerto Vallarta'},
            ]
        },
        {
            'zona': 'CHIHUAHUA',
            'sucursales': [
                {'clave_sucursal': '17', 'descripcion': 'Cd. Juarez'},
            ]
        },
    ]
    
    # Crear una lista de nombres de zona para mostrar en el cliente
    zonas_transformed = [{'zona': zona['zona']} for zona in zonas]
    
    # Paginar las zonas transformadas
    zonas_paginados = objPaginator(request, zonas_transformed)
    
    response_data = {
        'data_type': data_type,
        'zonas': zonas_transformed,
        'zonasPaginados': zonas_paginados,
    }
    
    return JsonResponse(response_data)

    
def handle_region(request, data_type):
    regiones = Kdregiones.objects.values('clave_region', 'descripcion_region').distinct().order_by('clave_region')
    regiones_paginados = objPaginator(request, regiones)
    
    response_data = {
        'data_type': data_type,
        'regiones' : list(regiones),
        'regionesPaginados': regiones_paginados,
    }
    
    return JsonResponse(response_data)
    
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
    'marca_inicial': handle_linea,
    'marca_final': handle_linea,
    'grupoCorporativo_inicial': handle_grupo_corporativo,
    'grupoCorporativo_final': handle_grupo_corporativo,
    'grupoCorporativo': handle_grupo_corporativo,
    'segmento_inicial': handle_segmento,
    'segmento_final': handle_segmento,
    'status': handle_status,
    'zona': handle_zona,
    'sucursal': handle_sucursal,
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