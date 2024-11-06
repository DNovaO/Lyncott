# views.py

# Diego Nova Olguín
# Ultima modificación: 17/10/2024

# Funcion que se encarga de manejar las peticiones de los datos de los reportes.
# Maneja los datatypes y en base a estos se encarga de llamar a las funciones correspondientes y
# renderizar los datos en el formato correspondiente para los reportes.

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

    # Si hay parámetros en la URL, los obtenemos
    categoria_reporte = request.GET.get('categoria_reporte', None)
    tipo_reporte = request.GET.get('tipo_reporte', None)

    # Si la solicitud es POST
    if request.method == 'POST':
        try:
            # Procesamos los datos JSON enviados con la solicitud POST
            data = json.loads(request.body)
            data_type = data.get('data_type')

            if data_type:
                return handle_data(request, data_type)

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse({'error': f'Invalid JSON format: {e}'}, status=400)
        except KeyError as e:
            logger.error(f"Missing key in request data: {e}")
            return JsonResponse({'error': f'Missing key: {e}'}, status=400)
        except Exception as e:
            logger.error(f"Unexpected server error: {e}")
            return JsonResponse({'error': f'Server error: {e}'}, status=500)
    else:
        context = {
            'categoria_reporte': categoria_reporte,
            'tipo_reporte': tipo_reporte,
        }
        print("------ Report View GET 4 -----")
        return render(request, 'informes/reportes.html', context)
