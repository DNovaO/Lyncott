# Description: Queries para el reporte de ventas por familia en kilos con refacturación.
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection


def consultaVentasPorFamiliaKgConRefacturacion(fecha_inicial, fecha_final, producto_inicial, producto_final, familia_inicial, familia_final, sucursal):
    print(f"Consulta de ventas por familia en kilos con refacturación desde {fecha_inicial} hasta {fecha_final}, producto inicial: {producto_inicial} y producto final: {producto_final}, familia inicial: {familia_inicial} y familia final: {familia_final}, sucursal: {sucursal}")
    
    # Si la sucursal es 'ALL', ajustamos el rango de sucursal
    if sucursal == "ALL":
        sucursal_inicial = '01'
        sucursal_final = '20'
    else:
        sucursal_inicial = sucursal
        sucursal_final = sucursal

    with connection.cursor() as cursor:
        query = """ 
            SELECT 
                dbo.KDIF.C1 AS familia, 
                dbo.KDIF.C2 AS descripcion_familia,  
                SUM(dbo.KDIJ.C11) AS unidad, 
                SUM(dbo.KDIJ.C11 * dbo.KDII.C13) AS kg, 
                SUM(dbo.KDIJ.C14) AS ventas
            FROM dbo.KDIJ
                INNER JOIN dbo.KDII ON dbo.KDIJ.C3 = dbo.KDII.C1
                INNER JOIN dbo.KDIF ON dbo.KDII.C5 = dbo.KDIF.C1
                INNER JOIN dbo.KDUV ON dbo.KDIJ.C16 = dbo.KDUV.C2
            WHERE dbo.KDIF.C1 >= %s -- Familia inicial
                AND dbo.KDIF.C1 <= %s -- Familia final
                AND dbo.KDII.C1 >= %s -- Producto inicial
                AND dbo.KDII.C1 <= %s -- Producto final
                AND dbo.KDIJ.C1 >= %s -- Sucursal inicial
                AND dbo.KDIJ.C1 <= %s -- Sucursal final
                AND dbo.KDIJ.C10 >= %s -- Fecha inicial
                AND dbo.KDIJ.C10 <= %s -- Fecha final
                AND dbo.KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                AND dbo.KDIJ.C4 = 'U'
                AND dbo.KDIJ.C5 = 'D'
                AND dbo.KDIJ.C6 IN ('5', '45')
                AND dbo.KDIJ.C7 IN ('1','2','3','4','5','6','18','19','21','22','25','26','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97')
            GROUP BY dbo.KDIF.C1, dbo.KDIF.C2
            ORDER BY dbo.KDIF.C1
        """
        
        params = [
            familia_inicial, familia_final, producto_inicial, producto_final,
            sucursal_inicial, sucursal_final, fecha_inicial, fecha_final
        ]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
    
    return result
