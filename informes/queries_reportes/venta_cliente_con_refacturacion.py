# Description: Consulta para obtener el tipo de cliente con refacturación
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
import json


from django.db import connection
from decimal import Decimal

def consultaVentaPorCliente(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta de ventas por cliente desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}")
        
    with connection.cursor() as cursor:
        query = """
            DECLARE @p_inicial AS VARCHAR(10) = %s, 
                    @p_final AS VARCHAR(10) = %s, 
                    @f_inicial AS DATETIME = %s, 
                    @f_final AS DATETIME = %s, 
                    @c_inicial AS VARCHAR(10) = %s, 
                    @c_final AS VARCHAR(10) = %s;

            SELECT
                CASE    
                    WHEN VENTAS.SUC IN ('04','15','16','17') THEN '2.-Norte'
                    WHEN VENTAS.SUC IN ('05','08','10','19') THEN '3.-Centro'
                    WHEN VENTAS.SUC IN ('03','09','12','14','20') THEN '4.-Pacifico'
                    WHEN VENTAS.SUC IN ('07','11','13','18') THEN '5.-Sureste'
                    ELSE '1.-Vallejo'
                END AS zona,
                
                CASE    
                    WHEN VENTAS.SUC = '1' THEN '1&nbsp;-&nbsp;Autoservicio'
                    WHEN VENTAS.SUC = '2' THEN '2&nbsp;-&nbsp;Norte'
                    WHEN VENTAS.SUC = '3' THEN '3&nbsp;-&nbsp;Sur'
                    WHEN VENTAS.SUC = '4' THEN '4&nbsp;-&nbsp;Vent. Especiales'
                    WHEN VENTAS.SUC = '5' THEN '5&nbsp;-&nbsp;Cadenas'
                    WHEN VENTAS.SUC = '6' THEN '6&nbsp;-&nbsp;Centro'
                    ELSE VENTAS.SUC + '&nbsp;-&nbsp;' + SUCURSAL.C2
                END AS sucursal,
                
                SUM(VENTAS.KilosAutoservice) AS KilosAutoservice,
                SUM(VENTAS.VentaAutoservice) AS VentaAutoservice,
                SUM(VENTAS.KilosFoodservice) AS KilosFoodservice,
                SUM(VENTAS.VentaFoodservice) AS VentaFoodservice,
                
                SUM(VENTAS.KilosAutoservice) + SUM(VENTAS.KilosFoodservice) AS KilosTotal,
                SUM(VENTAS.VentaAutoservice) + SUM(VENTAS.VentaFoodservice) AS VentaTotal
                
            FROM (
                -- Primer bloque de la consulta UNION
                SELECT 
                    CASE 
                        WHEN KDIJ.C1 = '02' THEN LTRIM(RTRIM(KDUV.C22))
                        ELSE LTRIM(RTRIM(KDIJ.C1))
                    END AS SUC,
                    
                    SUM(CASE WHEN KDUD.C30 = 'A' THEN KDIJ.C14 ELSE 0 END) AS VentaAutoservice,
                    SUM(CASE WHEN KDUD.C30 = 'A' THEN KDIJ.C11 * KDII.C13 ELSE 0 END) AS KilosAutoservice,
                    SUM(CASE WHEN KDUD.C30 <> 'A' THEN KDIJ.C14 ELSE 0 END) AS VentaFoodservice,
                    SUM(CASE WHEN KDUD.C30 <> 'A' THEN KDIJ.C11 * KDII.C13 ELSE 0 END) AS KilosFoodservice
                FROM KDIJ
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                WHERE KDIJ.C3 BETWEEN @p_inicial AND @p_final
                AND KDIJ.C10 BETWEEN @f_inicial AND @f_final
                AND KDIJ.C15 BETWEEN @c_inicial AND @c_final
                AND KDIJ.C4 = 'U'
                AND KDIJ.C5 = 'D'
                AND KDIJ.C6 IN ('5', '45')
                GROUP BY KDIJ.C1, KDUV.C22, KDUD.C30

                UNION

                -- Segundo bloque de la consulta UNION
                SELECT 
                    CASE 
                        WHEN KDIJ.C1 = '02' THEN LTRIM(RTRIM(KDUV.C22))
                        ELSE LTRIM(RTRIM(KDIJ.C1))
                    END AS SUC,
                    
                    SUM(CASE WHEN KDUD.C33 = 'A' THEN KDIJ.C14 ELSE 0 END) AS VentaAutoservice,
                    SUM(CASE WHEN KDUD.C33 = 'A' THEN KDIJ.C11 * KDII.C13 ELSE 0 END) AS KilosAutoservice,
                    SUM(CASE WHEN KDUD.C33 <> 'A' THEN KDIJ.C14 ELSE 0 END) AS VentaFoodservice,
                    SUM(CASE WHEN KDUD.C33 <> 'A' THEN KDIJ.C11 * KDII.C13 ELSE 0 END) AS KilosFoodservice
                FROM KDIJ
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                WHERE KDIJ.C3 BETWEEN @p_inicial AND @p_final
                AND KDIJ.C10 BETWEEN @f_inicial AND @f_final
                AND KDIJ.C15 BETWEEN @c_inicial AND @c_final
                AND KDIJ.C4 = 'U'
                AND KDIJ.C5 = 'D'
                AND KDIJ.C6 IN ('5', '45')
                GROUP BY KDIJ.C1, KDUV.C22, KDUD.C33
            ) AS VENTAS
            LEFT JOIN (
                SELECT KDMS.C1, KDMS.C2 FROM KDMS
            ) AS SUCURSAL ON SUCURSAL.C1 = VENTAS.SUC
            GROUP BY VENTAS.SUC, SUCURSAL.C2

            -- Ordenar por zona y luego por sucursal
            ORDER BY 
                CASE    
                    WHEN VENTAS.SUC IN ('04','15','16','17') THEN 2  -- '2.-Norte'
                    WHEN VENTAS.SUC IN ('05','08','10','19') THEN 3  -- '3.-Centro'
                    WHEN VENTAS.SUC IN ('03','09','12','14','20') THEN 4  -- '4.-Pacifico'
                    WHEN VENTAS.SUC IN ('07','11','13','18') THEN 5  -- '5.-Sureste'
                    ELSE 1  -- '1.-Vallejo'
                END, 
                SUCURSAL.C2;


        """

        params = [
            producto_inicial, producto_final, 
            fecha_inicial, fecha_final,
            cliente_inicial, cliente_final,
        
        ]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        
    return result

