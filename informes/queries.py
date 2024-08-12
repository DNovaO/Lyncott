from datetime import datetime
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, DecimalField
from django.db.models.functions import Coalesce, Cast, Concat, Round
from .models import *

def clasificarParametros(parametrosSeleccionados, tipo_reporte):
    filtros = {}
    
    for key, value in parametrosSeleccionados.items():
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            for item in value:
                key_value = item[list(item.keys())[0]].strip()
                if key in ('fecha_inicial', 'fecha_final', 'cliente_inicial', 'cliente_final', 'producto_inicial', 'producto_final', 'sucursal_inicial', 'sucursal_final'):
                    filtros[key] = key_value
        else:
            if isinstance(value, list) and len(value) > 0:
                value = value[0]
                if isinstance(value, dict):
                    value = value[list(value.keys())[0]].strip()
                    
            filtros[key] = value
    
    return ejecutarConsulta(filtros, tipo_reporte)

def ejecutarConsulta(filtros, tipo_reporte):
    fecha_inicial_str = filtros.get('fecha_inicial')
    fecha_final_str = filtros.get('fecha_final')
    cliente_inicial = filtros.get('cliente_inicial')
    cliente_final = filtros.get('cliente_final')
    producto_inicial = filtros.get('producto_inicial')
    producto_final = filtros.get('producto_final')
    sucursal_inicial = filtros.get('sucursal_inicial')
    sucursal_final = filtros.get('sucursal_final')
    
    fecha_inicial = parse_date(fecha_inicial_str)
    fecha_final = parse_date(fecha_final_str)
    
    resultados = []
                        
    if tipo_reporte == "Por Producto (con Refacturación)":
        resultados.extend(consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final))
    
    return resultados
    
def parse_date(date_str):
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    except ValueError:
        return None

def consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final):
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
        
        venta_sumatoria=Sum('monto_venta'),
        
        venta=Concat(
            Value('$'),
            'venta_sumatoria',
            output_field=CharField()
        ),
        
        kgslts=ExpressionWrapper(
            Round(F('cantidad') * F('factor_conversion'), 2),
            output_field=FloatField()
        )
    )

    queryVentaPorProducto = subqueryVentaPorProducto.values(
        'clave_producto',
        'descripcion_producto',
        'cantidad',
        'unidad_medida',
        'kgslts',
        'unidad_alternativa',
        'venta'
    ).order_by(
        'clave_producto'
    )

    return list(queryVentaPorProducto)