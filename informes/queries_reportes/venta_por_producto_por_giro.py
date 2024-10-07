# Description: Consulta de ventas por producto por giro
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaVentaPorProductoPorGiro(fecha_inicial, fecha_final, region):
    
    # Calcula las fechas del año anterior
    fecha_inicial_year_anterior = fecha_inicial.replace(year=fecha_inicial.year - 1)
    fecha_final_year_anterior = fecha_final.replace(year=fecha_final.year - 1)

    actual_year = str(fecha_inicial.year)
    last_year = str(fecha_inicial.year - 1)
    
    # Determinar las regiones según el valor de 'region'
    if region == '1':
        regions = 'IN (02, 02, 02, 02, 02)'
    elif region == '2':
        regions = 'IN (16, 04 ,15 ,17)'
    elif region == '3':
        regions = 'IN (05, 08, 10,19)'
    elif region == '4':
        regions = 'IN (03, 09, 12, 14, 20)'
    elif region == '5':
        regions = 'IN (07, 11, 13, 18)'

    with connection.cursor() as cursor:
        query = f"""
            DECLARE 
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @fecha_inicial_year_anterior DATE = CONVERT(DATE, %s, 102),
                @fecha_final_year_anterior DATE = CONVERT(DATE, %s, 102);
                
            SELECT
                ISNULL(VtasAct.CLAVE, VtasAnt.CLAVE) AS CLAVE,
                Productos.C2 AS Productos,
                ISNULL(VtasAnt.AutoservicioVENTA, 0) AS autoservicio_venta_{last_year},
                ISNULL(VtasAct.AutoservicioVENTA, 0) AS autoservicio_venta_{actual_year},
                ISNULL(VtasAct.AutoservicioVENTA, 0) - ISNULL(VtasAnt.AutoservicioVENTA, 0) AS diferencia_autoservicio,
                ISNULL(VtasAnt.FoodserviceVENTA, 0) AS foodservice_venta_{last_year},
                ISNULL(VtasAct.FoodserviceVENTA, 0) AS foodservice_venta_{actual_year},
                ISNULL(VtasAct.FoodserviceVENTA, 0) - ISNULL(VtasAnt.FoodserviceVENTA, 0) AS diferencia_foodservice,
                ISNULL(VtasAnt.FoodserviceVENTA, 0) + ISNULL(VtasAnt.AutoservicioVENTA, 0) AS total_{last_year},
                ISNULL(VtasAct.FoodserviceVENTA, 0) + ISNULL(VtasAct.AutoservicioVENTA, 0) AS total_{actual_year},
                ISNULL(VtasAct.FoodserviceVENTA, 0) + ISNULL(VtasAct.AutoservicioVENTA, 0) - ISNULL(VtasAnt.FoodserviceVENTA, 0) - ISNULL(VtasAnt.AutoservicioVENTA, 0) AS diferencia_total
            FROM (
                SELECT
                    KDIJ.C3 AS CLAVE,
                    SUM(CASE WHEN KDUD.C33 IN ('A', 'a') THEN ISNULL(KDIJ.C14, 0) END) AS AutoservicioVENTA,
                    SUM(CASE WHEN KDUD.C33 NOT IN ('A', 'a') THEN ISNULL(KDIJ.C14, 0) END) AS FoodserviceVENTA
                FROM KDIJ
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                WHERE
                    KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C1 {regions}
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '21', '22', '25', '26')
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                GROUP BY KDIJ.C3
            ) AS VtasAct
            FULL JOIN (
                SELECT
                    KDIJ.C3 AS CLAVE,
                    SUM(CASE WHEN KDUD.C33 IN ('A', 'a') THEN ISNULL(KDIJ.C14, 0) END) AS AutoservicioVENTA,
                    SUM(CASE WHEN KDUD.C33 NOT IN ('A', 'a') THEN ISNULL(KDIJ.C14, 0) END) AS FoodserviceVENTA
                FROM KDIJ
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                WHERE
                    KDIJ.C10 >= @fecha_inicial_year_anterior
                    AND KDIJ.C10 <= @fecha_final_year_anterior
                    AND KDIJ.C1 {regions}
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '21', '22', '25', '26')
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                GROUP BY KDIJ.C3
            ) AS VtasAnt ON VtasAnt.CLAVE = VtasAct.CLAVE
            LEFT JOIN (
                SELECT C1, C2 FROM KDII
            ) AS Productos ON VtasAnt.CLAVE = Productos.C1 OR VtasAct.CLAVE = Productos.C1
            ORDER BY 1;
        """

        # Definir los parámetros para las fechas
        params = [fecha_inicial, fecha_final, fecha_inicial_year_anterior, fecha_final_year_anterior]

        for param in params:
            print(param, type(param))

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result
