# Description: Consulta Analisis Ventas Vendedor
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


#INCOMPLETA
def consultaVentasCadenaFoodService(fecha_inicial, fecha_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final):
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}, sucursal_inicial: {sucursal_inicial}, sucursal_final: {sucursal_final}")
    
    fecha_inicial_year_anterior = fecha_inicial.replace(year=fecha_inicial.year - 1)
    fecha_final_year_anterior = fecha_final.replace(year=fecha_final.year - 1)

    actual_year = str(fecha_inicial.year)
    last_year = str(fecha_inicial.year - 1)

    with connection.cursor() as cursor:
        query = f"""
            DECLARE 
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @fecha_inicial_year_anterior DATE = CONVERT(DATE, %s, 102),
                @fecha_final_year_anterior DATE = CONVERT(DATE, %s, 102),
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s,
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s;
        SELECT * FROM(       
            SELECT 	 
                    CASE	WHEN A.CLAVE IN ('GALS01','GLIV','SHE01','GCMR01','GTO01') 		THEN 'Restaurante'
                            WHEN A.CLAVE IN ('GPOS01','GRIU01','GHPR01','GHNH01') 			THEN 'Hotel'
                            WHEN A.CLAVE IN ('GSEV01','ACM01','GGOM01') 					THEN 'Tiendas Conveniencia'
                            ELSE 'Sin grupo'
                    END 						AS 'grupo',
                    A.Clave 		AS 'clave',
                    
                    C.VENTA 		AS 'venta_mes_anterior_{last_year}',
                    B.VENTA 		AS 'ventas_{last_year}',
                    A.VENTA 		AS 'ventas_{actual_year}' 

            FROM(
                    SELECT	KDUD.C66 		AS CLAVE,
                            SUM(KDIJ.C14) 	AS VENTA,
                            GDUCORP.C2		AS DESCRIPCION
                    FROM				KDIJ 
                            INNER JOIN	KDII 	ON KDIJ.C3 = KDII.C1 
                            INNER JOIN	KDUD 	ON KDIJ.C15 = KDUD.C2
                            INNER JOIN	GDUCORP	ON KDUD.C66 = GDUCORP.C1
                    WHERE	
                        KDII.C1 >= @producto_inicial
                        AND KDII.C1 <= @producto_final
                        AND KDIJ.C10 >= @fecha_inicial
                        AND KDIJ.C10 <= @fecha_final
                        AND KDIJ.C1 >= @sucursal_inicial
                        AND KDIJ.C1 <= @sucursal_final
                        AND KDUD.C66 IN ('GALS01','GLIV','GCMR01','GTO01','GPOS01','GRIU01','GHPR01','GHNH01','GSEV01','GGOM01')
                        AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','917','918','919','920','921','922','923','924')
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                        AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','20','21','22','25','26','71','72','73','74','75','76','77','78','79','80','86','87','88','96','97')
                    GROUP BY KDUD.C66, GDUCORP.C2
                )AS A LEFT JOIN (
                    SELECT	KDUD.C66 		AS CLAVE,
                            SUM(KDIJ.C14) 	AS VENTA
                    FROM			KDIJ
                        INNER JOIN	KDII ON KDIJ.C3 = KDII.C1
                        INNER JOIN	KDUD ON KDIJ.C15 = KDUD.C2
                    WHERE	
                        KDII.C1 >= @producto_inicial
                        AND KDII.C1 <= @producto_final
                        AND KDIJ.C10 >= @fecha_inicial_year_anterior
                        AND KDIJ.C10 <= @fecha_final_year_anterior
                        AND KDIJ.C1 >= @sucursal_inicial
                        AND KDIJ.C1 <= @sucursal_final
                        AND KDUD.C66 IN ('GALS01','GLIV','GCMR01','GTO01','GPOS01','GRIU01','GHPR01','GHNH01','GSEV01','GGOM01')
                        AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','917','918','919','920','921','922','923','924')
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                        AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','20','21','22','25','26','71','72','73','74','75','76','77','78','79','80','86','87','88','96','97')
                    GROUP BY KDUD.C66
                ) AS B  ON A.Clave = B.Clave LEFT JOIN (
                    SELECT	KDUD.C66 AS CLAVE,
                            SUM(KDIJ.C14) AS VENTA
                    FROM			KDIJ
                        INNER JOIN	KDII ON KDIJ.C3 = KDII.C1
                        INNER JOIN	KDUD ON KDIJ.C15 = KDUD.C2
                    WHERE	
                        KDII.C1 >= @producto_inicial
                        AND KDII.C1 <= @producto_final
                        AND KDIJ.C10 >= @fecha_inicial_year_anterior
                        AND KDIJ.C10 <= @fecha_final_year_anterior
                        AND KDIJ.C1 >= @sucursal_inicial
                        AND KDIJ.C1 <= @sucursal_final
                        AND KDUD.C66 IN ('GALS01','GLIV','GCMR01','GTO01','GPOS01','GRIU01','GHPR01','GHNH01','GSEV01', 'GGOM01')
                        AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','917','918','919','920','921','922','923','924')
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                        AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','20','21','22','25','26','71','72','73','74','75','76','77','78','79','80','86','87','88','96','97')
                    GROUP BY KDUD.C66
                ) AS C ON a.Clave = C.Clave
            UNION
            SELECT 	CASE	WHEN D.Clave IN ('SHE01') 		THEN 'Restaurante'
                            WHEN D.Clave IN ('ACM01','MACD') 		THEN 'Tiendas Conveniencia'
                            ELSE 'Sin grupo'
                    END 			AS grupo,
                    D.Clave 		AS 'CLAVE',
                    F.VENTA			AS 'VENTA MES ANTERIOR anioAnt',
                    E.VENTA			AS 'VENTAS anioAnt',
                    D.VENTA			AS 'VENTAS anioAct' 
            FROM(
                    SELECT	KDUD.C66 		AS CLAVE,
                            SUM(KDIJ.C14) 	AS VENTA,
                            GDUCORP.C2		AS DESCRIPCION
                    FROM			KDIJ 
                        INNER JOIN	KDII 		ON KDIJ.C3 = KDII.C1 
                        INNER JOIN	KDUD 		ON KDIJ.C15 = KDUD.C2
                        INNER JOIN	GDUCORP	ON KDUD.C66 = GDUCORP.C1
                    WHERE	
                        KDII.C1 >= @producto_inicial
                        AND KDII.C1 <= @producto_final
                        AND KDIJ.C10 >= @fecha_inicial
                        AND KDIJ.C10 <= @fecha_final
                        AND KDIJ.C1 >= @sucursal_inicial
                        AND KDIJ.C1 <= @sucursal_final
                        AND KDUD.C66 IN ('SHE01','MACD','ACM01')
                        AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','917','918','919','920','921','922','923','924')
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                        AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','20','21','22','25','26','71','72','73','74','75','76','77','78','79','80','86','87','88','96','97')
                    GROUP BY KDUD.C66, GDUCORP.C2
                )AS D LEFT JOIN (
                    SELECT	KDUD.C66 		AS CLAVE,
                            SUM(KDIJ.C14) 	AS VENTA
                    FROM			KDIJ
                        INNER JOIN	KDII ON KDIJ.C3 = KDII.C1
                        INNER JOIN	KDUD ON KDIJ.C15 = KDUD.C2
                    WHERE	
                        KDII.C1 >= @producto_inicial
                        AND KDII.C1 <= @producto_final
                        AND KDIJ.C10 >= @fecha_inicial_year_anterior
                        AND KDIJ.C10 <= @fecha_final_year_anterior
                        AND KDIJ.C1 >= @sucursal_inicial
                        AND KDIJ.C1 <= @sucursal_final
                        AND KDUD.C66 IN ('SHE01','MACD','ACM01')
                        AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','917','918','919','920','921','922','923','924')
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                        AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','20','21','22','25','26','71','72','73','74','75','76','77','78','79','80','86','87','88','96','97')
                    GROUP BY KDUD.C66
                ) AS E  ON D.Clave = E.Clave LEFT JOIN (
                    SELECT	KDUD.C66 AS CLAVE,
                            SUM(KDIJ.C14) AS VENTA
                    FROM			KDIJ
                        INNER JOIN	KDII ON KDIJ.C3 = KDII.C1
                        INNER JOIN	KDUD ON KDIJ.C15 = KDUD.C2
                    WHERE	
                        KDII.C1 >= @producto_inicial
                        AND KDII.C1 <= @producto_final
                        AND KDIJ.C10 >= @fecha_inicial_year_anterior
                        AND KDIJ.C10 <= @fecha_final_year_anterior
                        AND KDIJ.C1 >= @sucursal_inicial
                        AND KDIJ.C1 <= @sucursal_final
                        AND KDUD.C66 IN ('SHE01','MACD','ACM01')
                        AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','917','918','919','920','921','922','923','924')
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                        AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','20','21','22','25','26','71','72','73','74','75','76','77','78','79','80','86','87','88','96','97')
                    GROUP BY KDUD.C66
                ) AS F ON D.Clave = F.Clave
            ) AS X
        """

        params = [
            fecha_inicial, fecha_final,
            fecha_inicial_year_anterior, fecha_final_year_anterior,
            producto_inicial, producto_final,
            sucursal_inicial, sucursal_final
        ]
        
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
