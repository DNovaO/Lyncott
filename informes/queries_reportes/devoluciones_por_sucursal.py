#Description: Consulta de devoluciones por sucursal
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *

def consultaDevolucionesPorSucursal(fecha_inicial, fecha_final):
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}")
    
    with connection.cursor() as cursor:
        query = f"""
            DECLARE
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102);
            
            SELECT
                CASE
                    WHEN A.SUCURSAL IN ('02') THEN '1.-Vallejo'
                    WHEN A.SUCURSAL IN ('17', '04', '15', '16') THEN '2.-Norte'
                    WHEN A.SUCURSAL IN ('05', '10', '19', '08') THEN '3.-Centro'
                    WHEN A.SUCURSAL IN ('09', '14', '03', '12', '20') THEN '4.-Pacifico'
                    WHEN A.SUCURSAL IN ('13', '11', '18', '07') THEN '5.-Sureste'
                    ELSE 'Sin zona'
                END AS 'zona',
                LTRIM(RTRIM(A.SUCURSAL)) + '-' + LTRIM(RTRIM(Sucursales.C2)) AS sucursal,
                A.KILOS AS kilos,
                A.PRECIO AS precio
            FROM (
                SELECT
                    ISNULL(DBKL.SUCURSAL, 0) AS SUCURSAL,
                    ISNULL(DBKL.KILOS, 0) AS KILOS,
                    ISNULL(DBKL.PRECIO, 0) AS PRECIO
                FROM (
                    SELECT
                        KDIJ.C1 AS SUCURSAL,
                        ISNULL(SUM(KDIJ.C11 * KDII.C13), 0) AS KILOS,
                        ISNULL(SUM(KDIJ.C11 * KDII.C14), 0) AS PRECIO
                    FROM
                        KDIJ /*Movimiento*/
                    INNER JOIN KDII ON KDIJ.C3 = KDII.C1 /*Catálogo de productos*/
                    LEFT JOIN KDUV ON KDIJ.C2 = KDUV.C24 -- AND KDIJ.C1 = KDUV.C1
                    WHERE
                        KDIJ.C10 >= @fecha_inicial
                        AND KDIJ.C10 <= @fecha_final
                        AND KDIJ.C4 = 'N' /*Movimiento - Género U=ventas X=compras N=otros*/
                        AND KDIJ.C5 = 'D' /*Movimiento - Naturaleza A= entrada D=salida*/
                        AND KDIJ.C6 IN ('5', '11') --Movimiento - Grupo de documento
                        AND KDIJ.C7 = '21' --Movimiento - Tipo de documento (es el sub catalogo de KDIJ.C6)
                        AND KDIJ.C16 NOT IN (
                            '902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924'
                        ) --Movimiento - ID_Vendedor
                    GROUP BY KDIJ.C1, KDUV.C22
                ) AS DBKL
            ) AS A
            LEFT JOIN (
                SELECT KL2020.dbo.KDMS.C1, KL2020.dbo.KDMS.C2 FROM KL2020.dbo.KDMS
            ) AS Sucursales ON A.SUCURSAL = Sucursales.C1
            ORDER BY zona, sucursal;
        """
        
        params = [
                fecha_inicial, fecha_final,
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
