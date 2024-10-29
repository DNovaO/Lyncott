#Description: Consulta de Comparativo Precios, Reales vs Teoricos y Venta Simulada
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaComparativoPreciosRealesvsTeoricos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, sucursal_inicial, sucursal_final, grupoCorporativo_inicial, grupoCorporativo_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}, sucursal_inicial: {sucursal_inicial}, sucursal_final: {sucursal_final}, grupo_corporativo_inicial: {grupoCorporativo_inicial}, grupo_corporativo_final: {grupoCorporativo_final}")
    
    
    if sucursal_inicial == 'ALL' and sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_inicial == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '{sucursal_inicial}' AND '{sucursal_final}'"

    
    if grupoCorporativo_inicial == 'ALL' and grupoCorporativo_final == 'ALL':
        filtro_grupoCorporativo = f"AND KDUD.C66 BETWEEN '7 ELEV' AND 'POSAD'"
    elif grupoCorporativo_inicial == 'ALL':
        filtro_grupoCorporativo = f"AND KDUD.C66 BETWEEN '7 ELEV' AND 'POSAD'"
    elif grupoCorporativo_final == 'ALL':
        filtro_grupoCorporativo = f"AND KDUD.C66 BETWEEN '7 ELEV' AND 'POSAD'"
    else:
        filtro_grupoCorporativo = f"AND KDUD.C66 BETWEEN '{grupoCorporativo_inicial}' AND '{grupoCorporativo_final}'"
    
    with connection.cursor() as cursor:
        query = f"""
            SET LANGUAGE Español;

            DECLARE 
                @fecha_inicial VARCHAR(20) = %s,
                @fecha_final VARCHAR(20) = %s,
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s,
                @grupo_corporativo_inicial VARCHAR(20) = %s,
                @grupo_corporativo_final VARCHAR(20) = %s;

            SELECT 
                ISNULL(DBDBAlt.CLAVE, DBDBAct.CLAVE) AS clave,
                ISNULL(DBDBAlt.PRODUCTO, DBDBAct.PRODUCTO) AS producto,
                ISNULL(DBDBAlt.KGSLTS, DBDBAct.KGSLTS) AS venta_kg,
                ISNULL(DBDBAlt.VENTA, 0) + ISNULL(DBDBAct.VENTA, 0) AS venta_pesos,
                (ISNULL(DBDBAlt.VENTA, 0) + ISNULL(DBDBAct.VENTA, 0)) / 
                    (ISNULL(DBDBAlt.KGSLTS, 0) + ISNULL(DBDBAct.KGSLTS, 0)) AS 'pesos/kg',
                (ISNULL(DBDBAlt.PRECIO_VENTA, 0) + ISNULL(DBDBAct.PRECIO_VENTA, 0)) * 
                    (ISNULL(DBDBAlt.CANTIDAD, 0) + ISNULL(DBDBAct.CANTIDAD, 0)) AS venta_simulada_pesos,
                ISNULL(DBDBAlt.PRECIO_VENTA, 0) + ISNULL(DBDBAct.PRECIO_VENTA, 0) AS precio_lista,
                (ISNULL(DBDBAlt.PRECIO_VENTA, 0) + ISNULL(DBDBAct.PRECIO_VENTA, 0)) * 
                    (ISNULL(DBDBAlt.CANTIDAD, 0) + ISNULL(DBDBAct.CANTIDAD, 0)) / 
                    (ISNULL(DBDBAlt.KGSLTS, 0) + ISNULL(DBDBAct.KGSLTS, 0)) AS 'pesos/kg',
                (
                    (
                        (ISNULL(DBDBAlt.VENTA, 0) + ISNULL(DBDBAct.VENTA, 0)) 
                        / 
                        (ISNULL(DBDBAlt.KGSLTS, 0) + ISNULL(DBDBAct.KGSLTS, 0))
                        - 
                        (
                            (ISNULL(DBDBAlt.PRECIO_VENTA, 0) + ISNULL(DBDBAct.PRECIO_VENTA, 0))
                            * 
                            (ISNULL(DBDBAlt.CANTIDAD, 0) + ISNULL(DBDBAct.CANTIDAD, 0))
                            / 
                            (ISNULL(DBDBAlt.KGSLTS, 0) + ISNULL(DBDBAct.KGSLTS, 0))
                        )
                    )
                    / 
                    (
                        (ISNULL(DBDBAlt.PRECIO_VENTA, 0) + ISNULL(DBDBAct.PRECIO_VENTA, 0))
                        * 
                        (ISNULL(DBDBAlt.CANTIDAD, 0) + ISNULL(DBDBAct.CANTIDAD, 0))
                        / 
                        (ISNULL(DBDBAlt.KGSLTS, 0) + ISNULL(DBDBAct.KGSLTS, 0))
                    )
                ) * 100 AS teorico

            FROM (
                SELECT 
                    KDII.C1 AS CLAVE,
                    KDII.C2 AS PRODUCTO,
                    KDII.C14 AS PRECIO_VENTA,
                    SUM(KDIJ.C11) AS CANTIDAD,
                    KDII.C11 AS UNI,
                    SUM(KDIJ.C11 * KDII.C13) AS KGSLTS,
                    KDII.C12 AS UNID,
                    SUM(KDIJ.C14) AS VENTA
                FROM 
                    KDIJ 
                INNER JOIN 
                    KDII ON KDIJ.C3 = KDII.C1 
                INNER JOIN 
                    KDUD ON KDIJ.C15 = KDUD.C2
                INNER JOIN 
                    GDUCORP ON GDUCORP.C1 = KDUD.C66
                WHERE 
                    KDIJ.C10 >= CONVERT(DATETIME, @fecha_inicial, 102) /* FInicial */
                    AND KDIJ.C10 <= CONVERT(DATETIME, @fecha_final, 102) /* FFinal */
                    {filtro_sucursal}
                    AND KDUD.C2 >= @cliente_inicial /* CInicial */
                    AND KDUD.C2 <= @cliente_final /* CFinal */
                    {filtro_grupoCorporativo}
                    AND KDIJ.C16 NOT IN (
                        '902', '903', '904', '905', '906', '907', '908', '909',
                        '910', '911', '912', '913', '914', '915', '917', '918',
                        '919', '920', '921', '922', '923', '924'
                    )
                    AND KDIJ.C4 = 'U' 
                    AND KDIJ.C5 = 'D' 
                    AND KDIJ.C6 IN ('5', '45') 
                    AND KDIJ.C7 IN (
                        '1', '2', '3', '4', '5', '6', '18', '19', '20', '21',
                        '22', '25', '26', '71', '72', '73', '74', '75', '76',
                        '77', '78', '79', '80', '81', '82', '86', '87', '88',
                        '94', '96', '97'
                    )
                GROUP BY 
                    KDII.C1, 
                    KDII.C2, 
                    KDII.C14, 
                    KDII.C11, 
                    KDII.C12
            ) AS DBDBAct 
            FULL JOIN (
                SELECT 
                    KDII.C1 AS CLAVE,
                    KDII.C2 AS PRODUCTO,
                    KDII.C14 AS PRECIO_VENTA,
                    SUM(KDIJ.C11) AS CANTIDAD,
                    KDII.C11 AS UNI,
                    SUM(KDIJ.C11 * KDII.C13) AS KGSLTS,
                    KDII.C12 AS UNID,
                    SUM(KDIJ.C14) AS VENTA
                FROM 
                    KDIJ 
                INNER JOIN 
                    KDII ON KDIJ.C3 = KDII.C1 
                INNER JOIN 
                    KDUD ON KDIJ.C15 = KDUD.C2
                INNER JOIN 
                    KDCORPO ON KDCORPO.C1 = KDUD.C66
                WHERE 
                    KDIJ.C10 >= CONVERT(DATETIME, @fecha_inicial, 102)
                    AND KDIJ.C10 <= CONVERT(DATETIME, @fecha_final, 102)
                    {filtro_sucursal}
                    AND KDUD.C2 >= @cliente_inicial /* CInicial */
                    AND KDUD.C2 <= @cliente_final /* CFinal */
                    {filtro_grupoCorporativo}
                    AND KDIJ.C16 NOT IN (
                        '902', '903', '904', '905', '906', '907', '908', '909',
                        '910', '911', '912', '913', '914', '915', '917', '918',
                        '919', '920', '921', '922', '923', '924'
                    )
                    AND KDIJ.C4 = 'U' 
                    AND KDIJ.C5 = 'D' 
                    AND KDIJ.C6 IN ('5', '45') 
                    AND KDIJ.C7 IN (
                        '1', '2', '3', '4', '5', '6', '18', '19', '20', '21',
                        '22', '25', '26', '71', '72', '73', '74', '75', '76',
                        '77', '78', '79', '80', '81', '82', '86', '87', '88',
                        '94', '96', '97'
                    )
                GROUP BY 
                    KDII.C1, 
                    KDII.C2, 
                    KDII.C14, 
                    KDII.C11, 
                    KDII.C12
            ) AS DBDBAlt 
                ON DBDBAct.CLAVE = DBDBAlt.CLAVE
            ORDER BY 
                CLAVE;

        """

        params = [
                    fecha_inicial, fecha_final,
                    cliente_inicial, cliente_final,
                    sucursal_inicial, sucursal_final,
                    grupoCorporativo_inicial, grupoCorporativo_final
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