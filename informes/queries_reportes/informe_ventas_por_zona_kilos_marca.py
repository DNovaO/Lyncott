# Description: Consulta de ventas por crédito contable
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaVentasPorZonaKilosMarca(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, marca_inicial, marca_final):

    print(f"Consulta de ventas por zona en kilos desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial}, cliente final: {cliente_final}, producto inicial: {producto_inicial}, producto final: {producto_final}, marca inicial: {marca_inicial}, marca final: {marca_final}")
    
    # Obtener los valores tanto de f_DifDias como de f_DifDiasTotales
    dif_dias = f_DifDias(fecha_inicial, fecha_final, [])
    dif_dias_totales = f_DifDiasTotales(fecha_inicial, fecha_final, [])
        
    print('Diferencia de días:', dif_dias)
    print('Diferencia de días totales:', dif_dias_totales)
    
    if isinstance(fecha_inicial, str):
        fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d')

    if isinstance(fecha_final, str):
        fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d')

    # Calcula las fechas del año anterior
    fecha_inicial_year_anterior = fecha_inicial.replace(year=fecha_inicial.year - 1)
    fecha_final_year_anterior = fecha_final.replace(year=fecha_final.year - 1)
    
    actual_year = str(fecha_inicial.year)
    last_year = str(fecha_inicial.year - 1)

    with connection.cursor() as cursor:
        query = f"""
            DECLARE @Dias INT = %s,
                    @DiasTotales INT = %s,
                    @fecha_inicial VARCHAR(20) = %s,
                    @fecha_final VARCHAR(20) = %s,
                    @fecha_inicial_year_anterior VARCHAR(20) = %s,
                    @fecha_final_year_anterior VARCHAR(20) = %s,
                    @producto_inicial VARCHAR(20) = %s,
                    @producto_final VARCHAR(20) = %s,
                    @cliente_inicial VARCHAR(20) = %s,
                    @cliente_final VARCHAR(20) = %s,
                    @marca_inicial VARCHAR(20) = %s,
                    @marca_final VARCHAR(20) = %s;

            SELECT 
                ISNULL(ANTERIOR.ZONA, ACTUAL.ZONA) AS zona,
                ISNULL(ANTERIOR.CLAVE, ACTUAL.CLAVE) AS clave,
                ISNULL(ANTERIOR.SUC, ACTUAL.SUC) AS sucursal,
                SUM(ISNULL(ANTERIOR.KILOS, 0)) AS venta_anterior_{last_year},
                SUM(ISNULL(ACTUAL.KILOS, 0)) AS venta_actual_{actual_year},
                SUM(ISNULL(ACTUAL.KILOS, 0)) - SUM(ISNULL(ANTERIOR.KILOS, 0)) AS diferencia_en_kg,
                
                CASE 
                    WHEN SUM(ISNULL(ANTERIOR.KILOS, 0)) = 0 THEN 
                        CASE 
                            WHEN SUM(ISNULL(ACTUAL.KILOS, 0)) = 0 THEN 0
                            ELSE 100
                        END 
                    ELSE 
                        CASE 
                            WHEN SUM(ISNULL(ACTUAL.KILOS, 0)) = 0 THEN -100
                            ELSE SUM(ISNULL(ACTUAL.KILOS, 0)) / SUM(ISNULL(ANTERIOR.KILOS, 0)) * 100 - 100
                        END
                END AS 'diferencia_en_porcentaje',
                
                ISNULL(SUM(ISNULL(ACTUAL.KILOS, 0)) / @Dias * @DiasTotales, 0) AS 'estimado_mes',
                
                CASE 
                    WHEN SUM(ISNULL(ACTUAL.KILOS, 0)) = 0 THEN 0
                    ELSE SUM(ISNULL(ACTUAL.VENTA, 0)) / SUM(ISNULL(ACTUAL.KILOS, 0)) 
                END AS promedio
                
                -- SUM(ISNULL(ACTUAL.KILOS, 0)) AS 'ventas_año_actual_en_kilos'
            FROM(
                SELECT
                        DBKL2020.ZONA AS ZONA,
                        DBKL2020.CLAVE AS CLAVE,
                        DBKL2020.SUC AS SUC,
                        SUM(ISNULL(DBKL2020.VENT,0)) AS VENTA,				
                        SUM(ISNULL(DBKL2020.KILOS,0)) AS KILOS,
                        (SUM(ISNULL(DBKL2020.VENT,0)))/(SUM(ISNULL(DBKL2020.CUENTA,0))) AS PROMEDIO
                        FROM(					
                            SELECT KL.ZONA,KL.CLAVE,KL.SUC,SUM(KL.VENT) AS VENT,SUM(KL.KILOS) AS KILOS,SUM(KL.CUENTA) AS CUENTA
                            FROM(
                                SELECT 	
                                        CASE 	WHEN KDIJ.C1 = '02' then '1.-Vallejo' 
                                                WHEN KDIJ.C1 IN ('17','04','15','16')	THEN '2.-Norte'
                                                WHEN KDIJ.C1 IN ('05','10','19','08')	THEN '3.-Centro'
                                                WHEN KDIJ.C1 IN ('09','14','03','12','06','20')	THEN '4.-Pacifico'
                                                WHEN KDIJ.C1 IN ('13','11','18','07')	THEN '5.-Sureste'
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
                                        KDII.C1 >= @producto_inicial /*PInicial*/
                                    AND KDII.C1 <= @producto_final /*PFinal*/
                                    AND	KDIJ.C10 >= CONVERT(DATETIME, @fecha_inicial_year_anterior, 102) /*FInicial*/
                                    AND KDIJ.C10 <= CONVERT(DATETIME, @fecha_final_year_anterior, 102) /*FFinal*/
                                    AND KDUD.C2 >= @cliente_inicial /*CInicial*/
                                    AND KDUD.C2 <= @cliente_final /*CFinal*/
                                    AND KDIG.c1 >= @marca_inicial /*MInicial*/
                                    AND KDIG.c1 <= @marca_final /*MFinal*/
                                    AND KDIJ.C4 = 'U'
                                    AND KDIJ.C5 = 'D'
                                    AND KDIJ.C6 IN ('5','45')
                                    AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','20','21','22','25','26','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99')
                                    AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                                GROUP BY KDIJ.C1, KDMS.C2, KDUV.C22
                            )AS KL GROUP BY KL.ZONA,KL.CLAVE,KL.SUC
                        ) AS DBKL2020 
                        GROUP BY DBKL2020.ZONA, DBKL2020.CLAVE, DBKL2020.SUC
        ) AS ANTERIOR FULL JOIN (
            SELECT GRAL_ACT.ZONA, GRAL_ACT.CLAVE,GRAL_ACT.SUC,SUM(GRAL_ACT.VENTA) AS VENTA,SUM(GRAL_ACT.KILOS) AS KILOS,SUM(GRAL_ACT.PROMEDIO) AS PROMEDIO
            FROM(
                -- sin asignar vallejo se cambia la segunda linea aquí
                SELECT 	
                        CASE 	WHEN KDIJ.C1 = '02' then '1.-Vallejo' 
                                WHEN KDIJ.C1 IN ('17','04','15','16')	THEN '2.-Norte'
                                WHEN KDIJ.C1 IN ('05','10','19','08')	THEN '3.-Centro'
                                WHEN KDIJ.C1 IN ('09','14','03','12','06','20')	THEN '4.-Pacifico'
                                WHEN KDIJ.C1 IN ('13','11','18','07')	THEN '5.-Sureste'
                                ELSE 'Sin zona' 
                        END AS ZONA,
                        
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
                        END AS CLAVE,
                            				
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
                        KDII.C1 >= @producto_inicial /*PInicial*/
                    AND KDII.C1 <= @producto_final /*PFinal*/
                    AND	KDIJ.C10 >= CONVERT(DATETIME, @fecha_inicial, 102) /*FInicial*/
                    AND KDIJ.C10 <= CONVERT(DATETIME, @fecha_final, 102) /*FFinal*/
                    AND KDUD.C2 >= @cliente_inicial /*CInicial*/
                    AND KDUD.C2 <= @cliente_final /*CFinal*/
                    AND KDIG.c1 >= @marca_inicial /*MInicial*/
                    AND KDIG.c1 <= @marca_final /*MFinal*/
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

        params = [
                    dif_dias, dif_dias_totales,
                    fecha_inicial, fecha_final,
                    fecha_inicial_year_anterior, fecha_final_year_anterior,
                    producto_inicial, producto_final, 
                    cliente_inicial, cliente_final,
                    marca_inicial, marca_final
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