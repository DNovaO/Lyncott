from django.http import JsonResponse
from django.shortcuts import render

def dashboard_view(request):
    if request.headers.get('Accept') == 'application/json':
        if request.method == "GET":
            data = {
                "status": "ok",
                "ventas": 1200,
                "devoluciones": 45,
            }
            return JsonResponse(data)  # Responde con JSON
        else:
            return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    # Para solicitudes que no son JSON, renderizamos la página HTML
    return render(request, 'dashboard/dashboard.html')
