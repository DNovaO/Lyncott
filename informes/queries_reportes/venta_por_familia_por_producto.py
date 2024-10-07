# Description: Consulta de ventas por familia por producto
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaVentaPorFamiliaPorProducto(fecha_inicial, fecha_final, region):
    
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
                
            SELECT 	AUT.CLAVE 														AS 'clave',
                    Aut.PRODUCTO 													AS 'producto',
                    ISNULL(x.VENTA,0)												AS 'venta_{last_year}_$',
                    ISNULL(aUt.VENTA,0)												AS 'venta_{actual_year}_$',
                    (ISNULL(aUT.VENTA,0)-ISNULL(x.VENTA,0))							AS 'diferencia_$',
                    ISNULL(x.KG,0)													AS 'venta_{last_year}_kg',
                    ISNULL(AUt.KG,0)												AS 'venta_{actual_year}_kg',
                    (ISNULL(x.KG,0)-ISNULL(AUt.KG,0))								AS 'diferencia_kg'
            FROM (
                    SELECT 	KDII.C1 									AS CLAVE,
                                    KDII.C2 									AS PRODUCTO,
                                    SUM(KDIJ.C11 * KDII.C13) 		AS KG,
                                    SUM(KDIJ.C14) 							AS VENTA
                            FROM			KDIJ
                                INNER JOIN	KDII ON KDIJ.C3 = KDII.C1
                            WHERE 	KDIJ.C10 >= @fecha_inicial
                                AND KDIJ.C10 <= @fecha_final
                                AND KDIJ.C1 {regions}
                                AND KDIJ.C4 = 'U'
                                AND KDIJ.C5 = 'D'
                                AND KDIJ.C6 IN ('5','45')
                                AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','21','22','25','26'/*,'71','72','73','74','75','76','77','78','79','80','81','82','86','87','88','94','96','97'*/)
                                AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                            GROUP BY KDII.C1, KDII.C2
                    
            ) AS aUT LEFT JOIN (
                SELECT 	KDII.C1 									AS CLAVE, 
                        KDII.C2 									AS PRODUCTO, 
                        SUM(KDIJ.C11*KDII.C13) 			AS KG, 
                        SUM(KDIJ.C14) 							AS VENTA
                FROM 			KDIJ 
                    INNER JOIN 	KDII ON KDIJ.C3=KDII.C1 
                WHERE 	KDIJ.C10 >= @fecha_inicial_year_anterior
                    AND KDIJ.C10 <= @fecha_final_year_anterior
                    AND KDIJ.C1 {regions}
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5','45')
                    AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','21','22','25','26'/*,'71','72','73','74','75','76','77','78','79','80','81','82','86','87','88','94','96','97'*/)
                    AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                GROUP BY KDII.C1, KDII.C2 
            ) AS  X ON AUT.CLAVE = X.CLAVE ORDER BY AUT.CLAVE
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
