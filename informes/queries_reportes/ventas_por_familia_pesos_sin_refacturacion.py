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


def consutlaVentasPorFamiliaPesosSinRefacturacion(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, producto_inicial, producto_final, familia_inicial, familia_final):
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

            SELECT 
                ISNULL(aut.CLAVE, X.CLAVE) AS clave,
                LTRIM(RTRIM(ISNULL(aut.GRUPO, X.GRUPO))) AS grupo,
                ISNULL(X.VENTA, 0) AS "venta_{last_year}",
                ISNULL(aut.VENTA, 0) AS "venta_{actual_year}",
                ISNULL((aut.VENTA - X.VENTA), aut.VENTA) AS diferencia,
                (((ISNULL(aut.VENTA, X.VENTA) / NULLIF(X.VENTA, 0)) - 1) * 100) AS "crecimiento_en_porcentaje",
                ISNULL(aut.VENTA, 0) / @Dias * @DiasTotales AS "estimado_mes",
                ISNULL(ISNULL(aut.VENTA, 0) / NULLIF(aut.KG, 0), 0) AS "precio_promedio",
                ISNULL(aut.KG, 0) AS "venta_kg_{actual_year}"
            FROM (
                SELECT 
                    KL2020.dbo.KDIF.C1 AS CLAVE,
                    KL2020.dbo.KDIF.C2 AS GRUPO,
                    SUM(KL2020.dbo.KDIJ.C11 * KL2020.dbo.KDII.C13) AS KG,
                    SUM(KL2020.dbo.KDIJ.C11) AS UNI,
                    SUM(KL2020.dbo.KDIJ.C14) AS VENTA,
                    SUM(KL2020.dbo.KDIJ.C14) / COUNT(KL2020.dbo.KDIJ.C14) AS PROMEDIO
                FROM 
                    KL2020.dbo.KDIJ
                    INNER JOIN KL2020.dbo.KDII ON KL2020.dbo.KDIJ.C3 = KL2020.dbo.KDII.C1
                    INNER JOIN KL2020.dbo.KDIF ON KL2020.dbo.KDII.C82 = KL2020.dbo.KDIF.C1
                WHERE 
                    KL2020.dbo.KDII.C1 >= @producto_inicial
                    AND KL2020.dbo.KDII.C1 <= @producto_final
                    AND KL2020.dbo.KDIJ.C10 >= CONVERT(DATETIME, @fecha_inicial_year_anterior, 102)
                    AND KL2020.dbo.KDIJ.C10 <= CONVERT(DATETIME, @fecha_final_year_anterior, 102)
                    AND KL2020.dbo.KDIJ.C1 >= @sucursal_inicial
                    AND KL2020.dbo.KDIJ.C1 <= @sucursal_final
                    AND KL2020.dbo.KDIF.C1 >= @familia_inicial
                    AND KL2020.dbo.KDIF.C1 <= @familia_final
                    AND KL2020.dbo.KDIJ.C4 = 'U'
                    AND KL2020.dbo.KDIJ.C5 = 'D'
                    AND KL2020.dbo.KDIJ.C6 IN ('5', '45')
                    AND KL2020.dbo.KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '21', '22', '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '86', '87', '88', '94', '96', '97')
                    AND KL2020.dbo.KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                GROUP BY 
                    KL2020.dbo.KDIF.C1, KL2020.dbo.KDIF.C2
            ) X
            FULL JOIN (
                SELECT 
                    KL2020.dbo.KDIF.C1 AS CLAVE,
                    KL2020.dbo.KDIF.C2 AS GRUPO,
                    SUM(KL2020.dbo.KDIJ.C11 * KL2020.dbo.KDII.C13) AS KG,
                    SUM(KL2020.dbo.KDIJ.C11) AS UNI,
                    SUM(KL2020.dbo.KDIJ.C14) AS VENTA
                FROM 
                    KL2020.dbo.KDIJ
                    INNER JOIN KL2020.dbo.KDII ON KL2020.dbo.KDIJ.C3 = KL2020.dbo.KDII.C1
                    INNER JOIN KL2020.dbo.KDIF ON KL2020.dbo.KDII.C82 = KL2020.dbo.KDIF.C1
                    INNER JOIN KL2020.dbo.KDUV ON KL2020.dbo.KDIJ.C16 = KDUV.C2
                WHERE 
                    KL2020.dbo.KDII.C1 >= @producto_inicial
                    AND KL2020.dbo.KDII.C1 <= @producto_final
                    AND KL2020.dbo.KDIJ.C10 >= CONVERT(DATETIME, @fecha_inicial, 102)
                    AND KL2020.dbo.KDIJ.C10 <= CONVERT(DATETIME, @fecha_final, 102)
                    AND KL2020.dbo.KDIJ.C1 >= @sucursal_inicial
                    AND KL2020.dbo.KDIJ.C1 <= @sucursal_final
                    AND KL2020.dbo.KDIF.C1 >= @familia_inicial
                    AND KL2020.dbo.KDIF.C1 <= @familia_final
                    AND KL2020.dbo.KDIJ.C4 = 'U'
                    AND KL2020.dbo.KDIJ.C5 = 'D'
                    AND KL2020.dbo.KDIJ.C6 IN ('5', '45')
                    AND KL2020.dbo.KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '21', '22', '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '86', '87', '88', '94', '96', '97')
                    AND KL2020.dbo.KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                GROUP BY 
                    KL2020.dbo.KDIF.C1, KL2020.dbo.KDIF.C2
            ) aut ON aut.CLAVE = X.CLAVE
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