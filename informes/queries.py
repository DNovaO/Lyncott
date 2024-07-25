from datetime import datetime
from django.db.models import Sum, F, FloatField, ExpressionWrapper, DateTimeField
from django.db.models.functions import Cast
from itertools import zip_longest 
from .models import *
def printAllSelectedItems(parametrosSeleccionados):
    filtros = {}
    print("All Selected Items:")
    
    for key, value in parametrosSeleccionados.items():
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            for item in value:
                print(f" {key}: {item[list(item.keys())[0]].strip()}")
                if key in ('fecha_inicial', 'fecha_final', 'cliente_inicial', 'cliente_final', 'producto_inicial', 'producto_final', 'sucursal_inicial', 'sucursal_final'):
                    filtros[key] = item[list(item.keys())[0]].strip()
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
    
    if fecha_inicial and fecha_final and cliente_inicial and cliente_final and producto_inicial and producto_final and sucursal_inicial and sucursal_final:
        return consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final)
    elif cliente_inicial and cliente_final and producto_inicial and producto_final:
        return consultaCombinada(cliente_inicial, cliente_final, producto_inicial, producto_final)
    else:
        resultados = []
        if cliente_inicial and cliente_final:
            resultados.extend(consultaClientes(cliente_inicial, cliente_final))
        
        if producto_inicial and producto_final:
            resultados.extend(consultaProductos(producto_inicial, producto_final))
    
    return resultados

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d-%m-%Y')
    except ValueError:
        return None

def consultaClientes(cliente_inicial, cliente_final):
    print(f"Consulta de Clientes donde cliente inicial: {cliente_inicial} y cliente final: {cliente_final}")
    
    queryClientes = Kdud.objects.values(
        'clave_cliente',
        'nombre_cliente',
        'calle_numero_direccion'
    ).filter(
        clave_cliente__range=(cliente_inicial, cliente_final)
    ).order_by('clave_cliente')
    
    return list(queryClientes)

def consultaProductos(producto_inicial, producto_final):
    print(f"Consulta de productos donde producto inicial: {producto_inicial} y producto final: {producto_final}")
    
    queryProductos = Kdii.objects.values(
        'clave_producto',
        'descripcion_producto',
        'linea_producto'
    ).filter(
        clave_producto__range=(producto_inicial, producto_final)
    ).order_by('clave_producto')
    
    return list(queryProductos)

def consultaCombinada(cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta combinada de Clientes y Productos donde cliente inicial: {cliente_inicial}, cliente final: {cliente_final}, producto inicial: {producto_inicial}, producto final: {producto_final}")
     
    # Obtener resultados de clientes y productos
    resultados_clientes = consultaClientes(cliente_inicial, cliente_final)
    resultados_productos = consultaProductos(producto_inicial, producto_final)

    # Combinar los resultados en una lista de diccionarios
    resultados_combinados = []
    for cliente, producto in zip_longest(resultados_clientes, resultados_productos, fillvalue='-'):
        combinado = {**cliente, **producto}
        resultados_combinados.append(combinado)
    
    return resultados_combinados

def consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final):
    print(f"Consulta de ventas por productos desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}, sucursal inicial: {sucursal_inicial} y sucursal final: {sucursal_final}")

    resultados = (Kdij.objects
                    .filter(
                        clave_producto__gte= producto_inicial,
                        clave_producto__lte= producto_final,
                        fecha_gte= Cast(fecha_inicial, DateTimeField()),
                        fecha_lte= Cast(fecha_final, DateTimeField()),
                        clave_sucursal__gte= sucursal_inicial,
                        clave_sucursal__lte= sucursal_final,
                        clave_cliente__gte= cliente_inicial,
                        clave_cliente__lte= cliente_final,
                        genero = 'U',
                        naturaleza = 'D',
                        grupo_movimiento__in = ['5','45']  
                    ).values('clave_producto', 'Kdii__descripcion_producto', 'Kdii__unidad_medida', 'unidad_alternativa')
                    .annotate(
                        CLAVE=F('C3'),
                        PRODUCTO=F('kdii__C2'),
                        CANTIDAD=Sum('C11'),
                        UNI=F('kdii__C11'),
                        KGSLTS=Sum(F('C11') * F('kdii__C13')),
                        UNID=F('kdii__C12'),
                        VENTA=Sum('C14'),
                    )
                    .order_by('C3', 'kdii__C2', 'kdii__C11', 'kdii__C12'))
        
return resultados