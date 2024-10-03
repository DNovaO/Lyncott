# Description: Consulta de Venta sin Cargo por Zona

#Description: Consulta de Comparativo Precios, Reales vs Teoricos y Venta Simulada
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaVentaSinCargoPorZona(fecha_inicial, fecha_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}")
    
        
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
            SET LANGUAGE Español;

            DECLARE 
                @fecha_inicial VARCHAR(20) = %s,
                @fecha_final VARCHAR(20) = %s,
                @fecha_inicial_year_anterior VARCHAR(20) = %s,
                @fecha_final_year_anterior VARCHAR(20) = %s;
                
            SELECT 
                    ISNULL(A.ZONA, B.ZONA)                                                          AS zona,
                    ISNULL(A.SUCURSAL, B.SUCURSAL)                                                  AS sucursal,
                    ISNULL(A.VENTA, 0) 											                    AS venta_anterior_{last_year},
                    ISNULL(B.VENTA, 0) 											                    AS venta_actual_{actual_year},
                    ISNULL(B.VENTA, 0)-ISNULL(A.VENTA,0) 						                    AS diferencia_en_pesos,
                    ((ISNULL(B.VENTA, 0)/ISNULL(A.VENTA,B.VENTA))-1)*100 				            AS diferencia_en_porcentaje
                    
            FROM (
                    SELECT 	
                            KDM2.C1 												AS 'ID_Zona',
                            KDUV.C22												AS 'ID_Sucursal',
                            '1.-Vallejo'									AS 'ZONA',
                            CASE	WHEN KDUV.C22 = 1 THEN 'Autoservicio'
                                    WHEN KDUV.C22 = 2 THEN 'Norte'
                                    WHEN KDUV.C22 = 3 THEN 'Sur'
                                    WHEN KDUV.C22 = 4 THEN 'Vent. Especiales'
                                    WHEN KDUV.C22 = 5 THEN 'Cadenas'
                                    WHEN KDUV.C22 IS NULL THEN 'Cadenas'
                                    WHEN KDUV.C22 ='' THEN 'Cadenas'
                                    ELSE 'sin asignar a Vallejo'
                            END																AS 'SUCURSAL',
                            sum (KDM2.C13)										AS 'VENTA'
                    FROM 			KDM2
                        INNER JOIN 	KDUV ON KDUV.C2  = KDM2.C27 
                    WHERE 
                                KDM2.C32 >= CONVERT(DATETIME, @fecha_inicial_year_anterior , 102)
                            AND KDM2.C32 <= CONVERT(DATETIME, @fecha_final_year_anterior , 102)
                            AND KDM2.C1 = '02'
                            AND KDM2.C2 = 'U'
                            AND KDM2.C3 = 'D'
                            AND KDM2.C4 = '5'
                            AND KDM2.C5 IN ('71','72','73','74','75','76','77','78','79','80','81','82','86','87','88','91','92','93','94','95','96','97','98','99')
                            AND KDM2.C27 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    GROUP BY KDUV.C22, KDM2.C1
                ) AS A FULL JOIN (
                                    SELECT 
                                            KDM2.C1 												AS 'ID_Zona',
                                            KDUV.C22												AS 'ID_Sucursal',
                                            'Vallejo' 									                    AS 'ZONA',
                                            CASE	WHEN KDUV.C22 = 1 THEN 'Autoservicio'
                                                    WHEN KDUV.C22 = 2 THEN 'Norte'
                                                    WHEN KDUV.C22 = 3 THEN 'Sur'
                                                    WHEN KDUV.C22 = 4 THEN 'Vent. Especiales'
                                                    WHEN KDUV.C22 = 5 THEN 'Cadenas'
                                                    WHEN KDUV.C22 IS NULL THEN 'Cadenas'
                                                    WHEN KDUV.C22 ='' THEN 'Cadenas'
                                                    ELSE 'sin asignar a Vallejo'
                                            END																AS 'SUCURSAL',
                                            sum (KDM2.C13)										AS 'VENTA'
                                    FROM 			KDM2
                                        INNER JOIN 	KDUV ON KDUV.C2  = KDM2.C27 
                                    WHERE 
                                                KDM2.C32 >= CONVERT(DATETIME, @fecha_inicial, 102)
                                            AND KDM2.C32 <= CONVERT(DATETIME, @fecha_final , 102)
                                            AND KDM2.C1 = '02'
                                            AND KDM2.C2 = 'U'
                                            AND KDM2.C3 = 'D'
                                            AND KDM2.C4 = '5'
                                            AND KDM2.C5 IN ('71','72','73','74','75','76','77','78','79','80','81','82','86','87','88','91','92','93','94','95','96','97','98','99')
                                            AND KDM2.C27 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                                    GROUP BY KDUV.C22, KDM2.C1
                            
                ) AS B ON B.ID_Zona = A.ID_Zona AND B.ID_Sucursal =A.ID_Sucursal
            UNION
            SELECT 
                    ISNULL(A.ZONA, B.ZONA)															            AS 'ZONA',
                    ISNULL(A.SUCURSAL, B.SUCURSAL) 																AS 'SUCURSAL',
                    ISNULL(A.VENTA, 0) 											                                AS 'VENTAS anioAnt',
                    ISNULL(B.VENTA, 0) 											                                AS 'VENTAS anioAct',
                    ISNULL(B.VENTA, 0)-ISNULL(A.VENTA,0) 						                                AS 'diferencia_en_pesos',
                    ((ISNULL(B.VENTA, 0)/ISNULL(A.VENTA,B.VENTA))-1)*100 				                        AS 'diferencia_en_porcentaje'
                    
                FROM (
                    SELECT 	
                            LTRIM(RTRIM(KDM2.C1)) 									AS 'ID_Zona',
                            
                            CASE	WHEN KDM2.C1 IN ('17','04','15','16')	THEN '2.-Norte'
                                    WHEN KDM2.C1 IN ('09','14','12','03','20')	THEN '3.-Pacifico'
                                    WHEN KDM2.C1 IN ('05','10','08','19')	THEN '4.-Centro'
                                    WHEN KDM2.C1 IN ('13','11','18','07')	THEN '5.-Sureste'
                                    ELSE 'Sin zona'
                            END 																AS 'ZONA',
                            KDMS.C2 													AS 'SUCURSAL',
                            sum (KDM2.C13)											AS 'VENTA'
                    FROM 			KDM2
                        INNER JOIN 	KDUV ON KDUV.C2  = KDM2.C27 
                        INNER JOIN 	KDMS ON KDMS.C1 = KDM2.C1 
                    WHERE 
                                KDM2.C32 >= CONVERT(DATETIME, @fecha_inicial_year_anterior , 102)
                            AND KDM2.C32 <= CONVERT(DATETIME, @fecha_final_year_anterior , 102)
                            AND KDM2.C1 <> '02'
                            AND KDM2.C2 = 'U'
                            AND KDM2.C3 = 'D'
                            AND KDM2.C4 = '5'
                            AND KDM2.C5 IN ('71','72','73','74','75','76','77','78','79','80','81','82','86','87','88','91','92','93','94','95','96','97','98','99')
                            AND KDM2.C27 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    GROUP BY  KDM2.C1,  KDMS.C2
                    
            ) AS A FULL JOIN (
                                SELECT 
                                    KDM2.C1 													AS 'ID_Zona',
                                    
                                    CASE	WHEN KDM2.C1 IN ('17','04','15','16')	THEN '2.-Norte'
                                            WHEN KDM2.C1 IN ('09','14','12','03','20')	THEN '3.-Pacifico'
                                            WHEN KDM2.C1 IN ('05','10','08','19')	THEN '4.-Centro'
                                            WHEN KDM2.C1 IN ('13','11','18','07')	THEN '5.-Sureste'
                                            ELSE 'Sin zona'
                                    END 																AS 'ZONA',
                                    KDMS.C2 													AS 'SUCURSAL',
                                    sum (KDM2.C13)											AS 'VENTA'
                                FROM 			KDM2
                                    INNER JOIN 	KDUV ON KDUV.C2  = KDM2.C27 
                                    INNER JOIN 	KDMS ON KDMS.C1 = KDM2.C1 
                                WHERE 
                                        KDM2.C32 >= CONVERT(DATETIME, @fecha_inicial , 102)
                                        AND KDM2.C32 <= CONVERT(DATETIME, @fecha_final , 102)
                                        AND KDM2.C1 <> '02'
                                        AND KDM2.C2 = 'U'
                                        AND KDM2.C3 = 'D'
                                        AND KDM2.C4 = '5'
                                        AND KDM2.C5 IN ('71','72','73','74','75','76','77','78','79','80','81','82','86','87','88','91','92','93','94','95','96','97','98','99')
                                        AND KDM2.C27 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                                GROUP BY KDM2.C1,  KDMS.C2
                            
            ) AS B ON B.ID_Zona = A.ID_Zona  
        """

        params = [
                    fecha_inicial, fecha_final,
                    fecha_inicial_year_anterior, fecha_final_year_anterior
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