# Description: Consulta de lista de precios por producto
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaListaPreciosProducto(producto_inicial, producto_final):
    print(f"Consulta de lista de precios por producto desde {producto_inicial} hasta {producto_final}")

    with connection.cursor() as cursor:
        query = """
            SELECT 
                KDII.C1	AS clave_producto,
                KDII.C2	AS nombre_producto,
                KDII.C7 AS UPC,
                KDIG.C2 AS linea,
                KDII.C12 AS unidad,
                KDII.C13 AS factor_conversion,
                KDII.C14 AS A_centro,
                KDII.C15 AS B_peninsula,
                KDII.C16 AS C_pacifico,
                KDII.C17 AS D_chihuahua
            FROM KDII
                INNER JOIN KDIG ON KDIG.C1 = KDII.C3
            WHERE KDII.C4 ='PT'
                AND  KDII.C1 >= %s
                AND  KDII.C1 <= %s
        """

        params = [producto_inicial, producto_final]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        
    return result


