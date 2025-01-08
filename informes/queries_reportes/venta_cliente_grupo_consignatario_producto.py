# Description: Consulta de Venta por Cliente, Grupo, Consignatario y Producto
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaVentaClienteGrupoConsignatarioProducto(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, grupoCorporativo_inicial, grupoCorporativo_final):
    
    if sucursal_inicial == 'ALL' and sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_inicial == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '{sucursal_inicial}' AND '{sucursal_final}'"

    if grupoCorporativo_inicial == 'ALL' and grupoCorporativo_final == 'ALL':
        filtro_grupoCorporativo = f"KDUD.C66 BETWEEN '' AND 'POSAD'"
    elif grupoCorporativo_inicial == 'ALL':
        filtro_grupoCorporativo = f"KDUD.C66 BETWEEN '' AND 'POSAD'"
    elif grupoCorporativo_final == 'ALL':
        filtro_grupoCorporativo = f"KDUD.C66 BETWEEN '' AND 'POSAD'"
    else:
        filtro_grupoCorporativo = f"KDUD.C66 BETWEEN '{grupoCorporativo_inicial}' AND '{grupoCorporativo_final}'"
    
    
    with connection.cursor() as cursor:
        query = f"""
            DECLARE 
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s,
                @grupoCorporativo_inicial VARCHAR(20) = %s,    
                @grupoCorporativo_final VARCHAR(20) = %s;

            WITH ClientesFiltrados AS (
                SELECT C2, C66 
                FROM KDUD 
                WHERE 
                {filtro_grupoCorporativo}
            )
            SELECT 
                LTRIM(RTRIM(KDIJ.C1)) + ' - ' + LTRIM(RTRIM(KDMS.C2)) AS 'sucursal',
                KDUD.C66 AS 'clave_grupo',
                ISNULL(KDCORPO.C2, '-Sin Grupo-') AS 'nombre_grupo',
                CASE 
                    WHEN KDUD.C33 = 'A' THEN '-A-' 
                    ELSE '-F-' 
                END AS 'giro',
                LTRIM(RTRIM(KDUD.C2)) + ' - ' + LTRIM(RTRIM(KDUD.C3)) AS 'cliente',
                KDSEGMENTACION.C2 AS 'segmento',
                KDM1.C181 AS 'clave_consignatario',
                KDVDIREMB.C3 AS 'nombre_consignatario',
                KDIF.C1 + ' - ' + KDIF.C2 AS 'familia',
                KDII.C1 AS 'clave_producto',
                KDII.C2 AS 'producto',
                ISNULL(SUM(KDIJ.C11 * KDII.C13), 0) AS 'venta_kg',
                ISNULL(SUM(KDIJ.C14), 0) AS 'venta_pesos',
                ISNULL(SUM(KDIJ.C11), 0) AS 'unidades'
            FROM
                KDIJ 
                INNER JOIN KDMS ON KDMS.C1 = KDIJ.C1
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1 
                LEFT JOIN KDUD ON KDIJ.C15 = KDUD.C2
                LEFT JOIN KDCORPO ON KDUD.C66 = KDCORPO.C1    
                INNER JOIN KDM1 ON KDIJ.C1 = KDM1.C1 
                    AND KDIJ.C4 = KDM1.C2 
                    AND KDIJ.C5 = KDM1.C3 
                    AND KDIJ.C6 = KDM1.C4 
                    AND KDIJ.C7 = KDM1.C5 
                    AND KDIJ.C8 = KDM1.C6
                LEFT JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 
                    AND KDM1.C181 = KDVDIREMB.C2
                LEFT JOIN KDIF ON KDIF.C1 = KDII.C5
                LEFT JOIN KDSEGMENTACION ON KDSEGMENTACION.C1 = KDVDIREMB.C78
                -- Join directo con los clientes filtrados
                FULL JOIN ClientesFiltrados CF ON KDUD.C2 = CF.C2
            WHERE  
                KDIJ.C10 BETWEEN @fecha_inicial AND @fecha_final
                {filtro_sucursal}
                AND KDIJ.C16 NOT IN (
                    '902', '903', '904', '905', '906', '907', '908', '909', '910', '911', 
                    '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', 
                    '922', '923', '924'
                )
                AND KDIJ.C4 = 'U'
                AND KDIJ.C5 = 'D'
                AND KDIJ.C6 IN ('5', '45')
                AND KDIJ.C7 IN (
                    '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26', 
                    '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', 
                    '86', '87', '88', '94', '96', '97'
                )
            GROUP BY 
                KDII.C1, KDII.C2, KDII.C11, KDIF.C1, KDIF.C2, KDII.C12, KDM1.C181, KDIJ.C1, 
                KDUD.C66, KDCORPO.C2, KDUD.C2, KDUD.C3, KDVDIREMB.C3, KDMS.C2, KDUD.C33, 
                KDSEGMENTACION.C2
            ORDER BY
                KDM1.C181, KDII.C1;
        """

        params = [
                    fecha_inicial, fecha_final,
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