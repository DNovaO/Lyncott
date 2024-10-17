# Description: Consulta de ventas por producto con refacturación 
from datetime import datetime, timedelta
from django.db.models import Value, CharField, OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaVentasPorProductoConRefacturacion(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final):
    print(f"Consulta de ventas por productos desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}, sucursal inicial: {sucursal_inicial} y sucursal final: {sucursal_final}")
    
    kdii_subquery = Kdii.objects.filter(
        clave_producto=OuterRef('clave_producto')
    ).values(
        'descripcion_producto',
        'unidad_medida',
        'unidad_alternativa',
        'factor_conversion'
    )[:1]

    subqueryVentaPorProducto = Kdij.objects.filter(
        clave_cliente__gte=cliente_inicial,
        clave_cliente__lte=cliente_final,
        clave_producto__gte=producto_inicial,
        clave_producto__lte=producto_final,
        fecha__gte=fecha_inicial,
        fecha__lte=fecha_final,
        clave_sucursal__gte=sucursal_inicial,
        clave_sucursal__lte=sucursal_final,
        genero='U',
        naturaleza='D',
        grupo_movimiento__in=['5', '45']
    ).values(
        'clave_producto'
    ).annotate(
        descripcion_producto=Subquery(kdii_subquery.values('descripcion_producto')),
        unidad_medida=Subquery(kdii_subquery.values('unidad_medida')),
        unidad_alternativa=Subquery(kdii_subquery.values('unidad_alternativa')),
        factor_conversion=Subquery(kdii_subquery.values('factor_conversion')),
        cantidad=Round(Sum('cantidad_unidades_entrada'), 2),
        venta=Sum('monto_venta'),
        kgslts=ExpressionWrapper(
            Round(F('cantidad') * F('factor_conversion'), 2),
            output_field=FloatField()
        ),
        venta_sobre_Kg=ExpressionWrapper(
            F('venta') / F('kgslts'),
            output_field=FloatField()
        ),
        venta_sobre_UV=ExpressionWrapper(
            Round(F('venta') / F('cantidad'), 2),
            output_field=FloatField()
        ),   
    )

    queryVentaPorProducto = subqueryVentaPorProducto.values(
        'clave_producto',
        'descripcion_producto',
        'cantidad',
        'unidad_medida',
        'kgslts',
        'unidad_alternativa',
        'venta_sobre_Kg',
        'venta_sobre_UV',
        'venta',
    ).order_by(
        'clave_producto'
    )
    
    # Convert Decimal values to float
    result = []
    for row in queryVentaPorProducto:
        converted_row = {key: float(value) if isinstance(value, Decimal) else value for key, value in row.items()}
        result.append(converted_row)

    return result