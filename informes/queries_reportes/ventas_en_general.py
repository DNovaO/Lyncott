# Description: Consulta de ventas en general
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.fechas import obtener_rango_fechas


def consultaVentasEnGeneral(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta de ventas en general desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}")

    # Obtener el rango de fechas por mes
    rangos_fechas = obtener_rango_fechas()

    with connection.cursor() as cursor:
        query = """
           SELECT 
                KDIJ.C1 AS sucursal,
                CASE 
                    WHEN KDUV.C22 = 1 THEN 'Autoservicio'
                    WHEN KDUV.C22 = 2 THEN 'Norte'
                    WHEN KDUV.C22 = 3 THEN 'Sur'
                    WHEN KDUV.C22 = 4 THEN 'Vent. Especiales'
                    WHEN KDUV.C22 = 5 THEN 'Cadenas'
                    WHEN KDUV.C22 = 6 THEN 'Centro'
                    ELSE 'sin asignar a Vallejo'
                END AS nombre,
                CONCAT('1 - ', KDMS.C2) AS zona,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_ENE,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_FEB,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_MAR,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_ABR,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_MAY,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_JUN,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_JUL,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_AGO,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_SEP,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_OCT,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_NOV,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_DIC
            FROM 
                KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1
            WHERE 
                KDII.C1 BETWEEN %s AND %s
                AND KDIJ.C10 BETWEEN %s AND %s
                AND KDIJ.C1 = '02'
                AND KDUV.C22 BETWEEN '1' AND '6'
                AND KDUD.C2 BETWEEN %s AND %s
                AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                AND KDIJ.C4 = 'U'
                AND KDIJ.C5 = 'D'
                AND KDIJ.C6 IN ('5','45')
            GROUP BY 
                KDIJ.C1,
                KDUV.C22,
                KDMS.C2

            UNION

            SELECT 
                KDIJ.C1 AS sucursal, 
                KDMS.C2 AS nombre,
                CASE 
                    WHEN KDIJ.C1 IN ('04','15','16','17') THEN '2 - Norte'
                    WHEN KDIJ.C1 IN ('05','08','10','19') THEN '4 - Centro'
                    WHEN KDIJ.C1 IN ('03','09','12','14','06','20') THEN '3 - Pacifico'
                    WHEN KDIJ.C1 IN ('07','11','13','18') THEN '5 - Sureste'
                    ELSE 'Sin zona'
                END AS zona,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_ENE,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_FEB,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_MAR,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_ABR,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_MAY,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_JUN,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_JUL,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_AGO,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_SEP,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_OCT,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_NOV,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_DIC
            FROM 
                KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1
            WHERE 
                KDII.C1 BETWEEN %s AND %s
                AND KDIJ.C10 BETWEEN %s AND %s
                AND KDIJ.C1 IN ('03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20')
                AND KDUD.C2 BETWEEN %s AND %s
                AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                AND KDIJ.C4 = 'U'
                AND KDIJ.C5 = 'D'
                AND KDIJ.C6 IN ('5','45')
            GROUP BY 
                KDIJ.C1,
                KDMS.C2

            ORDER BY 
                3, 1;

        """

        # Lista de parámetros con los rangos de fechas mensuales
        params = [
            rangos_fechas['january_inicial'], rangos_fechas['january_final'],
            rangos_fechas['february_inicial'], rangos_fechas['february_final'],
            rangos_fechas['march_inicial'], rangos_fechas['march_final'],
            rangos_fechas['april_inicial'], rangos_fechas['april_final'],
            rangos_fechas['may_inicial'], rangos_fechas['may_final'],
            rangos_fechas['june_inicial'], rangos_fechas['june_final'],
            rangos_fechas['july_inicial'], rangos_fechas['july_final'],
            rangos_fechas['august_inicial'], rangos_fechas['august_final'],
            rangos_fechas['september_inicial'], rangos_fechas['september_final'],
            rangos_fechas['october_inicial'], rangos_fechas['october_final'],
            rangos_fechas['november_inicial'], rangos_fechas['november_final'],
            rangos_fechas['december_inicial'], rangos_fechas['december_final'],
            producto_inicial, producto_final,
            fecha_inicial, fecha_final,
            cliente_inicial, cliente_final,

            rangos_fechas['january_inicial'], rangos_fechas['january_final'],
            rangos_fechas['february_inicial'], rangos_fechas['february_final'],
            rangos_fechas['march_inicial'], rangos_fechas['march_final'],
            rangos_fechas['april_inicial'], rangos_fechas['april_final'],
            rangos_fechas['may_inicial'], rangos_fechas['may_final'],
            rangos_fechas['june_inicial'], rangos_fechas['june_final'],
            rangos_fechas['july_inicial'], rangos_fechas['july_final'],
            rangos_fechas['august_inicial'], rangos_fechas['august_final'],
            rangos_fechas['september_inicial'], rangos_fechas['september_final'],
            rangos_fechas['october_inicial'], rangos_fechas['october_final'],
            rangos_fechas['november_inicial'], rangos_fechas['november_final'],
            rangos_fechas['december_inicial'], rangos_fechas['december_final'],
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