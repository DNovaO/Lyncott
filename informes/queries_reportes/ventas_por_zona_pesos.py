# Description: Consulta de ventas por zonas en pesos
from datetime import datetime, timedelta, date
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

#Sin terminar
def consultaVentasPorZonasPesos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta de ventas por zonas en pesos desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}")
    
    with connection.cursor() as cursor:
        query = """
           
        """
        params = [
            fecha_inicial, fecha_final, fecha_inicial, fecha_final,
            producto_inicial, producto_final,
            fecha_inicial, fecha_final,
            cliente_inicial, cliente_final,

            producto_inicial, producto_final,
            fecha_inicial, fecha_final,
            cliente_inicial, cliente_final,
        ]

        for param in params:
            print(f"Param: {param}, {type(param)}")


        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        
    return result