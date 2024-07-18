from django.shortcuts import redirect, render   
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import connection
from django.core.paginator import Paginator
from informes.models import Kdud

@login_required
def home_view(request):
    
    #Conexion a base de datos para mostrar que la conexion es valida
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DB_NAME() AS dbname")
            row = cursor.fetchone()
            print("Base de datos conectada")
            dbname = row[0] if row else None
    except Exception as e:
        dbname = False
        
    categorias_reporte = { 
        "Ventas": [
                   "Por Producto",
                   "Por Cliente",
                   "Ventas en Cadenas FoodService",
                   "Ventas por Tipo de Cliente (Sin Refacturación)",
                   "Ventas de Credito y Contado (Sin Refacturación)",
                   "Cierre de Mes",
                   "Conciliación de Ventas",
                   "Lista de Precios por Producto y por Zonas",
                   "Comparativo Precios, Reales vs Teoricos y Venta Simulada",
                   "Comparativo de Ventas por (Producto Sin Refacturación)",
                   "Ventas en General (Pesos Sin Refacturación)",
                   "Tendencia de las Ventas",
                   "Tendencia de las Ventas por Sector (2020)",
                   "Trazabilidad por Producto"],
        
        "Contable": [
                     "Por Producto (con Refacturación)",
                     "Por Tipo de Cliente (con Refacturación)",
                     "Credito Contable (con Refacturación)",
                     "Por Familia en Kilos (con Refacturación)", 
                     "Folios de Facturas"],
        
        
        "Indicadores": ["Ventas por Zonas Pesos (Sin Refacturación)",
                        "Ventas por Zonas Kilos (Sin Refacturación)",
                        "Ventas por Familia en Pesos (Sin Refacturación)",
                        "Ventas por Familia en Kilos (Sin Refacturación)",
                        "Informe de Ventas por Zonas en Pesos",
                        "Informe de Ventas por Zonas en Kilogramos y por Marca (Sin Refacturación)",
                        "Ventas Sin Cargo",
                        "Ventas de Cadenas FoodService KAM",
                        "Ventas de Cadenas AutoService KAM",
                        "Comparativa de Notas de Crédito en Kilogramos",
                        "Ventas sin Notas de Credito en Pesos",
                        "Avance de Ventas por Vendedor",
                        "Análisis Semanal de los Principales Contribuyentes a través del Principio 80/20",
                        "Ventas Contra Devoluciones",
                        "Comparativa de Ventas y Presupuesto por Zonas en Pesos (Sin Refacturación)"],
        
        "Clientes / Consignatarios / Segmento": [
                                                "Clientes por Grupos",
                                                "Consignatarios por Código Postal",
                                                "Consignatarios por Segmento",
                                                "Consignatarios por Producto",
                                                "Consignatarios por Familia",
                                                "Ventas a Clientes/Consignatarios por Mes",
                                                "Ventas de Clientes por Grupo, Consignatario y Producto",
                                                "Clientes y Productos por Grupo",
                                                "Consignatarios por Sucursal",
                                                "Análisis de Ventas por Vendedor",
                                                "Clientes y Consignatarios Activos"],
        
        "Regional": [
                    "Ventas por Categoría según la Región", 
                     "Ventas por Producto según la Familia",
                     "Ventas de Producto según el Sector",
                     "Ventas Sin Cargo por Zona",
                     "Ventas Sin Cargo por Zona según el Mes"],
        
        "Devoluciones": [
                        "Devoluciones por Fecha",
                         "Devoluciones por Sucursal",
                         "Devoluciones por Zona en Pesos",
                         "Devoluciones por Zona en Kilogramos"],
    }
    
    if request.method == 'POST':
        categoria_reporte = request.POST.get('categoria_reporte')
        tipo_reporte = request.POST.get('tipo_reporte')
        clients_page = 0
        # Obtener la URL inversa de 'report' y pasar los parámetros como argumentos de consulta
        report_url = reverse('report')
        report_url += '?categoria_reporte={}&tipo_reporte={}&page={}'.format(categoria_reporte, tipo_reporte,clients_page)
        return redirect(report_url)

    context = {
        'categorias_reporte': categorias_reporte,
        'dbname': dbname,
    }
    return render(request, 'portal/home.html', context)
