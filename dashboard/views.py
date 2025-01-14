from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .queries_dashboard.dashboard_ventas_contra_devoluciones import ventas_contra_devoluciones
from .queries_dashboard.dasboard_estadisticas_rapidas import estadisticas_rapidas
from .queries_dashboard.dashboard_distribucion_productos import distribucion_venta_productos
import json
import gzip

def dashboard_view(request):
    if request.headers.get('Accept') == 'application/json':
        if request.method == "POST":
            try:
                # Validar que el cuerpo no esté vacío
                if not request.body:
                    return JsonResponse({"status": "error", "message": "Cuerpo de la solicitud vacío"}, status=400)

                # Verificar si los datos están comprimidos
                if request.headers.get('Content-Encoding') == 'gzip':
                    request_data = gzip.decompress(request.body).decode('utf-8')
                else:
                    request_data = request.body.decode('utf-8')

                # Intentar cargar el JSON
                data_json = json.loads(request_data)
                print(f"POST Data Received: {data_json}")
                
                if data_json.get('Titulo') == 'Ventas y Devoluciones':
                    fecha_inicial = data_json.get('Fecha_inicial')
                    fecha_final = data_json.get('Fecha_final')
                    
                    ventas_devoluciones = ventas_contra_devoluciones(fecha_inicial, fecha_final)
                    
                    data = {
                        "status": "ok",
                        "titulo": "Ventas y Devoluciones",
                        "ventas": ventas_devoluciones,
                        "fecha": fecha_inicial,
                        "fecha_final": fecha_final,
                    } 

                    print(f"Ventas y Devoluciones: {data}")
                
                    json_data = json.dumps(data)
                    compressed_data = gzip.compress(json_data.encode('utf-8'))

                    response = HttpResponse(compressed_data, content_type='application/json')
                    response['Content-Encoding'] = 'gzip'

                    return response
                elif data_json.get('Titulo') == "Estadisticas Rapidas":
                
                    data = {
                        "status": "ok",
                        "titulo": "Estadisticas Rapidas",
                        "estadisticas": estadisticas_rapidas(),
                    } 
                
                    json_data = json.dumps(data)
                    compressed_data = gzip.compress(json_data.encode('utf-8'))

                    response = HttpResponse(compressed_data, content_type='application/json')
                    response['Content-Encoding'] = 'gzip'

                    return response
                elif data_json.get('Titulo') == "Distribucion de Ventas": 
                                
    
                    data = {
                        "status": "ok",
                        "titulo": "Distribucion de Ventas",
                        "distribucion_ventas": distribucion_venta_productos()
                    }
                    
                    json_data = json.dumps(data)
                    compressed_data = gzip.compress(json_data.encode('utf-8'))

                    response = HttpResponse(compressed_data, content_type='application/json')
                    response['Content-Encoding'] = 'gzip'

                    return response
                elif data_json.get('Titulo') == "Autorizaciones de Gasto":
                    data = {
                        "status": "ok",
                        "titulo": "Autorizaciones de Gasto",
                        "asunto": "Viaje gastos",
                        "gastos": 150,
                        "fecha": "2021-10-10",
                        "autorizacion": "Pendiente",
                    }
                    
                    json_data = json.dumps(data)
                    compressed_data = gzip.compress(json_data.encode('utf-8'))

                    response = HttpResponse(compressed_data, content_type='application/json')
                    response['Content-Encoding'] = 'gzip'

                    return response
                
                else:
                    return JsonResponse({"status": "error", "message": "Titulo no valido"}, status=400)

            except json.JSONDecodeError:
                return JsonResponse({"status": "error", "message": "JSON inválido en el cuerpo de la solicitud"}, status=400)
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)

        else:
            return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    # Para solicitudes que no son JSON, renderizamos la página HTML
    return render(request, 'dashboard/dashboard.html')

