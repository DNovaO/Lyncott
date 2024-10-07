# Description: Consulta de ventas por zona en kilos y marca
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *

#Incompleta
def consultaComparativoNotasCreditoKilogramos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}")

    # Calcula las fechas del año anterior
    fecha_inicial_year_anterior = fecha_inicial.replace(year=fecha_inicial.year - 1)
    fecha_final_year_anterior = fecha_final.replace(year=fecha_final.year - 1)

    actual_year = str(fecha_inicial.year)
    last_year = str(fecha_inicial.year - 1)


    with connection.cursor() as cursor:
        query = f"""
            -- Declaración de variables
            DECLARE
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @fecha_inicial_year_anterior DATE = CONVERT(DATE, %s, 102),
                @fecha_final_year_anterior DATE = CONVERT(DATE, %s, 102), 
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s;
            
            SELECT     
                ISNULL(DB2019.ZONA, DB2018.ZONA) 																	AS zona,
                ISNULL(DB2019.SUC, DB2018.SUC) 																		AS clave_sucursal,
                ISNULL(DB2019.SUCURSALNOMBRE, DB2018.SUCURSALNOMBRE) 												AS sucursal,
                ISNULL(DB2018.NotaCredito,0)																		AS nota_credito_{last_year}_kg,
                ISNULL(DB2019.NotaCredito,0) 																		AS nota_credito_{actual_year}_kg,
                ISNULL(DB2019.NotaCredito,0) - ISNULL(DB2018.NotaCredito,0)											AS diferencia,
                ((ISNULL(DB2019.NotaCredito,0) / ISNULL(DB2018.NotaCredito,0))-1)*100								AS crecimiento_porcentual
            FROM (
                    SELECT 
                            DB2018.zona 																	AS ZONA,
                            DB2018.SUC 																		AS SUC,
                            DB2018.SUCURSALNOMBRE 															AS SUCURSALNOMBRE,
                            (SUM(ISNULL(DB2018.VENT, 0)) - SUM(ISNULL(DB2018.NotaCreditoConProducto,0))) 	AS NotaCredito
                    FROM (
                            SELECT 	
                                CASE	
                                    WHEN KDIJ.C1 IN ('02')					THEN '1.-Vallejo'
                                    WHEN KDIJ.C1 IN ('03','04','15','17')	THEN '2.-Norte'
                                    WHEN KDIJ.C1 IN ('05','08','10','16')	THEN '3.-Centro'
                                    WHEN KDIJ.C1 IN ('06','09','12','14')	THEN '4.-Pacifico'
                                    WHEN KDIJ.C1 IN ('07','11','13','18')	THEN '5.-Sureste'
                                    ELSE 'Sin zona'
                                END 					                                            AS 'ZONA',
                                CASE	
                                    WHEN KDIJ.C1 IN ('02')					THEN 	LTRIM(RTRIM(KDUV.C22))
                                    ELSE KDIJ.C1 
                                END						                                         AS 'SUC',
                                CASE	
                                    WHEN KDIJ.C1 IN ('02')   THEN 
                                            CASE	
                                                WHEN KDUV.C22 = 1			THEN 'Autoservicio'
                                                WHEN KDUV.C22 = 2			THEN 'Norte'
                                                WHEN KDUV.C22 = 3			THEN 'Sur'
                                                WHEN KDUV.C22 = 4			THEN 'Vent. Especiales'
                                                WHEN KDUV.C22 = 5			THEN 'Cadenas'
                                                ELSE 'sin asignar a Vallejo'
                                            END	
                                    ELSE LTRIM(RTRIM(KDMS.C2))	
                                END						                                         AS 'SUCURSALNOMBRE',
                                ISNULL(SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' AND KDIJ.C6 IN ('5','45')									THEN KDIJ.C11*KDII.C13 END),0) AS VENT,
                                ISNULL(SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 IN ('20') AND KDIJ.C7 IN ('24')		THEN KDIJ.C11*KDII.C13 END),0) AS NotaCreditoConProducto
                            FROM           KDIJ 
                                INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1 
                                INNER JOIN KDII ON KDIJ.C3 = KDII.C1 
                                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2 
                            WHERE	KDII.C1 >= @producto_inicial /*PInicial*/
                                AND KDII.C1 <= @producto_final /*PFinal*/
                                AND KDIJ.C10 >= @fecha_inicial_year_anterior
                                AND KDIJ.C10 <= @fecha_final_year_anterior
                                AND KDIJ.C15 >= @cliente_inicial /*CInicial*/
                                AND KDIJ.C15 <= @cliente_final /*CFinal*/
                                AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','917','918','919','921','922','923','924')  
                            GROUP BY KDUV.C22, KDIJ.C1, KDMS.C2
                    ) AS DB2018
                    GROUP BY DB2018.ZONA, DB2018.SUC, DB2018.SUCURSALNOMBRE
            ) AS 	DB2018 FULL JOIN (
                    SELECT
                            CASE	
                                WHEN ISNULL(DBV.SUC,DBL.SUC) IN ('02')					THEN '1.-Vallejo'
                                WHEN ISNULL(DBV.SUC,DBL.SUC) IN ('03','04','15','17')	THEN '2.-Norte'
                                WHEN ISNULL(DBV.SUC,DBL.SUC) IN ('05','08','10','16')	THEN '3.-Centro'
                                WHEN ISNULL(DBV.SUC,DBL.SUC) IN ('06','09','12','14')	THEN '4.-Pacifico'
                                WHEN ISNULL(DBV.SUC,DBL.SUC) IN ('07','11','13','18')	THEN '5.-Sureste'
                                ELSE 'Sin zona'
                            END 					                                            AS 'ZONA',
                            ISNULL(DBV.SUC,DBL.SUC)  									AS SUC,
                            ISNULL(DBV.SUCURSALNOMBRE,DBL.SUCURSALNOMBRE)  				AS SUCURSALNOMBRE,
                            ISNULL(DBV.NotaCredito,0) + ISNULL(DBL.NotaCredito,0)  		AS NotaCredito
                    FROM (
                                SELECT 
                                        DB2019.SUC 																		AS SUC,
                                        DB2019.SUCURSALNOMBRE 															AS SUCURSALNOMBRE,
                                        (SUM(ISNULL(DB2019.VENT, 0)) - SUM(ISNULL(DB2019.NotaCreditoConProducto,0))) 	AS NotaCredito
                                FROM (
                                        SELECT 	
                                            CASE	
                                                WHEN KDIJ.C1 IN ('02')					THEN 	LTRIM(RTRIM(KDUV.C22))
                                                ELSE KDIJ.C1 
                                            END						                                         AS 'SUC',
                                            CASE	
                                                WHEN KDIJ.C1 IN ('02')   THEN 
                                                        CASE	
                                                            WHEN KDUV.C22 = 1			THEN 'Autoservicio'
                                                            WHEN KDUV.C22 = 2			THEN 'Norte'
                                                            WHEN KDUV.C22 = 3			THEN 'Sur'
                                                            WHEN KDUV.C22 = 4			THEN 'Vent. Especiales'
                                                            WHEN KDUV.C22 = 5			THEN 'Cadenas'
                                                            ELSE 'sin asignar a Vallejo'
                                                        END	
                                                ELSE LTRIM(RTRIM(KDMS.C2))	
                                            END						                                         AS 'SUCURSALNOMBRE',
                                            ISNULL(SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' AND KDIJ.C6 IN ('5','45')									THEN KDIJ.C11*KDII.C13 END),0) AS VENT,
                                            ISNULL(SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 IN ('20') AND KDIJ.C7 IN ('24')	THEN KDIJ.C11*KDII.C13 END),0) AS NotaCreditoConProducto
                                        FROM           KDIJ 
                                            INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1 
                                            INNER JOIN KDII ON KDIJ.C3 = KDII.C1 
                                            INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2 
                                        WHERE	KDII.C1 >= @producto_inicial /*PInicial*/
                                            AND KDII.C1 <= @producto_final /*PFinal*/
                                            AND KDIJ.C10 >= @fecha_inicial /*FInicial*/
                                            AND KDIJ.C10 <= @fecha_final /*FFinal*/
                                            AND KDIJ.C15 >= @cliente_inicial /*CInicial*/
                                            AND KDIJ.C15 <= @cliente_final /*CFinal*/
                                            AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','917','918','919','921','922','923','924')  
                                        GROUP BY KDUV.C22, KDIJ.C1, KDMS.C2
                                ) AS DB2019
                                GROUP BY  DB2019.SUC, DB2019.SUCURSALNOMBRE
                    ) AS DBV  FULL JOIN (
                                SELECT 
                                        DBL2019.SUC 																	AS SUC,
                                        DBL2019.SUCURSALNOMBRE 															AS SUCURSALNOMBRE,
                                        (SUM(ISNULL(DBL2019.VENT, 0)) - SUM(ISNULL(DBL2019.NotaCreditoConProducto,0))) 	AS NotaCredito
                                FROM (
                                        SELECT 
                                            CASE	
                                                WHEN KDIJ.C1 IN ('02')					THEN 	LTRIM(RTRIM(KDUV.C22))
                                                ELSE KDIJ.C1 
                                            END						                                         																																		AS 'SUC',
                                            CASE	
                                                WHEN KDIJ.C1 IN ('02')   THEN 
                                                        CASE	
                                                            WHEN KDUV.C22 = 1			THEN 'Autoservicio'
                                                            WHEN KDUV.C22 = 2			THEN 'Norte'
                                                            WHEN KDUV.C22 = 3			THEN 'Sur'
                                                            WHEN KDUV.C22 = 4			THEN 'Vent. Especiales'
                                                            WHEN KDUV.C22 = 5			THEN 'Cadenas'
                                                            ELSE 'sin asignar a Vallejo'
                                                        END	
                                                ELSE LTRIM(RTRIM(KDMS.C2))	
                                            END						                                         																																		AS 'SUCURSALNOMBRE',
                                            ISNULL(SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' AND KDIJ.C6 IN ('5','45')									THEN KDIJ.C11*KDII.C13 END),0) 	AS VENT,
                                            ISNULL(SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 IN ('20') AND KDIJ.C7 IN ('24')	THEN KDIJ.C11*KDII.C13 END),0) 	AS NotaCreditoConProducto
                                        FROM           KDIJ 
                                            INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1 
                                            INNER JOIN KDII ON KDIJ.C3 = KDII.C1 
                                            INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2 
                                        WHERE	KDII.C1 >= @producto_inicial /*PInicial*/
                                            AND KDII.C1 <= @producto_final /*PFinal*/
                                            AND KDIJ.C10 >= @fecha_inicial
                                            AND KDIJ.C10 <= @fecha_final
                                            AND KDIJ.C15 >= @cliente_inicial /*CInicial*/
                                            AND KDIJ.C15 <= @cliente_final /*CFinal*/
                                            AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','917','918','919','921','922','923','924')  
                                        GROUP BY KDUV.C22, KDIJ.C1, KDMS.C2
                                ) AS DBL2019
                                GROUP BY   DBL2019.SUC, DBL2019.SUCURSALNOMBRE
                    ) AS DBL ON DBV.SUC = DBL.SUC
            ) AS 	DB2019 ON  DB2018.SUC = DB2019.SUC
        """

        params = [ 
                  fecha_inicial, fecha_final, 
                  fecha_inicial_year_anterior, fecha_final_year_anterior,
                  cliente_inicial, cliente_final, 
                  producto_inicial, producto_final
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