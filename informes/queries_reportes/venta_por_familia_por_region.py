# Description: Consulta de ventas por familia por región
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaVentaPorFamiliaPorRegion(fecha_inicial, fecha_final, region):
    
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
                aut.CLAVE AS 'clave',
                aut.GRUPO AS 'familia',
                ISNULL(x.VENTA, 0) AS 'venta_{last_year}_$',
                ISNULL(aut.VENTA, 0) AS 'venta_{actual_year}_$',
                (ISNULL(aut.VENTA, 0) - ISNULL(x.VENTA, 0)) AS 'diferencia_$',
                ISNULL(x.KG, 0) AS 'venta_{last_year}_kg',
                ISNULL(aut.KG, 0) AS 'venta_{actual_year}_kg',
                (ISNULL(x.KG, 0) - ISNULL(aut.KG, 0)) AS 'diferencia_kg'
            FROM (
                SELECT 
                    KDIF.C1 AS CLAVE,
                    KDIF.C2 AS GRUPO,
                    SUM(KDIJ.C11 * KDII.C13) AS KG,
                    SUM(KDIJ.C14) AS VENTA
                FROM KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDIF ON KDII.C82 = KDIF.C1
                WHERE 
                    KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C1 {regions}
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '21', '22', '25', '26')
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                GROUP BY 
                    KDIF.C1, 
                    KDIF.C2
            ) aut
            LEFT JOIN (
                SELECT 
                    KDIF.C1 AS CLAVE, 
                    KDIF.C2 AS GRUPO, 
                    SUM(KDIJ.C11 * KDII.C13) AS KG, 
                    SUM(KDIJ.C14) AS VENTA
                FROM KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDIF ON KDII.C82 = KDIF.C1
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                WHERE 
                    KDIJ.C10 >= @fecha_inicial_year_anterior
                    AND KDIJ.C10 <= @fecha_final_year_anterior
                    AND KDIJ.C1 {regions}
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '21', '22', '25', '26')
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                GROUP BY 
                    KDIF.C1, 
                    KDIF.C2
            ) x ON aut.CLAVE = x.CLAVE
            ORDER BY aut.CLAVE;
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
