# Description: Consulta de ventas por crédito contable
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaVentasPorZonaKilos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, marca_inicial, marca_final):

    print(f"Consulta de ventas por zona en kilos desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial}, cliente final: {cliente_final}, producto inicial: {producto_inicial}, producto final: {producto_final}, marca inicial: {marca_inicial}, marca final: {marca_final}")
        
    with connection.cursor() as cursor:
        query = """
            SELECT 
                    ISNULL(ANTERIOR.ZONA,ACTUAL.ZONA) 									 										AS ZONA,
                    ISNULL(ANTERIOR.CLAVE,ACTUAL.CLAVE) 									 									AS CLAVE,
                    ISNULL(ANTERIOR.SUC,ACTUAL.SUC) 									 										AS SUC,
                    SUM(ISNULL(ANTERIOR.KILOS,0)) 								 												AS VENTA_ANTERIOR,
                    SUM(ISNULL(ACTUAL.KILOS,0)) 																				AS VENTA_ACtual,
                    SUM(ISNULL(ACTUAL.KILOS,0)) - SUM(ISNULL(ANTERIOR.KILOS,0))  													AS DIFERENCIA,
                    CASE	WHEN SUM(ISNULL(ANTERIOR.KILOS,0))= 0 THEN 
                                    CASE	WHEN SUM(ISNULL(ACTUAL.KILOS,0)) = 0 THEN 0
                                            ELSE 100
                                    END 
                            ELSE
                                    CASE	WHEN SUM(ISNULL(ACTUAL.KILOS,0)) = 0 THEN -100
                                            ELSE SUM(ISNULL(ACTUAL.KILOS,0))/SUM(ISNULL(ANTERIOR.KILOS,0))*100-100
                                    END
                    END																											AS 'DIFERENCIA EN %',
                    ISNULL(SUM(ISNULL(ACTUAL.KILOS,0)) / f_DifDias(%s,%s) * f_DifDiasTotales(%s,%s), 0) 		AS 'ESTIMADO MES',
                    CASE WHEN SUM(ISNULL(ACTUAL.KILOS,0)) = 0 THEN 0
                        ELSE SUM(ISNULL(ACTUAL.VENTA,0))/SUM(ISNULL(ACTUAL.KILOS,0)) 
                    END 	  		  																							AS PROMEDIO,
                    SUM(ISNULL(ACTUAL.KILOS, 0)) 																				AS 'VENTAS anioAct EN KILOS'
            FROM(
                    SELECT
                                    ZONA 									 				AS ZONA,
                                    CLAVE 										 			AS CLAVE,
                                    SUC 										 				AS SUC,
                                    SUM(ISNULL(VENT,0)) 							AS VENTA,				
                                    SUM(ISNULL(KILOS,0))							AS KILOS,
                                    (SUM(ISNULL(VENT,0)))/(SUM(ISNULL(CUENTA,0))) 						AS PROMEDIO
                            FROM(					
                                SELECT KL.ZONA,KL.CLAVE,KL.SUC,SUM(KL.VENT) AS VENT,SUM(KL.KILOS) AS KILOS,SUM(KL.CUENTA) AS CUENTA
                                FROM(
                                    SELECT 	
                                            CASE 	WHEN KDIJ.C1 = '02' then '<div hidden>1</div>Vallejo' 
                                                    WHEN KDIJ.C1 IN ('17','04','15','16')	THEN '<div hidden>2</div>Norte'
                                                    WHEN KDIJ.C1 IN ('05','10','19','08')	THEN '<div hidden>3</div>Centro'
                                                    WHEN KDIJ.C1 IN ('09','14','03','12','06','20')	THEN '<div hidden>4</div>Pacifico'
                                                    WHEN KDIJ.C1 IN ('13','11','18','07')	THEN '<div hidden>5</div>Sureste'
                                                    ELSE 'Sin zona' 
                                            END  		  															AS	 ZONA,
                                            CASE	WHEN KDIJ.C1 = '02' THEN   
                                                CASE    WHEN KDUV.C22 =1 THEN '1'
                                                        WHEN KDUV.C22 =2 THEN '2'
                                                        WHEN KDUV.C22 =3 THEN '3'
                                                        WHEN KDUV.C22 =4 THEN '4'
                                                        WHEN KDUV.C22 =5 THEN '5'
                                                        ELSE '6' --'sin asignar a Vallejo'
                                                END 
                                                WHEN KDIJ.C1 = '06' THEN   '12'
                                                ELSE LTRIM(RTRIM(KDIJ.C1)) 		            
                                            END 																	AS CLAVE,
                                            CASE	WHEN KDIJ.C1 = '02' THEN   
                                                        CASE    WHEN KDUV.C22 =1 THEN '1'
                                                                WHEN KDUV.C22 =2 THEN '2'
                                                                WHEN KDUV.C22 =3 THEN '3'
                                                                WHEN KDUV.C22 =4 THEN '4'
                                                                WHEN KDUV.C22 =5 THEN '5'
                                                                ELSE '6' --'sin asignar a Vallejo'
                                                        END
                                                    ELSE
                                                        CASE    WHEN KDUV.C22 =1 THEN '1'
                                                                WHEN KDUV.C22 =2 THEN '2'
                                                                WHEN KDUV.C22 =3 THEN '3'
                                                                WHEN KDUV.C22 =4 THEN '4'
                                                                WHEN KDUV.C22 =5 THEN '5'
                                                                ELSE 'sin asignar a Sucursal'
                                                        END		            
                                            END 																	AS Z_VEND,
                                            CASE	WHEN KDIJ.C1 = '02' THEN   
                                                        CASE    WHEN KDUV.C22 =1 THEN 'Autoservicio'
                                                                WHEN KDUV.C22 =2 THEN 'Norte'
                                                                WHEN KDUV.C22 =3 THEN 'Sur'
                                                                WHEN KDUV.C22 =4 THEN 'Vent. Especiales'
                                                                WHEN KDUV.C22 =5 THEN 'Cadenas'
                                                                ELSE 'Centro' --'sin asignar a Vallejo'
                                                        END 
                                                    WHEN KDIJ.C1 = '06' THEN   'Culiacan'
                                            ELSE LTRIM(RTRIM(KDMS.c2)) 
                                        END                                                          				AS SUC,
                                            SUM(KDIJ.C14) 												AS VENT,
                                            SUM(KDIJ.C11*KDII.C13) 							AS KILOS,
                                            COUNT(KDIJ.C14) 												AS CUENTA
                                    FROM 			KDIJ
                                        INNER JOIN	KDII ON KDIJ.C3 = KDII.C1
                                        INNER JOIN  KDIG ON KDII.C3 = KDIG.C1
                                        INNER JOIN 	KDMS ON KDIJ.C1 = KDMS.C1
                                        INNER JOIN	KDUV ON KDIJ.C16 = KDUV.C2
                                        INNER JOIN	KDUD ON KDIJ.C15 = KDUD.C2
                                    WHERE
                                            KDII.C1 >= %s /*PInicial*/
                                        AND KDII.C1 <= %s /*PFinal*/
                                        AND	KDIJ.C10 >= CONVERT(DATETIME, %s, 102) /*FInicial*/
                                        AND KDIJ.C10 <= CONVERT(DATETIME, %s, 102) /*FFinal*/
                                        AND KDUD.C2 >= %s /*CInicial*/
                                        AND KDUD.C2 <= %s /*CFinal*/
                                        AND KDIG.c1 >= %s /*MInicial*/
                                        AND KDIG.c1 <= %s /*MFinal*/
                                        AND KDIJ.C4 = 'U'
                                        AND KDIJ.C5 = 'D'
                                        AND KDIJ.C6 IN ('5','45')
                                        AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','20','21','22','25','26','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99')
                                        AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                                    GROUP BY KDIJ.C1, KDMS.C2, KDUV.C22
                                )AS KL GROUP BY KL.ZONA,KL.CLAVE,KL.SUC
                            ) AS DBKL2020 
                            GROUP BY ZONA, CLAVE, SUC
            ) AS ANTERIOR FULL JOIN (
                SELECT GRAL_ACT.ZONA, GRAL_ACT.CLAVE,GRAL_ACT.SUC,SUM(GRAL_ACT.VENTA) AS VENTA,SUM(GRAL_ACT.KILOS) AS KILOS,SUM(GRAL_ACT.PROMEDIO) AS PROMEDIO
                FROM(
                    -- sin asignar vallejo se cambia la segunda linea aquí
                    SELECT 	
                            CASE 	WHEN KDIJ.C1 = '02' then '<div hidden>1</div>Vallejo' 
                                    WHEN KDIJ.C1 IN ('17','04','15','16')	THEN '<div hidden>2</div>Norte'
                                    WHEN KDIJ.C1 IN ('05','10','19','08')	THEN '<div hidden>3</div>Centro'
                                    WHEN KDIJ.C1 IN ('09','14','03','12','06','20')	THEN '<div hidden>4</div>Pacifico'
                                    WHEN KDIJ.C1 IN ('13','11','18','07')	THEN '<div hidden>5</div>Sureste'
                                    ELSE 'Sin zona' 
                            END  		  															AS	 ZONA,
                            CASE	WHEN KDIJ.C1 = '02' THEN   
                                        CASE    WHEN KDUV.C22 =1 THEN '1'
                                                WHEN KDUV.C22 =2 THEN '2'
                                                WHEN KDUV.C22 =3 THEN '3'
                                                WHEN KDUV.C22 =4 THEN '4'
                                                WHEN KDUV.C22 =5 THEN '5'
                                                ELSE '6' --'sin asignar a Vallejo'
                                        END 
                                        WHEN KDIJ.C1 = '06' THEN   '12'
                                    ELSE LTRIM(RTRIM(KDIJ.C1)) 
                                END																	AS CLAVE,				
                            CASE	WHEN KDIJ.C1 = '02' THEN   
                                        CASE    WHEN KDUV.C22 =1 THEN 'Autoservicio'
                                                WHEN KDUV.C22 =2 THEN 'Norte'
                                                WHEN KDUV.C22 =3 THEN 'Sur'
                                                WHEN KDUV.C22 =4 THEN 'Vent. Especiales'
                                                WHEN KDUV.C22 =5 THEN 'Cadenas'
                                                ELSE 'Centro' --'sin asignar a Vallejo'
                                        END 
                                    WHEN KDIJ.C1 = '06' THEN   'Culiacan'
                            ELSE LTRIM(RTRIM(KDMS.c2)) 
                        END                                                          				AS SUC,
                            SUM(KDIJ.C14) 												AS VENTA,
                            SUM(KDIJ.C11*KDII.C13) 							AS KILOS,
                            SUM(KDIJ.C14)/COUNT(KDIJ.C14)						AS PROMEDIO
                    FROM 			KDIJ
                        INNER JOIN	KDII ON KDIJ.C3 = KDII.C1
                        INNER JOIN  KDIG ON KDII.C3 = KDIG.C1
                        INNER JOIN 	KDMS ON KDIJ.C1 = KDMS.C1
                        INNER JOIN	KDUV ON KDIJ.C16 = KDUV.C2
                        INNER JOIN	KDUD ON KDIJ.C15 = KDUD.C2
                        WHERE
                        KDII.C1 >= %s /*PInicial*/
                        AND KDII.C1 <= %s /*PFinal*/
                        AND	KDIJ.C10 >= CONVERT(DATETIME, %s, 102) /*FInicial*/
                        AND KDIJ.C10 <= CONVERT(DATETIME, %s, 102) /*FFinal*/
                        AND KDUD.C2 >= %s /*CInicial*/
                        AND KDUD.C2 <= %s /*CFinal*/
                        AND KDIG.c1 >= %s /*MInicial*/
                        AND KDIG.c1 <= %s /*MFinal*/
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND KDIJ.C6 IN ('5','45')
                        AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','20','21','22','25','26','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99')
                        AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    GROUP BY KDIJ.C1, KDMS.C2, KDUV.C22
                )AS GRAL_ACT
                GROUP BY GRAL_ACT.ZONA,GRAL_ACT.CLAVE,GRAL_ACT.SUC
            ) AS ACTUAL ON ANTERIOR.SUC = ACTUAL.SUC
            GROUP BY ANTERIOR.ZONA, ACTUAL.ZONA, ANTERIOR.CLAVE, ACTUAL.CLAVE, ANTERIOR.SUC, ACTUAL.SUC
            ORDER BY 1,2
        """

        params = [fecha_inicial, fecha_final, fecha_inicial, fecha_final, 
                  
                    producto_inicial, producto_final, 
                    fecha_inicial, fecha_final,
                    cliente_inicial, cliente_final,
                    marca_inicial, marca_final,
                    
                    producto_inicial, producto_final, 
                    fecha_inicial, fecha_final, cliente_inicial,
                    cliente_final, marca_inicial, marca_final,
    
                ]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        
    return result