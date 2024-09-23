# Description: Consulta de ventas por producto
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final, familia_inicial, familia_final):
    print(f"Consulta de ventas por producto desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}, sucursal inicial: {sucursal_inicial} y sucursal final: {sucursal_final}, familia inicial: {familia_inicial} y familia final: {familia_final}")

    with connection.cursor() as cursor:
        # Construcción dinámica de la consulta SQL
        query = """
            SELECT 
                dbo.KDII.C1 AS clave_producto,
                dbo.KDII.C2 AS producto,
                SUM(dbo.KDIJ.C11) AS cantidad,
                dbo.KDII.C11 AS tipo_unidad,
                SUM(dbo.KDIJ.C11 * dbo.KDII.C13) AS kgslts,
                dbo.KDII.C12 AS unidad_medida,
                SUM(dbo.KDIJ.C14) AS VENTA,
                SUM(dbo.KDIJ.C14) / SUM(dbo.KDIJ.C11 * dbo.KDII.C13) AS KG,
                SUM(dbo.KDIJ.C14) / SUM(dbo.KDIJ.C11) AS unidad_vendida
            FROM dbo.KDIJ
            INNER JOIN dbo.KDII ON dbo.KDIJ.C3 = dbo.KDII.C1
            INNER JOIN dbo.KDIF ON dbo.KDII.C5 = dbo.KDIF.C1
            INNER JOIN dbo.KDUD ON dbo.KDIJ.C15 = dbo.KDUD.C2
        """
        
        # Condicional para la tabla KDUV
        if sucursal_inicial == '02' and sucursal_final == '02':
            query += "INNER JOIN dbo.KDUV ON dbo.KDIJ.C16 = dbo.KDUV.C2 "

        query += """
            WHERE dbo.KDIF.C1 >= %s -- Familia Inicial
            AND dbo.KDIF.C1 <= %s -- Familia Final
            AND dbo.KDII.C1 >= %s -- Producto Inicial
            AND dbo.KDII.C1 <= %s -- Producto Final
            AND dbo.KDIJ.C1 >= %s -- Sucursal Inicial
            AND dbo.KDIJ.C1 <= %s -- Sucursal Final
            AND dbo.KDIJ.C10 >= %s -- Fecha Inicial
            AND dbo.KDIJ.C10 <= %s -- Fecha Final
            AND dbo.KDUD.C2 >= %s -- Cliente Inicial
            AND dbo.KDUD.C2 <= %s -- Cliente Final
            AND dbo.KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
            AND dbo.KDIJ.C4 = 'U'
            AND dbo.KDIJ.C5 = 'D'
            AND dbo.KDIJ.C6 IN ('5','45')
            AND dbo.KDIJ.C7 IN ('1','2','3','4','5','6','18','19','21','22','25','26','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97')
        """

        # Condicional para la zona si aplica
        if sucursal_inicial == '02' and sucursal_final == '02':
            query += "AND dbo.KDUV.C22 IN (%s) "

        query += """
            GROUP BY dbo.KDII.C1, dbo.KDII.C2, dbo.KDII.C11, dbo.KDII.C12
            ORDER BY dbo.KDII.C1;
        """

        # Parámetros para la consulta
        params = [
            familia_inicial, familia_final, producto_inicial, producto_final, 
            sucursal_inicial, sucursal_final, fecha_inicial, fecha_final, 
            cliente_inicial, cliente_final
        ]

        # Ejecutar la consulta
        cursor.execute(query, params)

        # Obtener los resultados
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
    
    return result