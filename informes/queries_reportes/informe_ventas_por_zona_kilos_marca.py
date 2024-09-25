# Description: Consulta de ventas por crédito contable
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaVentasPorZonaKilosMarca(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, marca_inicial, marca_final):

    print(f"Consulta de ventas por zona en kilos desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial}, cliente final: {cliente_final}, producto inicial: {producto_inicial}, producto final: {producto_final}, marca inicial: {marca_inicial}, marca final: {marca_final}")
    
    print('fechas:', fecha_inicial)
    print('fechas:', fecha_final)
    
    
    # Obtener los valores tanto de f_DifDias como de f_DifDiasTotales
    dif_dias = f_DifDias(fecha_inicial, fecha_final, [])
    dif_dias_totales = f_DifDiasTotales(fecha_inicial, fecha_final, [])
        
    print('Diferencia de días:', dif_dias)
    print('Diferencia de días totales:', dif_dias_totales)
    

    with connection.cursor() as cursor:
        query = """
            DECLARE @Dias INT = %s,
                    @DiasTotales INT = %s,
                    @fecha_inicial VARCHAR(20) = %s,
                    @fecha_final VARCHAR(20) = %s,
                    @producto_inicial VARCHAR(20) = %s,
                    @producto_final VARCHAR(20) = %s,
                    @cliente_inicial VARCHAR(20) = %s,
                    @cliente_final VARCHAR(20) = %s,
                    @marca_inicial VARCHAR(20) = %s,
                    @marca_final VARCHAR(20) = %s;

          
        """

        params = [
                    dif_dias, dif_dias_totales,
                    fecha_inicial, fecha_final,
                    producto_inicial, producto_final, 
                    cliente_inicial, cliente_final,
                    marca_inicial, marca_final
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