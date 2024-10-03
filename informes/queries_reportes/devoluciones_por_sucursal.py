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

#INCOMPLETO
def consultaDevolucionesPorSucursal(fecha_inicial, fecha_final):
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}")
    
    with connection.cursor() as cursor:
        query = f"""
            DECLARE @fecha_inicial VARCHAR(20) = %s,
                    @fecha_final VARCHAR(20) = %s;
            
            SELECT
                CASE    
                    WHEN A.SUCURSAL IN ('02')                     THEN '1.-Vallejo'
                    WHEN A.SUCURSAL IN ('17', '04', '15', '16')   THEN '2.-Norte'
                    WHEN A.SUCURSAL IN ('05', '10', '19', '08')   THEN '3.-Centro'
                    WHEN A.SUCURSAL IN ('09', '14', '03', '12')   THEN '4.-Pacífico'
                    WHEN A.SUCURSAL IN ('13', '11', '18', '07')   THEN '5.-Sureste'
                    ELSE 'Sin zona'
                END AS ZONA,
                --LTRIM(RTRIM(A.SUCURSAL)) + '-' + LTRIM(RTRIM(Sucursales.C2)) AS SUCURSAL,
                A.KILOS AS KILOS,
                A.PRECIO AS PRECIO
            FROM (
                SELECT
                    ISNULL(DBKV.SUCURSAL, DBKL.SUCURSAL) AS SUCURSAL,
                    ISNULL(TRY_CONVERT(DECIMAL(18, 2), DBKV.KILOS), 0) + ISNULL(TRY_CONVERT(DECIMAL(18, 2), DBKL.KILOS), 0) AS KILOS,
                    ISNULL(TRY_CONVERT(DECIMAL(18, 2), DBKV.PRECIO), 0) + ISNULL(TRY_CONVERT(DECIMAL(18, 2), DBKL.PRECIO), 0) AS PRECIO
                FROM (
                    SELECT 
                        KDIJ.C1 AS SUCURSAL,
                        SUM(ISNULL(TRY_CONVERT(DECIMAL(18, 2), KDIJ.C11) * TRY_CONVERT(DECIMAL(18, 2), KDII.C13), 0)) AS KILOS,
                        SUM(ISNULL(TRY_CONVERT(DECIMAL(18, 2), KDIJ.C11) * TRY_CONVERT(DECIMAL(18, 2), KDII.C14), 0)) AS PRECIO 
                    FROM 
                        KDIJ KDIJ
                        INNER JOIN KDII KDII ON KDIJ.C3 = KDII.C1
                        LEFT JOIN KDUV KDUV ON KDIJ.C2 = KDUV.C15
                    WHERE 
                        KDIJ.C10 >= CONVERT(DATETIME, @fecha_inicial, 102) /* Movimiento - fecha mínima */
                        AND KDIJ.C10 <= CONVERT(DATETIME, @fecha_final, 102) /* Movimiento - fecha máxima */
                        AND KDIJ.C4 = 'N' /* Movimiento - Género U=ventas, X=compras, N=otros */
                        AND KDIJ.C5 = 'D' /* Movimiento - Naturaleza A=entrada, D=salida */
                        AND KDIJ.C6 IN ('5', '11') /* Movimiento - Grupo de documento */
                        AND KDIJ.C7 = '21' /* Movimiento - Tipo de documento */
                        AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', 
                                            '909', '910', '911', '912', '913', '914', 
                                            '915', '916', '917', '918', '919', '920', 
                                            '921', '922', '923', '924') /* Movimiento - ID_Vendedor */
                    GROUP BY KDIJ.C1
                ) AS DBKV
                FULL JOIN (
                    SELECT 
                        KDIJ.C1 AS SUCURSAL,
                        SUM(ISNULL(TRY_CONVERT(DECIMAL(18, 2), KDIJ.C11) * TRY_CONVERT(DECIMAL(18, 2), KDII.C13), 0)) AS KILOS,
                        SUM(ISNULL(TRY_CONVERT(DECIMAL(18, 2), KDIJ.C11) * TRY_CONVERT(DECIMAL(18, 2), KDII.C14), 0)) AS PRECIO 
                    FROM 
                        KDIJ KDIJ
                        INNER JOIN KDII KDII ON KDIJ.C3 = KDII.C1
                        LEFT JOIN KDUV KDUV ON KDIJ.C2 = KDUV.C24
                    WHERE 
                        KDIJ.C10 >= CONVERT(DATETIME, @fecha_inicial, 102) /* Movimiento - fecha mínima */
                        AND KDIJ.C10 <= CONVERT(DATETIME, @fecha_final, 102) /* Movimiento - fecha máxima */
                        AND KDIJ.C4 = 'N' /* Movimiento - Género U=ventas, X=compras, N=otros */
                        AND KDIJ.C5 = 'D' /* Movimiento - Naturaleza A=entrada, D=salida */
                        AND KDIJ.C6 IN ('5', '11') /* Movimiento - Grupo de documento */
                        AND KDIJ.C7 = '21' /* Movimiento - Tipo de documento */
                        AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', 
                                            '909', '910', '911', '912', '913', '914', 
                                            '915', '916', '917', '918', '919', '920', 
                                            '921', '922', '923', '924') /* Movimiento - ID_Vendedor */
                    GROUP BY KDIJ.C1
                ) AS DBKL ON DBKL.SUCURSAL = DBKV.SUCURSAL
            ) AS A
            LEFT JOIN (
                SELECT 
                    C1, C2 
                FROM 
                    KDMS
            ) AS Sucursales ON A.SUCURSAL = Sucursales.C1;
        """
        
        params = [fecha_inicial, fecha_final]
        
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
