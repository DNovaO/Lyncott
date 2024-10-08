#Description: Consulta de devoluciones por zona
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *

def consultaDevolucionesPorZona(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final):
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}")
    
    with connection.cursor() as cursor:
        query = f"""
            DECLARE
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @sucursal_inicial VARCHAR(2) = %s,
                @sucursal_final VARCHAR(2) = %s;
            
            SELECT
                CASE    
                    WHEN A.SUCURSAL IN ('02') THEN '1.-Vallejo'
                    WHEN A.SUCURSAL IN ('04', '15', '16', '17') THEN '2.-Norte'
                    WHEN A.SUCURSAL IN ('05', '08', '10', '19') THEN '3.-Centro'
                    WHEN A.SUCURSAL IN ('03', '09', '12', '14', '20') THEN '4.-Pacifico'
                    WHEN A.SUCURSAL IN ('07', '11', '13', '18') THEN '5.-Sureste'
                    ELSE 'sin zona'
                END AS zona,
                
                CASE    
                    WHEN A.SUCURSAL IN ('02') THEN
                        CASE    
                            WHEN A.VENDEDOR = 1 THEN '1 - Autoservicio'
                            WHEN A.VENDEDOR = 2 THEN '2 - Norte'
                            WHEN A.VENDEDOR = 3 THEN '3 - Sur'
                            WHEN A.VENDEDOR = 4 THEN '4 - Vent. Especiales'
                            WHEN A.VENDEDOR = 5 THEN '5 - Cadenas'
                            WHEN A.VENDEDOR = 6 THEN '6 - Centro'
                            ELSE 'sin asignar a Vallejo'
                        END
                    ELSE LTRIM(RTRIM(A.SUCURSAL)) + '-'
                END AS sucursal,
                SUM(ISNULL(A.NOTA, 0)) AS nota,
                SUM(ISNULL(A.DEVOLUCIONES, 0)) AS devoluciones,
                SUM(ISNULL(A.VENTAS, 0)) AS ventas,
                SUM(ISNULL(A.VENTAS, 0)) - SUM(ISNULL(A.NOTA, 0)) - SUM(ISNULL(A.DEVOLUCIONES, 0)) AS diferencia_pesos,
                (SUM(ISNULL(A.VENTAS, 0)) - SUM(ISNULL(A.NOTA, 0)) - SUM(ISNULL(A.DEVOLUCIONES, 0))) / 
                COALESCE(NULLIF(ISNULL(SUM(ISNULL(A.NOTA, 0)) + SUM(ISNULL(A.DEVOLUCIONES, 0)), 0), 0), 
                SUM(ISNULL(A.VENTAS, 0)) - SUM(ISNULL(A.NOTA, 0)) - SUM(ISNULL(A.DEVOLUCIONES, 0))) AS diferencia_porcentaje
            FROM (
                SELECT
                    KDIJ.C1 AS SUCURSAL,
                    CASE
                        WHEN KDIJ.C1 = '02' THEN KDUV.C22
                        ELSE ''
                    END AS VENDEDOR,
                    SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' THEN KDIJ.C14 END) AS VENTAS,
                    0 AS DEVOLUCIONES,
                    SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' THEN KDIJ.C14 END) AS NOTA
                FROM KDIJ
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                WHERE
                    KDIJ.C1 >= @sucursal_inicial
                    AND KDIJ.C1 <= @sucursal_final
                    AND KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND (
                        (KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' AND KDIJ.C6 IN ('5', '45') AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26'))
                        OR (KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 = '20' AND KDIJ.C7 IN ('24', '26'))
                    )
                GROUP BY KDIJ.C1, KDUV.C22
                UNION
                SELECT
                    KDIJ.C1 AS SUCURSAL,
                    CASE
                        WHEN KDIJ.C1 = '02' THEN KDUV.C22
                        ELSE ''
                    END AS VENDEDOR,
                    0 AS VENTAS,
                    SUM(CASE WHEN KDIJ.C4 = 'N' AND KDIJ.C5 = 'D' THEN KDIJ.C14 END) AS DEVOLUCIONES,
                    0 AS NOTA
                FROM KDIJ
                INNER JOIN KDUV ON KDIJ.C2 = KDUV.C24 AND KDIJ.C1 = KDUV.C1
                WHERE
                    KDIJ.C1 >= @sucursal_inicial
                    AND KDIJ.C1 <= @sucursal_final
                    AND KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND (KDIJ.C4 = 'N' AND KDIJ.C5 = 'D' AND KDIJ.C6 = '25' AND KDIJ.C7 = '12')
                GROUP BY KDIJ.C1, KDUV.C22
                UNION
                SELECT
                    KDIJ.C1 AS SUCURSAL,
                    CASE
                        WHEN KDIJ.C1 = '02' THEN KDUV.C22
                        ELSE ''
                    END AS VENDEDOR,
                    SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' THEN KDIJ.C14 END) AS VENTAS,
                    0 AS DEVOLUCIONES,
                    SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' THEN KDIJ.C14 END) AS NOTA
                FROM KDIJ
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                WHERE
                    KDIJ.C1 >= @sucursal_inicial
                    AND KDIJ.C1 <= @sucursal_final
                    AND KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND (
                        (KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' AND KDIJ.C6 IN ('5', '45') AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26'))
                        OR (KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 = '20' AND KDIJ.C7 IN ('24', '26'))
                    )
                GROUP BY KDIJ.C1, KDUV.C22
                UNION
                SELECT
                    KDIJ.C1 AS SUCURSAL,
                    CASE
                        WHEN KDIJ.C1 = '02' THEN KDUV.C22
                        ELSE ''
                    END AS VENDEDOR,
                    0 AS VENTAS,
                    SUM(CASE WHEN KDIJ.C4 = 'N' AND KDIJ.C5 = 'D' THEN KDIJ.C14 END) AS DEVOLUCIONES,
                    0 AS NOTA
                FROM KDIJ
                INNER JOIN KDUV ON KDIJ.C2 = KDUV.C24 AND KDIJ.C1 = KDUV.C1
                WHERE
                    KDIJ.C1 >= @sucursal_inicial
                    AND KDIJ.C1 <= @sucursal_final
                    AND KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND (KDIJ.C4 = 'N' AND KDIJ.C5 = 'D' AND KDIJ.C6 = '25' AND KDIJ.C7 = '12')
                GROUP BY KDIJ.C1, KDUV.C22
            ) AS A
            GROUP BY A.SUCURSAL, A.VENDEDOR
            ORDER BY 1, 2;
        """
        
        params = [
                fecha_inicial, fecha_final,
                sucursal_inicial, sucursal_final,
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
