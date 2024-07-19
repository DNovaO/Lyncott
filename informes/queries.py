from django.db.models import Value, CharField
from itertools import zip_longest 
from .models import *

def printAllSelectedItems(parametrosSeleccionados):
    filtros = {}
    print("All Selected Items:")
    
    for key, value in parametrosSeleccionados.items():
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            for item in value:
                print(f" {key}: {item[list(item.keys())[0]].strip()}")
                if key in ('cliente_inicial', 'cliente_final', 'producto_inicial', 'producto_final'):
                    filtros[key] = item[list(item.keys())[0]].strip()
        else:
            print(f"{key}: {value}")
            filtros[key] = value
    
    return ejecutarConsulta(filtros)

def ejecutarConsulta(filtros):
    cliente_inicial = filtros.get('cliente_inicial')
    cliente_final = filtros.get('cliente_final')
    producto_inicial = filtros.get('producto_inicial')
    producto_final = filtros.get('producto_final')

    resultados = []
    
    if cliente_inicial and cliente_final and producto_inicial and producto_final:
        resultados = consultaCombinada(cliente_inicial, cliente_final, producto_inicial, producto_final)
    else:
        if cliente_inicial and cliente_final:
            resultados.extend(consultaClientes(cliente_inicial, cliente_final))
        
        if producto_inicial and producto_final:
            resultados.extend(consultaProductos(producto_inicial, producto_final))
    
    return resultados

def consultaClientes(cliente_inicial, cliente_final):
    print(f"Consulta de Clientes donde cliente inicial: {cliente_inicial} y cliente final: {cliente_final}")
    
    queryClientes = Kdud.objects.values(
        'clave_cliente',
        'nombre_cliente',
        'calle_numero_direccion'
    ).distinct().filter(
        clave_cliente__range=(cliente_inicial, cliente_final)
    ).order_by('clave_cliente')
    
    return list(queryClientes)

def consultaProductos(producto_inicial, producto_final):
    print(f"Consulta de productos donde producto inicial: {producto_inicial} y producto final: {producto_final}")
    
    queryProductos = Kdii.objects.values(
        'clave_producto',
        'descripcion_producto',
        'linea_producto'
    ).distinct().filter(
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