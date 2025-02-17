from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .queries_dashboard.dashboard_ventas_contra_devoluciones import ventas_contra_devoluciones
from .queries_dashboard.dasboard_estadisticas_rapidas import estadisticas_rapidas
from .queries_dashboard.dashboard_distribucion_productos import distribucion_venta_productos, parse_date
from .queries_dashboard.dashboard_bolsa_mercado import get_stock_data
from .queries_dashboard.dashboard_tendencia_ventas import consultaTendenciaVentasDashboard
# from .queries_dashboard.alta_usuarios import importar_usuarios
import json
import gzip

def dashboard_view(request):
    if request.headers.get('Accept') == 'application/json':
        if request.method == "POST":
            # importar_usuarios()
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
                    
                    fecha_inicial = parse_date(fecha_inicial)
                    fecha_final = parse_date(fecha_final)
                    
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
                    fecha_inicial = data_json.get('Fecha_inicial')
                    fecha_final = data_json.get('Fecha_final')
    
                    distrubucion_ventas = distribucion_venta_productos(fecha_inicial, fecha_final)

                    fecha_inicial = parse_date(fecha_inicial)
                    fecha_final = parse_date(fecha_final)
    
                    data = {
                        "status": "ok",
                        "titulo": "Distribucion de Ventas",
                        "distribucion_ventas": distrubucion_ventas,
                        "fecha": fecha_inicial,
                        "fecha_final": fecha_final,
                    }
                    
                    json_data = json.dumps(data)
                    compressed_data = gzip.compress(json_data.encode('utf-8'))

                    response = HttpResponse(compressed_data, content_type='application/json')
                    response['Content-Encoding'] = 'gzip'

                    return response
                elif data_json.get('Titulo') == "Tendencia de Ventas":
                    fecha_inicial = data_json.get('Fecha_inicial')
                    fecha_final = data_json.get('Fecha_final')
    
                    tendencia_ventas = consultaTendenciaVentasDashboard(fecha_inicial, fecha_final)

                    fecha_inicial = parse_date(fecha_inicial)
                    fecha_final = parse_date(fecha_final)
                    
                    data = {
                        "status": "ok",
                        "titulo": "Tendencia de Ventas",
                        "tendencia_ventas": tendencia_ventas,
                        "fecha": fecha_inicial,
                        "fecha_final": fecha_final,
                    }
                    
                    json_data = json.dumps(data)
                    compressed_data = gzip.compress(json_data.encode('utf-8'))

                    response = HttpResponse(compressed_data, content_type='application/json')
                    response['Content-Encoding'] = 'gzip'

                    return response
                elif data_json.get('Titulo') == "Bolsa Acciones":
                    symbols = ["VOO", "IVV", "VNO", "MSFT", "GOOGL"]
                    
                    bolsa_acciones = {}

                    for symbol in symbols:
                        bolsa_acciones[symbol] = get_stock_data(symbol)

                    data = {
                        "status": "ok",
                        "titulo": "Bolsa Acciones",
                        "acciones": bolsa_acciones,
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

