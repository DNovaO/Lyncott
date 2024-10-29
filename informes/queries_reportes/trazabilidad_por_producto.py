# Description: Consulta de trazabilidad por producto
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

#Tabla con formato especial
def consultaTrazabilidadPorProducto(fecha_inicial, fecha_final, producto_inicial, producto_final, status, sucursal):
    print(f"Consulta de trazabilidad por producto de: {fecha_inicial} a: {fecha_final}, del producto: {producto_inicial} al {producto_final}, con status {status} y de la sucursal {sucursal}")

    if sucursal == 'ALL':
        filtro_sucursal = f"KDPORD.C19 BETWEEN '01' AND '20'"
    else:
        filtro_sucursal = f"KDPORD.C19 = '{sucursal}'"

    # Si el status es "Todos", entonces buscamos tanto 'A' (Activo) como 'I' (Inactivo)
    if status == 'Activo':
        status_filter = "= 'A'"
    elif status == 'Inactivo':
        status_filter = "= 'I'"
    elif status == 'Todos':
        status_filter = "IN ('A', 'I')"
        
    with connection.cursor() as cursor:
        # Construcción dinámica de la consulta SQL
        query = f"""
            SELECT
                Orden.CLAVE AS clave_producto,
                Orden.Producto AS producto,
                CASE 
                    WHEN Orden.OStatus = 'A' THEN 'Activo'
                    WHEN Orden.OStatus = 'I' THEN 'Inactivo'
                    ELSE '-'
                END AS status,
                Orden.OOrden AS orden,
                Orden.OFecha AS orden_fecha,
                Orden.OFolio AS numero_folio,
                Orden.OCantidad AS cantidad,
                Orden.PFecha AS partes_fecha,
                Parte.Folio AS partes_folio,
                Termina.Folio AS termina_folio,
                Termina.Cantidad AS termina_cantidad,
                Orden.DiferenciaDias AS diferencia_de_dias,
                Orden.OCantidad - Termina.Cantidad AS diferencia_de_cantidad
            FROM (
                SELECT 
                    KDPORD.C3 AS CLAVE,
                    KDII.C2 AS Producto,
                    KDPORD.C2 AS OStatus,
                    KDPORD.C1 AS OOrden,
                    FORMAT(KDPORD.C6, 'd', 'en-gb') AS OFecha,
                    KDPORD.C24 AS OFolio,
                    KDPORD.C9 AS OCantidad,
                    FORMAT(KDM1.C9, 'd', 'en-gb') AS PFecha,
                    DATEDIFF(day, KDPORD.C6, KDM1.C9) AS DiferenciaDias
                FROM KL2020.dbo.KDPORD 
                INNER JOIN KL2020.dbo.KDII ON KDPORD.C3 = KDII.C1
                INNER JOIN KL2020.dbo.KDM1 ON KDPORD.C1 = KDM1.C11
                WHERE 
                {filtro_sucursal}  /*Sucursal*/
                AND KDPORD.C6 >= '{fecha_inicial}'  /*Fecha inicial*/
                AND KDPORD.C6 <= '{fecha_final}'  /*Fecha final*/
                AND KDPORD.C3 >= '{producto_inicial}'  /*Producto inicial*/
                AND KDPORD.C3 <= '{producto_final}'  /*Producto final*/
                AND KDPORD.C2 {status_filter} /*Status (A, I, o ambos)*/
            ) AS Orden
            LEFT JOIN (
                SELECT DISTINCT
                    KDPORD3.C1 AS OORden,
                    KDPORD3.C16 AS Folio
                FROM KL2020.dbo.KDPORD3
                WHERE C13 = 'D'
            ) AS Parte ON Orden.OOrden = Parte.OORden
            LEFT JOIN (
                SELECT DISTINCT
                    KDPORD3.C1 AS OORden,
                    KDPORD3.C16 AS Folio,
                    KDPORD3.C6 AS Cantidad
                FROM KL2020.dbo.KDPORD3
                WHERE C13 = 'A'
            ) AS Termina ON Orden.OOrden = Termina.OORden
            ORDER BY Orden.CLAVE
        """

        # params = [sucursal, fecha_inicial, fecha_final, producto_inicial, producto_final]
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        print(query)

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result