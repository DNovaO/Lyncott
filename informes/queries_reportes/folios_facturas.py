# Description: Consulta folio de facturas

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


def consultaFoliosFacturas(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final):
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, sucursal_inicial: {sucursal_inicial}, sucursal_final: {sucursal_final}")
    
        
    if sucursal_inicial == 'ALL' and sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDM1.C1 BETWEEN '02' AND '20'"
    elif sucursal_inicial == 'ALL':
        filtro_sucursal = f"AND KDM1.C1 BETWEEN '02' AND '20'"
    elif sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDM1.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDM1.C1 BETWEEN '{sucursal_inicial}' AND '{sucursal_final}'"
        
    with connection.cursor() as cursor:

        
        query = f"""
            DECLARE 
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s;

            SELECT
                KDM1.C6 AS folio,
                KDFECFDIVTA.C14 AS UUID,
                KDM1.C13 + KDM1.C16 AS subtotal,
                KDM1.C13 AS descuento,
                KDM1.C16 AS monto,
                CONVERT(VARCHAR, KDM1.c9, 103) AS fecha,
                CASE
                    WHEN KDM1.c43 = 'C' OR KDM1.c10 = '9999999' THEN 'Cancelado'
                    ELSE 'Activo'
                END AS estado,
                KDMS.C25 AS serie,
                KDUD.C10 AS RFC
            FROM
                KDM1
                LEFT JOIN KDMS ON KDMS.C1 = KDM1.C1
                LEFT JOIN KDUD ON KDUD.C2 = KDM1.c10
                LEFT JOIN KDFECFDIVTA 
                    ON KDFECFDIVTA.C1 = KDM1.C1
                    AND KDFECFDIVTA.C2 = KDM1.C2
                    AND KDFECFDIVTA.C3 = KDM1.C3
                    AND KDFECFDIVTA.C4 = KDM1.C4
                    AND KDFECFDIVTA.C5 = KDM1.C5
                    AND KDFECFDIVTA.C6 = KDM1.C6
            WHERE
                KDM1.C9 BETWEEN @fecha_inicial AND @fecha_final
                {filtro_sucursal}
                AND KDM1.c2 = 'U'
                AND KDM1.c3 = 'D'
                AND KDM1.c4 = '5'
            ORDER BY folio;

        """

        params = [
                    fecha_inicial, fecha_final,
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