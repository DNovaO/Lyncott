# Description: Consulta de ventas por producto sin refacturación
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaComparativoVentasProductoSinRefacturacion(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}, sucursal_inicial: {sucursal_inicial}, sucursal_final: {sucursal_final}")
    
    # Calcula las fechas del año anterior
    fecha_inicial_year_anterior = fecha_inicial.replace(year=fecha_inicial.year - 1)
    fecha_final_year_anterior = fecha_final.replace(year=fecha_final.year - 1)

    actual_year = str(fecha_inicial.year)
    last_year = str(fecha_inicial.year - 1)
    
    if sucursal_inicial == 'ALL' and sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_inicial == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '{sucursal_inicial}' AND '{sucursal_final}'"
    
    with connection.cursor() as cursor:
        query = f"""
            DECLARE 
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @fecha_inicial_year_anterior DATE = CONVERT(DATE, %s, 102),
                @fecha_final_year_anterior DATE = CONVERT(DATE, %s, 102),
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s,
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s;
            
            SELECT 
                LTRIM(RTRIM(ISNULL(A.CLAVE, B.CLAVE))) AS 'clave',
                LTRIM(RTRIM(ISNULL(A.PRODUCTO, B.PRODUCTO))) AS 'producto',
                ISNULL(B.CANTIDAD, 0) AS 'unidades_{last_year}',
                ISNULL(A.CANTIDAD, 0) AS 'unidades_{actual_year}',
                ISNULL(B.KGSLTS, 0) AS 'kgLts_{last_year}',
                ISNULL(A.KGSLTS, 0) AS 'kgLts_{actual_year}',
                ISNULL(B.VENTA, 0) AS 'venta_{last_year}',
                ISNULL(A.VENTA, 0) AS 'venta_{actual_year}',
                ISNULL(B.VENTA / B.KGSLTS, 0) AS 'venta_por_kgLts_{last_year}',
                ISNULL(B.VENTA / B.CANTIDAD, 0) AS 'venta_por_unidad_{last_year}',
                ISNULL(A.VENTA / A.KGSLTS, 0) AS 'venta_por_kgLts_{actual_year}',
                ISNULL(A.VENTA / A.CANTIDAD, 0) AS 'venta_por_unidad_{actual_year}'
            FROM (
                SELECT 
                    KDII.C1 AS CLAVE,
                    KDII.C2 AS PRODUCTO,
                    SUM(KDIJ.C11) AS CANTIDAD,
                    SUM(KDIJ.C11 * KDII.C13) AS KGSLTS,
                    SUM(KDIJ.C14) AS VENTA
                FROM KDIJ 
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1 
                INNER JOIN KDIF ON KDII.C5 = KDIF.C1 
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                WHERE 
                    KDII.C1 BETWEEN @producto_inicial AND @producto_final
                    AND KDIJ.C10 BETWEEN @fecha_inicial AND @fecha_final
                    {filtro_sucursal}
                    AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                    AND KDIJ.C16 NOT IN (
                        '902', '903', '904', '905', '906', '907', '908', '909', '910', 
                        '911', '912', '913', '914', '915', '916', '917', '918', '919', 
                        '920', '921', '922', '923', '924'
                    )
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN (
                        '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', 
                        '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', 
                        '79', '80', '81', '82', '86', '87', '88', '94', '96', '97'
                    )
                GROUP BY 
                    KDII.C1, 
                    KDII.C2
            ) AS A
            FULL JOIN (
                SELECT 
                    KDII.C1 AS CLAVE,
                    KDII.C2 AS PRODUCTO,
                    SUM(KDIJ.C11) AS CANTIDAD,
                    SUM(KDIJ.C11 * KDII.C13) AS KGSLTS,
                    SUM(KDIJ.C14) AS VENTA
                FROM KDIJ 
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1 
                INNER JOIN KDIF ON KDII.C5 = KDIF.C1 
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                WHERE 
                    KDII.C1 BETWEEN @producto_inicial AND @producto_final
                    AND KDIJ.C10 BETWEEN @fecha_inicial_year_anterior AND @fecha_final_year_anterior
                    {filtro_sucursal}
                    AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                    AND KDIJ.C16 NOT IN (
                        '902', '903', '904', '905', '906', '907', '908', '909', '910', 
                        '911', '912', '913', '914', '915', '916', '917', '918', '919', 
                        '920', '921', '922', '923', '924'
                    )
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN (
                        '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', 
                        '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', 
                        '79', '80', '81', '82', '86', '87', '88', '94', '96', '97'
                    )
                GROUP BY 
                    KDII.C1, 
                    KDII.C2
            ) AS B ON A.CLAVE = B.CLAVE;
                
        """

        # Definir los parámetros para las fechas
        params = [
                    fecha_inicial, fecha_final,
                    fecha_inicial_year_anterior, fecha_final_year_anterior,
                    cliente_inicial, cliente_final,
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
