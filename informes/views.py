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



# def report_view(request):
    
    
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             data_type = data.get('data_type')
            
#             # Para propósitos de depuración, podemos imprimir el data_type recibido
#             print("Received data_type:", data_type)

#             # Retornar el data_type en la respuesta JSON como prueba
#             response_data = {
#                 'status': 'success',
#                 'data_type': data_type,
#             }
#             return JsonResponse(response_data)
        
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)
    # categoria_reporte = request.GET.get('categoria_reporte', 'default_categoria')
    # tipo_reporte = request.GET.get('tipo_reporte', 'default_tipo')
    # dataType = request.GET.get('dataType', 'default_dataType')
    
    # QUERYS = {
    #     'clientes': Kdud.objects.values('clave_cliente', 'nombre_cliente').distinct().order_by('clave_cliente'),
    #     'sucursales': Kdms.objects.values('clave_sucursal', 'descripcion').distinct().order_by('clave_sucursal'),
    #     'productos': Kdii.objects.values('clave_producto', 'descripcion_producto', 'linea_producto').distinct().order_by('clave_producto'),
    # }
    
    # for query in QUERYS:
    #     list_query, page_query = queryPaginator(request, QUERYS[query])
    #     print(list_query)
        
    #     if request.method == 'POST':
    #         try:
    #             return JsonResponse({
    #                 query: list_query,
    #                 'Pagination': get_pagination_html(page_query),
    #             })
    #         except Exception as e:
    #             return JsonResponse({'error': str(e)}, status=400)
            
    # context = {
    #     'categoria_reporte': categoria_reporte,
    #     'tipo_reporte': tipo_reporte,
    # }
    
    # return render(request, 'informes/reportes.html', context)


# def queryPaginator(request, query):
    
#     paginator = Paginator(query, 10)
#     page_number = request.GET.get('page')
#     query_page = paginator.get_page(page_number)
#     query_list = list(query_page)
    
#     return query_list, query_page

# def get_pagination_html(page_obj):
#     return {
#         'has_previous': page_obj.has_previous(),
#         'has_next': page_obj.has_next(),
#         'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
#         'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
#         'number': page_obj.number,
#         'num_pages': page_obj.paginator.num_pages,
#     }
    
# def searchList(request, query):
    
#     print('hola')
    
#     return


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