from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse
from .models import *
from .handlers import handle_data
import json
import logging

logger = logging.getLogger(__name__)

def report_view(request):
    print("------ Report View -----")

    # Obtener parámetros GET, con un valor predeterminado de 0 para 'page' si no se proporciona
    categoria_reporte = request.GET.get('categoria_reporte', None)
    tipo_reporte = request.GET.get('tipo_reporte', None)
    page = request.GET.get('page', 0)

    print(f"GET Parameters - categoria_reporte: {categoria_reporte}, tipo_reporte: {tipo_reporte}, page: {page}")

    # Si la solicitud es POST
    if request.method == 'POST':
        try:
            # Leer y analizar los datos JSON recibidos
            data = json.loads(request.body)
            print(f"POST Data Received: {data}")

            # Variables clave del POST
            cambio = data.get('cambio', False)  # Verificar si es una solicitud de cambio
            data_type = data.get('data_type')   # Otro tipo de datos si no es un cambio

            print(f"POST Flags - cambio: {cambio}, data_type: {data_type}")

            # Si 'cambio' es True, redirigir con nuevos parámetros
            if cambio:
                categoria = data.get('nueva_categoria')
                tipo = data.get('nuevo_tipo')
                page = data.get('page', 0)  # Obtener la página del cuerpo JSON si está presente

                print(f"New Values - nueva_categoria: {categoria}, nuevo_tipo: {tipo}, page: {page}")

                # Crear la nueva URL completa con los parámetros
                report_url = reverse('report')
                report_url += '?categoria_reporte={}&tipo_reporte={}&page={}'.format(categoria, tipo, page)
                print(f"Redirecting to URL: {report_url}")
                
                # Responder con el JSON de redirección
                return JsonResponse({'redirect_url': report_url}, status=200)

            # Si 'data_type' está presente, manejar los datos de reporte
            elif data_type:
                print(f"Handling data with data_type: {data_type}")
                return handle_data(request, data_type)

            # Respuesta en caso de que el POST no contenga ni 'cambio' ni 'data_type'
            else:
                print("POST Request Missing 'cambio' or 'data_type'")
                return JsonResponse({'error': 'No se especificó un tipo de operación'}, status=400)

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            print(f"JSON Decode Error: {e}")
            return JsonResponse({'error': f'Formato JSON inválido: {e}'}, status=400)
        except KeyError as e:
            logger.error(f"Falta clave en los datos de la solicitud: {e}")
            print(f"KeyError: {e}")
            return JsonResponse({'error': f'Clave faltante: {e}'}, status=400)
        except Exception as e:
            logger.error(f"Error inesperado en el servidor: {e}")
            print(f"Unexpected Error: {e}")
            return JsonResponse({'error': f'Error en el servidor: {e}'}, status=500)
    
    # En caso de solicitud GET
    else:
        print("Rendering template with context")
        context = {
            'categoria_reporte': categoria_reporte,
            'tipo_reporte': tipo_reporte,
            'page': page,
        }
        print(f"Context Data: {context}")
        return render(request, 'informes/reportes.html', context)
