# Description: Consulta de ventas por zona en kilos y marca
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaPorCliente(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}, sucursal_inicial: {sucursal_inicial}, sucursal_final: {sucursal_final}")

    if sucursal_inicial == 'ALL' and sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_inicial == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 between '02' AND '20'"
    elif sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 between '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '{sucursal_inicial}' AND '{sucursal_final}'"

    with connection.cursor() as cursor:
        query = f"""
            DECLARE
                @fecha_inicial VARCHAR(20) = %s,
                @fecha_final VARCHAR(20) = %s,
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s,
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s;
            
            SELECT 
                aut.CLAVE AS 'clave',
                aut.NombreCliente AS 'nombre_cliente',
                CASE aut.TipoCliente
                    WHEN 'A' THEN 'Autoservicio'
                    ELSE 'Food-Service'
                END AS 'tipo_cliente',
                ISNULL(aut.VENTA, 0) AS 'venta_pesos',
                ISNULL(aut.VENTA * 100 / Pegatina.PESOS, 0) AS 'porcentaje_venta',
                ISNULL(aut.KG, 0) AS 'venta_kilos',
                ISNULL(aut.KG * 100 / Pegatina.KILOS, 0) AS 'porcentaje_kilos'
            FROM (
                SELECT 
                    KDUD.C2 AS CLAVE,
                    LTRIM(RTRIM(KDUD.C3)) AS NombreCliente,
                    SUM(KDIJ.C14) AS VENTA,
                    SUM(KDIJ.C11 * KDII.C13) AS KG,
                    KDUD.C33 AS TipoCliente
                FROM KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                WHERE 
                    KDII.C1 BETWEEN @producto_inicial AND @producto_final
                    AND KDIJ.C10 BETWEEN CONVERT(DATETIME, @fecha_inicial, 102) AND CONVERT(DATETIME, @fecha_final, 102)
                    {filtro_sucursal}
                    AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '86', '87', '88', '96', '97')
                GROUP BY KDUD.C2, KDUD.C3, KDUD.C33
            ) AS aut
            LEFT JOIN (
                SELECT 
                    SUM(KDIJ.C14) AS PESOS,
                    SUM(KDIJ.C11 * KDII.C13) AS KILOS
                FROM KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                WHERE 
                    KDII.C1 BETWEEN @producto_inicial AND @producto_final
                    AND KDIJ.C10 BETWEEN CONVERT(DATETIME, @fecha_inicial, 102) AND CONVERT(DATETIME, @fecha_final, 102)
                    {filtro_sucursal}
                    AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                    AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '86', '87', '88', '96', '97')
            ) AS Pegatina ON 1 = 1
            ORDER BY aut.CLAVE, aut.NombreCliente;
        """

        params = [ fecha_inicial, fecha_final, 
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