def formatear_resultados_a_json(resultados):
    grupos = {
        'Vallejo': [],
        'Norte': [],
        'Centro': [],
        'Pacifico': [],
        'Sureste': []
    }

    for fila in resultados:
        zona = fila['zona']
        grupos[zona].append(fila)

    tabla = []

    for zona, filas in grupos.items():
        total_kilos_autoservicio = 0
        total_venta_autoservicio = 0
        total_kilos_foodservice = 0
        total_venta_foodservice = 0
        
        for fila in filas:
            tabla.append({
                'sucursal': fila['sucursal'],
                'KilosAutoservice': fila['KilosAutoservice'],
                'VentaAutoservice': fila['VentaAutoservice'],
                'KilosFoodservice': fila['KilosFoodservice'],
                'VentaFoodservice': fila['VentaFoodservice']
            })
            total_kilos_autoservicio += fila['KilosAutoservice']
            total_venta_autoservicio += fila['VentaAutoservice']
            total_kilos_foodservice += fila['KilosFoodservice']
            total_venta_foodservice += fila['VentaFoodservice']
        
        tabla.append({
            'sucursal': f'Totales del grupo {zona}',
            'KilosAutoservice': total_kilos_autoservicio,
            'VentaAutoservice': total_venta_autoservicio,
            'KilosFoodservice': total_kilos_foodservice,
            'VentaFoodservice': total_venta_foodservice
        })

    return json.dumps(tabla)  # Devolver como JSON
