# Description: Consulta de ventas por faimilia en kilos sin refacturación
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consutlaVentasPorFamiliaKilosSinRefacturacion(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, producto_inicial, producto_final, familia_inicial, familia_final):
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, sucursal_inicial: {sucursal_inicial}, sucursal_final: {sucursal_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}, familia_inicial: {familia_inicial}, familia_final: {familia_final}")
    
    
    # Obtener los valores tanto de f_DifDias como de f_DifDiasTotales
    dif_dias = f_DifDias(fecha_inicial, fecha_final, [])
    dif_dias_totales = f_DifDiasTotales(fecha_inicial, fecha_final, [])
    
    # Convierte las cadenas a objetos datetime si es necesario
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
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s,
                @familia_inicial VARCHAR(20) = %s,
                @familia_final VARCHAR(20) = %s;
            
            WITH ventas_anterior AS (
                SELECT 
                    KDIF.C1 AS CLAVE,
                    KDIF.C2 AS FAMILIA,
                    SUM(KDIJ.C11 * KDII.C13) AS KG,
                    SUM(KDIJ.C11) AS UNID,
                    SUM(KDIJ.C14) AS VENTAS
                FROM 
                    KDIJ
                    INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                    INNER JOIN KDIF ON KDII.C82 = KDIF.C1
                WHERE 
                    KDII.C1 BETWEEN @producto_inicial AND @producto_final
                    AND KDIJ.C10 BETWEEN CONVERT(DATETIME, @fecha_inicial_year_anterior, 102) AND CONVERT(DATETIME, @fecha_final_year_anterior, 102)
                    AND KDIJ.C1 BETWEEN @sucursal_inicial AND @sucursal_final
                    AND KDIF.C1 BETWEEN @familia_inicial AND @familia_final
                    AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','21','22','25','26','71','72','73','74','75','76','77','78','79','80','81','82','86','87','88','94','96','97')
                GROUP BY 
                    KDIF.C1, KDIF.C2
            ),
            ventas_actual AS (
                SELECT 
                    KDIF.C1 AS CLAVE,
                    KDIF.C2 AS FAMILIA,
                    SUM(KDIJ.C11 * KDII.C13) AS KG,
                    SUM(KDIJ.C11) AS UNID,
                    SUM(KDIJ.C14) AS VENTAS
                FROM 
                    KDIJ
                    INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                    INNER JOIN KDIF ON KDII.C82 = KDIF.C1
                WHERE 
                    KDII.C1 BETWEEN @producto_inicial AND @producto_final
                    AND KDIJ.C10 BETWEEN CONVERT(DATETIME, @fecha_inicial, 102) AND CONVERT(DATETIME, @fecha_final, 102)
                    AND KDIJ.C1 BETWEEN @sucursal_inicial AND @sucursal_final
                    AND KDIF.C1 BETWEEN @familia_inicial AND @familia_final
                    AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN ('1','2','3','4','5','6','18','19','21','22','25','26','71','72','73','74','75','76','77','78','79','80','81','82','86','87','88','94','96','97')
                GROUP BY 
                    KDIF.C1, KDIF.C2
            )
            SELECT 
                COALESCE(aut.CLAVE, X.CLAVE) AS clave,
                LTRIM(RTRIM(COALESCE(aut.FAMILIA, X.FAMILIA))) AS familia,
                COALESCE(X.KG, 0) AS "venta_{last_year}",
                COALESCE(aut.KG, 0) AS "venta_{actual_year}",
                COALESCE((aut.KG - X.KG), aut.KG) AS diferencia,
                ((COALESCE(aut.KG, X.KG) / NULLIF(X.KG, 0)) - 1) * 100 AS "crecimiento_en_porcentaje",
                COALESCE(aut.KG, 0) / @Dias * @DiasTotales AS "estimado_mes"
            FROM ventas_anterior X
            FULL JOIN ventas_actual aut ON aut.CLAVE = X.CLAVE
            ORDER BY aut.CLAVE;       
        """

        params = [
                    dif_dias, dif_dias_totales,
                    fecha_inicial, fecha_final,
                    fecha_inicial_year_anterior, fecha_final_year_anterior,
                    producto_inicial, producto_final, 
                    sucursal_inicial, sucursal_final,
                    familia_inicial, familia_final
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