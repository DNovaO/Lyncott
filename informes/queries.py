from datetime import datetime
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, DecimalField
from django.db.models.functions import Coalesce, Cast, Concat
from .models import *

def printAllSelectedItems(parametrosSeleccionados):
    filtros = {}
    print("Parámetros seleccionados:")
    for key, value in parametrosSeleccionados.items():
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            for item in value:
                key_value = item[list(item.keys())[0]].strip()
                print(f" {key}: {key_value}")
                if key in ('fecha_inicial', 'fecha_final', 'cliente_inicial', 'cliente_final', 'producto_inicial', 'producto_final', 'sucursal_inicial', 'sucursal_final'):
                    filtros[key] = key_value
        else:
            print(f"{key}: {value}")
            filtros[key] = value
    
    return ejecutarConsulta(filtros)

def ejecutarConsulta(filtros):
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
                        
    if all([fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final]):
        resultados.extend(consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final))
    else:
        print("Faltan parámetros para realizar la consulta de ventas por producto")
        
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
        
        cantidad=Sum('cantidad_unidades_entrada'),
        
        venta_sumatoria=Sum('monto_venta'),
        
        venta=Concat(
            Value('$ '),
            'venta_sumatoria',
            output_field=CharField()
        ),
        
        kgslts=ExpressionWrapper(
            F('cantidad') * F('factor_conversion'),
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

def pruebas_consultas():
    
    queryKdii = Kdii.objects.values('factor_conversion')
    
    print('Esto es kdii', queryKdii)

    queryKdij = Kdij.objects.values('cantidad_unidades_entrada')
    
    print('Esto es kdij', queryKdij)
    
    return 0