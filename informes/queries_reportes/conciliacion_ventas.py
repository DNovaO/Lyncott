# Description: Consulta de conciliación de ventas
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaConciliacionVentas(fecha_inicial, fecha_final,cliente_inicial, cliente_final, vendedor_inicial, vendedor_final, sucursal, documento):
   
    if sucursal == "ALL":
        filtro_sucursal = f"AND KDMS.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDMS.C1 = '{sucursal}'" 
        
    if documento == "ALL":
        filtro_documento = "AND KDM1.C5 IN ('23', '24', '27')"
    else:
        filtro_documento = f"AND KDM1.C5 = '{documento}'"
   
    with connection.cursor() as cursor:
        query = f"""
                        DECLARE
                @fecha_inicial VARCHAR(20) = '2024-01-01',
                @fecha_final VARCHAR(20) = '2024-1-31',
                @cliente_inicial VARCHAR(20) =  '0000001',
                @cliente_final VARCHAR(20) = 'ZVM01',
                @vendedor_inicial VARCHAR(20) =  '101',
                @vendedor_final VARCHAR(20) = '978';
            
            SELECT 
                ISNULL(LTRIM(RTRIM(FACTURA.tipo_documento)), '') AS tipo_documento,
                ISNULL(LTRIM(RTRIM(FACTURA.folio_factura)), '') AS folio_factura,
                ISNULL(LTRIM(RTRIM(CONVERT(VARCHAR, FACTURA.fecha_factura, 101))), '') AS fecha_factura,
                ISNULL(LTRIM(RTRIM(FACTURA.vendedor_factura)), '') AS clave_vendedor,
                ISNULL(LTRIM(RTRIM(FACTURA.cliente_factura)), '') AS clave_cliente,
                ISNULL(LTRIM(RTRIM(NOMBRES.nombre_cliente)), '') AS nombre_cliente,
                FORMAT(ISNULL(FACTURA.venta_factura, 0), 'N2') AS venta_factura,
                
                ISNULL(LTRIM(RTRIM(REMISION.tipo_documento_remision)), '') AS tipo_documento_remision,
                ISNULL(LTRIM(RTRIM(REMISION.folio_remision)), '') AS folio_remision,
                ISNULL(LTRIM(RTRIM(CONVERT(VARCHAR, REMISION.fecha_remision, 101))), '') AS fecha_remision,
                ISNULL(LTRIM(RTRIM(REMISION.vendedor_remision)), '') AS clave_vendedor_remision,
                ISNULL(LTRIM(RTRIM(REMISION.cliente_remision)), '') AS clave_cliente_remision,
                ISNULL(LTRIM(RTRIM(NOMBRES_REM.nombre_cliente_remision)), '') AS nombre_cliente_remision,
                FORMAT(ISNULL(REMISION.venta_remision, 0), 'N2') AS venta_remision
            FROM (
                SELECT
                    KDM1.C5 AS tipo_documento,
                    KDM1.C6 AS folio_factura,
                    KDM1.C9 AS fecha_factura,
                    KDM1.C12 AS vendedor_factura,
                    KDM1.C10 AS cliente_factura,
                    (KDM1.C16 - KDM1.C15) AS venta_factura
                FROM KDM1
                    INNER JOIN KDMS ON KDM1.C1 = KDMS.C1
                    INNER JOIN KDUV ON KDM1.C12 = KDUV.C2
                    INNER JOIN KDUD ON KDM1.C10 = KDUD.C2
                WHERE
                    KDM1.C9 BETWEEN @fecha_inicial AND @fecha_final
                    AND KDM1.C2 = 'U'
                    AND KDM1.C3 = 'D'
                    AND KDM1.C4 = '5'
                    AND KDM1.C5 IN ('23', '24', '27')
                    AND KDUV.C2 BETWEEN @vendedor_inicial AND @vendedor_final
                    AND KDMS.C1  = '20'
                    AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                    AND KDUD.C2 != '9999999'
                    AND KDM1.C12 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                GROUP BY KDM1.C5, KDM1.C6, KDM1.C9, KDM1.C12, KDM1.C10, KDM1.C16, KDM1.C15
            ) AS FACTURA
            LEFT JOIN FULL OUTER JOIN (
                SELECT 
                    KDM1.C5 AS tipo_documento_remision,
                    KDM1.C6 AS folio_remision,
                    KDM1.C9 AS fecha_remision,
                    KDM1.C12 AS vendedor_remision,
                    KDM1.C10 AS cliente_remision,
                    (KDM1.C16 - KDM1.C15) AS venta_remision
                FROM KDM1
                    INNER JOIN KDMS ON KDM1.C1 = KDMS.C1
                    INNER JOIN KDUV ON KDM1.C12 = KDUV.C2
                    INNER JOIN KDUD ON KDM1.C10 = KDUD.C2
                WHERE
                    KDM1.C9 BETWEEN @fecha_inicial AND @fecha_final
                    AND KDM1.C2 = 'U'
                    AND KDM1.C3 = 'D'
                    AND KDM1.C4 = '45'
                    AND KDM1.C5 IN ('5', '6', '7')
                    AND KDUV.C2 BETWEEN @vendedor_inicial AND @vendedor_final
                    AND KDMS.C1 = '20'
                    AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                    AND KDUD.C2 <> '9999999'
                    AND KDM1.C12 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                GROUP BY KDM1.C5, KDM1.C6, KDM1.C9, KDM1.C12, KDM1.C10, KDM1.C16, KDM1.C15
            ) AS REMISION ON FACTURA.folio_factura = REMISION.folio_remision
            LEFT JOIN (
                SELECT C2, C3 AS nombre_cliente FROM KDUD
            ) AS NOMBRES ON NOMBRES.C2 = FACTURA.cliente_factura
            LEFT JOIN (
                SELECT C2, C3 AS nombre_cliente_remision FROM KDUD
            ) AS NOMBRES_REM ON NOMBRES_REM.C2 = REMISION.cliente_remision
        """
        
        # Definir los parámetros para las fechas y filtros
        params = [
            fecha_inicial, fecha_final,
            cliente_inicial, cliente_final, 
            vendedor_inicial, vendedor_final
        ]

        print(f"Parámetros de consulta: {params}")  # Imprimir los parámetros para depuración
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Convertir Decimals a float para evitar problemas al mostrar los datos
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result
