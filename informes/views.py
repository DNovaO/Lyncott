from django.shortcuts import render

def report_view(request):
    categoria_reporte = request.GET.get('categoria_reporte')
    tipo_reporte = request.GET.get('tipo_reporte')

    return render(request, 'informes/reportes.html', {'categoria_reporte': categoria_reporte, 'tipo_reporte': tipo_reporte})
