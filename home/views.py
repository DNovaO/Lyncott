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
            "Cierre de Mes",
            "Comparativo de Ventas por Producto (Sin Refacturación)",
            "Comparativo Precios, Reales vs Teoricos y Venta Simulada",
            "Conciliación de Ventas",
            "Lista de Precios por Producto y por Zonas",
            "Por Cliente",
            "Por Producto",
            "Tendencia de las Ventas",
            "Tendencia de las Ventas por Sector (2020)",
            "Trazabilidad por Producto",
            "Ventas de Credito y Contado (Sin Refacturación)",
            "Ventas en Cadenas FoodService",
            "Ventas en General (Pesos Sin Refacturación)",
            "Ventas por Tipo de Cliente (Sin Refacturación)"
        ],

        
        "Contable": [
            "Credito Contable (con Refacturación)",
            "Folios de Facturas",
            "Por Familia en Kilos (con Refacturación)",
            "Por Producto (con Refacturación)",
            "Por Tipo de Cliente (con Refacturación)"
        ],

        
        "Indicadores": [
            "Análisis Semanal de los Principales Contribuyentes a través del Principio 80/20",
            "Avance de Ventas por Vendedor",
            "Comparativa de Notas de Crédito en Kilogramos",
            "Comparativa de Ventas y Presupuesto por Zonas en Pesos",
            "Informe de Ventas por Zonas en Kilogramos y por Marca (Sin Refacturación)",
            "Informe de Ventas por Zonas en Pesos",
            "Ventas Contra Devoluciones",
            "Ventas Sin Cargo",
            "Ventas sin Notas de Credito en Pesos",
            "Ventas de Cadenas AutoService KAM",
            "Ventas de Cadenas FoodService KAM",
            "Ventas por Familia en Kilos (Sin Refacturación)",
            "Ventas por Familia en Pesos (Sin Refacturación)",
            "Ventas por Zonas Kilos (Sin Refacturación)",
            "Ventas por Zonas Pesos (Sin Refacturación)"
        ],

        
        "Clientes / Consignatarios / Segmento": [
            "Análisis de Ventas por Vendedor",
            "Clientes por Grupos",
            "Clientes y Consignatarios Activos",
            "Clientes y Productos por Grupo",
            "Consignatarios por Código Postal",
            "Consignatarios por Familia",
            # "Consignatarios por Producto",
            "Consignatarios por Segmento",
            "Consignatarios por Sucursal",
            "Ventas a Clientes/Consignatarios por Mes",
            "Ventas de Clientes por Grupo, Consignatario y Producto"
        ],
                
        "Regional": [
            "Ventas Sin Cargo por Zona",
            "Ventas Sin Cargo por Zona según el Mes",
            "Ventas por Producto por Giro",
            "Ventas por Familia por Producto",
            "Ventas por Familia por Región",
        ],

        "Devoluciones": [
            "Devoluciones por Fecha",
            "Devoluciones por Sucursal",
            "Devoluciones por Zona en Kilogramos",
            "Devoluciones por Zona en Pesos"
        ],

    }
    
    if request.method == 'POST':
        if 'categoria_reporte' in request.POST and 'tipo_reporte' in request.POST:
            categoria_reporte = request.POST.get('categoria_reporte')
            tipo_reporte = request.POST.get('tipo_reporte')
            clients_page = 0
            report_url = reverse('report')
            report_url += '?categoria_reporte={}&tipo_reporte={}&page={}'.format(categoria_reporte, tipo_reporte, clients_page)
            return redirect(report_url)
        else:
            return redirect('home')  # Esto maneja el POST que no contiene esos datos

    context = {
        'categorias_reporte': categorias_reporte,
        'dbname': dbname,
    }
    return render(request, 'portal/home.html', context)

