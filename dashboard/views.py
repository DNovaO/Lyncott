from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.db import connection
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
                data_1 = json.loads(request_data)
                print(f"POST Data Received: {data_1}")
                
                
                if data_1.get('Titulo') == 'Ventas y Devoluciones':
                    ventas_ind = ventas_indivuales()
                    
                    data = {
                        "status": "ok",
                        "ventas": ventas_ind,
                        "devoluciones": 50,
                    } 
                
                    json_data = json.dumps(data)
                    compressed_data = gzip.compress(json_data.encode('utf-8'))

                    response = HttpResponse(compressed_data, content_type='application/json')
                    response['Content-Encoding'] = 'gzip'

                    return response
                
                elif data_1.get('Titulo') == "Estadisticas Rapidas":
                    data = {
                        "status": "ok",
                        "ventas": 150,
                        "devoluciones": 50,
                        "productos": 100,
                        "clientes": 200,
                        "sucursales": 20,
                    } 
                
                    json_data = json.dumps(data)
                    compressed_data = gzip.compress(json_data.encode('utf-8'))

                    response = HttpResponse(compressed_data, content_type='application/json')
                    response['Content-Encoding'] = 'gzip'

                    return response
                
                elif data_1.get('Titulo') == "Distribucion de Ventas":
                    data = {
                        "status": "ok",
                        "ventas": 150,
                        "productos": 100,
                        "ventas_totales":500000,
                        "sucursales": 20,
                    }
                    
                    json_data = json.dumps(data)
                    compressed_data = gzip.compress(json_data.encode('utf-8'))

                    response = HttpResponse(compressed_data, content_type='application/json')
                    response['Content-Encoding'] = 'gzip'

                    return response
                
                elif data_1.get('Titulo') == "Autorizaciones de Gasto":
                    data = {
                        "status": "ok",
                        "titulo": "Viaje gastos",
                        "gastos": 150,
                        "fecha": "2021-10-10",
                        "autorizacion": "Pendiente",
                    }
                    
                    json_data = json.dumps(data)
                    compressed_data = gzip.compress(json_data.encode('utf-8'))

                    response = HttpResponse(compressed_data, content_type='application/json')
                    response['Content-Encoding'] = 'gzip'

                    return response
                
                ventas_ind = ventas_indivuales()
                data = {
                    "status": "ok",
                    "ventas": ventas_ind,
                    "devoluciones": 45,
                }

                json_data = json.dumps(data)
                compressed_data = gzip.compress(json_data.encode('utf-8'))

                response = HttpResponse(compressed_data, content_type='application/json')
                response['Content-Encoding'] = 'gzip'

                return response

            except json.JSONDecodeError:
                return JsonResponse({"status": "error", "message": "JSON inválido en el cuerpo de la solicitud"}, status=400)
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)

        else:
            return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    # Para solicitudes que no son JSON, renderizamos la página HTML
    return render(request, 'dashboard/dashboard.html')


def ventas_indivuales():
    with connection.cursor() as cursor:
        query_ventas_indivuales = """
            SELECT SUM(C14) AS VENTAS FROM KDIJ ;
        """
        
        # Ejecutar la consulta
        cursor.execute(query_ventas_indivuales)

        # Obtener los resultados
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result
