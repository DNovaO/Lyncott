from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .handlers import handle_data
import json
import logging

logger = logging.getLogger(__name__)

def report_view(request):
    print("------ Report View -----")
    categoria_reporte = request.GET.get('categoria_reporte', 'default_categoria')
    tipo_reporte = request.GET.get('tipo_reporte', 'default_tipo')

    if request.method == 'POST':
        try:
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
        return render(request, 'informes/reportes.html', context)