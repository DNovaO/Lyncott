#Description: Consulta de ventas sin cargo
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaVentaSinCargo(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final):
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}, sucursal_inicial: {sucursal_inicial}, sucursal_final: {sucursal_final}")
    
    if sucursal_inicial == 'ALL' and sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDM2.C1 BETWEEN '02' AND '20'"
    elif sucursal_inicial == 'ALL':
        filtro_sucursal = f"AND KDM2.C1 BETWEEN '02' AND '20'"
    elif sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDM2.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDM2.C1 BETWEEN '{sucursal_inicial}' AND '{sucursal_final}'"

    
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
                DBKL2019.CLAVE AS clave,
                DBKL2019.PRODUCTO AS producto,
                DBKL2019.CANTIDAD AS cantidad,
                DBKL2019.UNI AS unidad,
                ISNULL(DBKL2019.KGSLTS, 0) AS kgslts,
                DBKL2019.UNID AS unidad_de_medida,
                ISNULL(DBKL2019.PESOS, 0) AS pesos, 
                (ISNULL(DBKL2019.PESOS, 0)) / (ISNULL(DBKL2019.CANTIDAD, 0)) AS precio_promedio
            FROM (
                SELECT 
                    KDII.C1 AS 'CLAVE',
                    KDII.C2 AS 'PRODUCTO',
                    ISNULL(SUM(KDM2.C9), 0) AS 'CANTIDAD',
                    KDII.C11 AS 'UNI',
                    ISNULL(SUM(KDM2.C9 * KDII.C13), 0) AS 'KGSLTS',
                    KDII.C12 AS 'UNID',
                    ISNULL(SUM(KDM2.C9 * KDM2.C12), 0) AS 'PESOS',
                    ISNULL(SUM(KDM2.C9 * KDM2.C12) / SUM(KDM2.C9), 0) AS 'PRECIOPROMEDIO'
                FROM KDM2
                INNER JOIN KDII ON KDM2.C8 = KDII.C1
                WHERE 
                    KDM2.C8 >= @producto_inicial
                    AND KDM2.C8 <= @producto_final
                    AND KDM2.C32 >= CONVERT(DATETIME, @fecha_inicial, 102)
                    AND KDM2.C32 <= CONVERT(DATETIME, @fecha_final, 102)
                    {filtro_sucursal}
                    AND KDM2.C25 >= @cliente_inicial
                    AND KDM2.C25 <= @cliente_final
                    AND KDM2.C2 = 'U'
                    AND KDM2.C3 = 'D'
                    AND KDM2.C4 = '5'
                    AND KDM2.C5 IN (27, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99)
                GROUP BY KDII.C1, KDII.C2, KDII.C11, KDII.C12
            ) AS DBKL2019;
        """

        params = [
            fecha_inicial, fecha_final,
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