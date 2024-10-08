# Description: Consulta de devolución por zona en kilos
from datetime import datetime, timedelta
from django.db.models import Value, CharField, OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaDevolucionPorZonaKilos(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, sucursal_inicial: {sucursal_inicial}, sucursal_final: {sucursal_final}")    

    query = f"""
            DECLARE 
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s;
        
            SELECT
                A.FAMILIA AS familia,
                SUM(ISNULL(A.NOTA, 0)) AS nota,
                SUM(ISNULL(A.DEVOLUCIONES, 0)) AS devolucion,
                SUM(ISNULL(A.VENTAS, 0)) AS venta,
                SUM(ISNULL(A.VENTAS, 0)) - SUM(ISNULL(A.NOTA, 0)) - SUM(ISNULL(A.DEVOLUCIONES, 0)) AS diferencia_kg,
                (SUM(ISNULL(A.VENTAS, 0)) - SUM(ISNULL(A.NOTA, 0)) - SUM(ISNULL(A.DEVOLUCIONES, 0))) / 
                COALESCE(NULLIF(ISNULL(SUM(ISNULL(A.NOTA, 0)) + SUM(ISNULL(A.DEVOLUCIONES, 0)), 0), 0), 
                SUM(ISNULL(A.VENTAS, 0)) - SUM(ISNULL(A.NOTA, 0)) - SUM(ISNULL(A.DEVOLUCIONES, 0))) AS diferencia_porcentaje
            FROM (
                SELECT
                    LTRIM(RTRIM(KDIF.C2)) AS FAMILIA,
                    SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' THEN KDIJ.C11 * KDII.C13 END) AS VENTAS,
                    0 AS DEVOLUCIONES,
                    SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' THEN KDIJ.C11 * KDII.C13 END) AS NOTA
                FROM
                    KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDIF ON KDII.C82 = KDIF.C1
                WHERE
                    KDIJ.C1 >= @sucursal_inicial
                    AND KDIJ.C1 <= @sucursal_final
                    AND KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND (
                        (/*VENT*/
                            KDIJ.C4 = 'U'
                            AND KDIJ.C5 = 'D'
                            AND KDIJ.C6 IN ('5', '45')
                            AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26')
                        )
                        OR (/*NOTA*/
                            KDIJ.C4 = 'U'
                            AND KDIJ.C5 = 'A'
                            AND KDIJ.C6 = '20'
                            AND KDIJ.C7 IN ('24', '26')
                        )
                    )
                GROUP BY KDIF.C2
                UNION
                SELECT
                    LTRIM(RTRIM(KDIF.C2)) AS FAMILIA,
                    0 AS VENTAS,
                    SUM(CASE WHEN KDIJ.C4 = 'N' AND KDIJ.C5 = 'D' THEN KDIJ.C11 * KDII.C13 END) AS DEVOLUCIONES,
                    0 AS NOTA
                FROM
                    KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDIF ON KDII.C82 = KDIF.C1
                WHERE
                    KDIJ.C1 >= @sucursal_inicial
                    AND KDIJ.C1 <= @sucursal_final
                    AND KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND (
                        (/*DEV*/
                            KDIJ.C4 = 'N'
                            AND KDIJ.C5 = 'D'
                            AND KDIJ.C6 = '25'
                            AND KDIJ.C7 = '12'
                        )
                    )
                GROUP BY KDIF.C2
                UNION
                SELECT
                    LTRIM(RTRIM(KDIF.C2)) AS FAMILIA,
                    SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' THEN KDIJ.C11 * KDII.C13 END) AS VENTAS,
                    0 AS DEVOLUCIONES,
                    SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' THEN KDIJ.C11 * KDII.C13 END) AS NOTA
                FROM
                    KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDIF ON KDII.C82 = KDIF.C1
                WHERE
                    KDIJ.C1 >= @sucursal_inicial
                    AND KDIJ.C1 <= @sucursal_final
                    AND KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND (
                        (/*VENT*/
                            KDIJ.C4 = 'U'
                            AND KDIJ.C5 = 'D'
                            AND KDIJ.C6 IN ('5', '45')
                            AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26')
                        )
                        OR (/*NOTA*/
                            KDIJ.C4 = 'U'
                            AND KDIJ.C5 = 'A'
                            AND KDIJ.C6 = '20'
                            AND KDIJ.C7 IN ('24', '26')
                        )
                    )
                GROUP BY KDIF.C2
                UNION
                SELECT
                    LTRIM(RTRIM(KDIF.C2)) AS FAMILIA,
                    0 AS VENTAS,
                    SUM(CASE WHEN KDIJ.C4 = 'N' AND KDIJ.C5 = 'D' THEN KDIJ.C11 * KDII.C13 END) AS DEVOLUCIONES,
                    0 AS NOTA
                FROM
                    KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDIF ON KDII.C82 = KDIF.C1
                WHERE
                    KDIJ.C1 >= @sucursal_inicial
                    AND KDIJ.C1 <=  @sucursal_final
                    AND KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND (
                        (/*DEV*/
                            KDIJ.C4 = 'N'
                            AND KDIJ.C5 = 'D'
                            AND KDIJ.C6 = '25'
                            AND KDIJ.C7 = '12'
                        )
                    )
                GROUP BY KDIF.C2
            ) AS A
            GROUP BY A.FAMILIA
            ORDER BY 1, 2;
    """

    params = [
        fecha_inicial, fecha_final,
        sucursal_inicial, sucursal_final
    ]

    # Imprimir los parámetros para depuración
    for param in params:
        print(param, type(param))

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Convertir valores Decimal a float
            for row in result:
                for key, value in row.items():
                    if isinstance(value, Decimal):
                        row[key] = float(value)

        return result

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []
