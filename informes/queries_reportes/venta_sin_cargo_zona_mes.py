# Description: Consulta de Venta sin Cargo por Zona Mes
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaVentaSinCargoPorZonaMes(fecha_inicial, fecha_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}")

    # Calcula las fechas del año anterior
    fecha_inicial_year_anterior = fecha_inicial.replace(year=fecha_inicial.year - 1)
    fecha_final_year_anterior = fecha_final.replace(year=fecha_final.year - 1)
    
        
    actual_year = str(fecha_inicial.year)
    last_year = str(fecha_inicial.year - 1)
    
    meses = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre"
    }
    
    mes = meses.get(fecha_inicial.month)
    
    
    with connection.cursor() as cursor:
        query = f"""
            SET LANGUAGE Español;

            DECLARE 
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @fecha_inicial_year_anterior DATE = CONVERT(DATE, %s, 102),
                @fecha_final_year_anterior DATE = CONVERT(DATE, %s, 102);

            SELECT 
                CASE    
                    WHEN COALESCE(A.ZONA, B.ZONA) IN ('02') THEN '1.-Vallejo'
                    WHEN COALESCE(A.ZONA, B.ZONA) IN ('17', '04', '15', '16') THEN '2.-Norte'
                    WHEN COALESCE(A.ZONA, B.ZONA) IN ('09', '14', '12', '03') THEN '3.-Centro'
                    WHEN COALESCE(A.ZONA, B.ZONA) IN ('05', '10', '08', '19') THEN '4.-Pacífico'
                    WHEN COALESCE(A.ZONA, B.ZONA) IN ('13', '11', '18', '07') THEN '5.-Sureste'
                    ELSE 'SIN ZONA'
                END AS zona,

                CASE    
                    WHEN COALESCE(A.ZONA, B.ZONA) IN ('02') THEN  
                        CASE    
                            WHEN COALESCE(A.SUCURSAL, B.SUCURSAL) = '1' THEN '1 - Autoservicio'
                            WHEN COALESCE(A.SUCURSAL, B.SUCURSAL) = '2' THEN '2 - Norte'
                            WHEN COALESCE(A.SUCURSAL, B.SUCURSAL) = '3' THEN '3 - Sur'
                            WHEN COALESCE(A.SUCURSAL, B.SUCURSAL) = '4' THEN '4 - Vent. Especiales'
                            WHEN COALESCE(A.SUCURSAL, B.SUCURSAL) = '5' THEN '5 - Cadenas'
                            ELSE 'SIN ASIGNAR A VALLEJO'
                        END 
                    ELSE COALESCE(A.ZONA, B.ZONA) + '-' + SUCURSALES.C2
                END AS sucursal,
                
                ISNULL(B.VENTA_YEAR_ANTERIOR, 0) AS venta_{mes}_{last_year},
                ISNULL(A.VENTA_ACTUAL, 0) AS venta_{mes}_{actual_year}
                
            FROM 
                (
                    SELECT 
                        LTRIM(RTRIM(KDM2.C1)) AS ZONA,   
                        CASE 
                            WHEN KDM2.C1 = '02' THEN LTRIM(RTRIM(KDUV.C22))
                            ELSE ''
                        END AS SUCURSAL,
                        SUM(KDM2.C13) AS VENTA_ACTUAL
                    FROM KDM2
                    INNER JOIN KDUV ON KDUV.C2 = KDM2.C27 
                    WHERE 
                        KDM2.C32 BETWEEN @fecha_inicial AND @fecha_final
                        AND KDM2.C2 = 'U'
                        AND KDM2.C3 = 'D'
                        AND KDM2.C4 = '5'
                        AND KDM2.C5 IN (
                            '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', 
                            '81', '82', '86', '87', '88', '91', '92', '93', '94', '95', 
                            '96', '97'
                        )
                        AND KDM2.C27 NOT IN (
                            '902', '903', '904', '905', '906', '907', '908', '909', '910', 
                            '911', '912', '913', '914', '915', '916', '917', '918', '919', 
                            '920', '921', '922', '923', '924'
                        )
                    GROUP BY KDUV.C22, KDM2.C1
                ) AS A
                FULL OUTER JOIN 
                (
                    SELECT 
                        LTRIM(RTRIM(KDM2.C1)) AS ZONA,   
                        CASE 
                            WHEN KDM2.C1 = '02' THEN LTRIM(RTRIM(KDUV.C22))
                            ELSE ''
                        END AS SUCURSAL,
                        SUM(KDM2.C13) AS VENTA_YEAR_ANTERIOR
                    FROM KDM2
                    INNER JOIN KDUV ON KDUV.C2 = KDM2.C27 
                    WHERE 
                        KDM2.C32 BETWEEN @fecha_inicial_year_anterior AND @fecha_final_year_anterior
                        AND KDM2.C2 = 'U'
                        AND KDM2.C3 = 'D'
                        AND KDM2.C4 = '5'
                        AND KDM2.C5 IN (
                            '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', 
                            '81', '82', '86', '87', '88', '91', '92', '93', '94', '95', 
                            '96', '97'
                        )
                        AND KDM2.C27 NOT IN (
                            '902', '903', '904', '905', '906', '907', '908', '909', '910', 
                            '911', '912', '913', '914', '915', '916', '917', '918', '919', 
                            '920', '921', '922', '923', '924'
                        )
                    GROUP BY KDUV.C22, KDM2.C1
                ) AS B
                    ON A.ZONA = B.ZONA AND A.SUCURSAL = B.SUCURSAL
                LEFT JOIN (
                    SELECT C1, C2 FROM KL2020.DBO.KDMS
                ) AS SUCURSALES 
                    ON COALESCE(A.ZONA, B.ZONA) = SUCURSALES.C1
            ORDER BY zona, sucursal;

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