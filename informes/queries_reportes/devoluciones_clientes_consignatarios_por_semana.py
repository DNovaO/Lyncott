# Description: Consulta de devoluciones por cliente consignatario por semana
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaDevolucionesPorClienteConsignatarioPorSemana(producto_inicial, producto_final, sucursal_inicial, sucursal_final, cliente_inicial, cliente_final, mes, year):
    
    if sucursal_inicial == 'ALL' and sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_inicial == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '{sucursal_inicial}' AND '{sucursal_final}'"

    with connection.cursor() as cursor:
        query = f"""
            DECLARE
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s,
                @mes INT = %s,
                @year INT = %s,
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s;
            
            SELECT
                LTRIM(RTRIM(KDIJ.C1)) AS sucursal,
                LTRIM(RTRIM(KDUD.C66)) AS grupo,
                LTRIM(RTRIM(KDUD.C2)) AS cliente,
                LTRIM(RTRIM(KDM1.C181)) AS clave_consignatario,
                LTRIM(RTRIM(KDVDIREMB.C3)) AS nombre_consignatario,
                SUM(CASE
                    WHEN DATEPART(WEEK, KDIJ.C10) - DATEPART(WEEK, DATEADD(MONTH, DATEDIFF(MONTH, 0, KDIJ.C10), 0)) + 1 = 1
                    THEN KDIJ.C14 ELSE 0 END) AS SEM_1,
                SUM(CASE
                    WHEN DATEPART(WEEK, KDIJ.C10) - DATEPART(WEEK, DATEADD(MONTH, DATEDIFF(MONTH, 0, KDIJ.C10), 0)) + 1 = 2
                    THEN KDIJ.C14 ELSE 0 END) AS SEM_2,
                SUM(CASE
                    WHEN DATEPART(WEEK, KDIJ.C10) - DATEPART(WEEK, DATEADD(MONTH, DATEDIFF(MONTH, 0, KDIJ.C10), 0)) + 1 = 3
                    THEN KDIJ.C14 ELSE 0 END) AS SEM_3,
                SUM(CASE
                    WHEN DATEPART(WEEK, KDIJ.C10) - DATEPART(WEEK, DATEADD(MONTH, DATEDIFF(MONTH, 0, KDIJ.C10), 0)) + 1 = 4
                    THEN KDIJ.C14 ELSE 0 END) AS SEM_4,
                SUM(CASE
                    WHEN DATEPART(WEEK, KDIJ.C10) - DATEPART(WEEK, DATEADD(MONTH, DATEDIFF(MONTH, 0, KDIJ.C10), 0)) + 1 = 5
                    THEN KDIJ.C14 ELSE 0 END) AS SEM_5,
                SUM(KDIJ.C14) AS TOTAL
            FROM KDIJ
            INNER JOIN KDII ON KDIJ.C3 = KDII.C1
            INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
            FULL JOIN KDM1 ON KDIJ.C1 = KDM1.C1
                AND KDIJ.C4 = KDM1.C2
                AND KDIJ.C5 = KDM1.C3
                AND KDIJ.C6 = KDM1.C4
                AND KDIJ.C7 = KDM1.C5
                AND KDIJ.C8 = KDM1.C6
            FULL JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1
                AND KDM1.C181 = KDVDIREMB.C2
            WHERE 
                KDII.C1 >= @producto_inicial /*Producto Inicial*/
                AND KDII.C1 <= @producto_final /*Producto Final*/
                AND MONTH(KDIJ.C10) = @mes /*Mes derivado del parámetro único*/
                AND YEAR(KDIJ.C10) = @year   /*Año derivado del parámetro único*/
                {filtro_sucursal} /*Filtro de sucursal*/
                AND KDUD.C2 >= @cliente_inicial /*Cliente Inicial*/
                AND KDUD.C2 <= @cliente_final /*Cliente Final*/
                AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')                                                  
                AND KDIJ.C4 = 'N'
                AND KDIJ.C5 = 'D'
                AND KDIJ.C6 IN ('25')
                AND KDIJ.C7 IN ('12')
            GROUP BY
                KDIJ.C1,
                KDUD.C66,
                KDUD.C2,
                KDM1.C181,
                KDVDIREMB.C3;
        """

        # Definir los parámetros para las fechas y filtros
        params = [
            producto_inicial, producto_final,
            mes, year, 
            cliente_inicial, cliente_final
        ]

        print(f"Parámetros de consulta: {params}")  # Imprimir los parámetros para depuración
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Convertir Decimals a float para evitar problemas al mostrar los datos
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result
