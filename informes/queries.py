from django.db.models import Q, F, Value, CharField
from django.db.models.functions import LTrim, RTrim
from .models import *
from django.db.models import Count

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

    # Filtrar por clientes y productos en una sola consulta
    if cliente_inicial and cliente_final and producto_inicial and producto_final:
        resultados = consultaCombinada(cliente_inicial, cliente_final, producto_inicial, producto_final)
    
    # Si no se especifican ambos rangos de clientes y productos, manejar por separado
    else:
        resultados = []
        if cliente_inicial and cliente_final:
            resultados.extend(consultaClientes(cliente_inicial, cliente_final))
        
        if producto_inicial and producto_final:
            resultados.extend(consultaProductos(producto_inicial, producto_final))
    
    return resultados

def consultaClientes(cliente_inicial, cliente_final):
    print(f"Consulta de Clientes donde cliente inicial: {cliente_inicial} y cliente final: {cliente_final}")
    
    queryClientes = Kdud.objects.values('clave_cliente', 'nombre_cliente', 'calle_numero_direccion') \
            .distinct() \
            .filter(clave_cliente__range=(cliente_inicial, cliente_final)) \
            .order_by('clave_cliente')
    
    return list(queryClientes)

def consultaProductos(producto_inicial, producto_final):
    print(f"Consulta de productos donde producto inicial: {producto_inicial} y producto final: {producto_final}")
    
    queryProductos = Kdii.objects.values('clave_producto', 'descripcion_producto', 'linea_producto')\
            .distinct()\
            .filter(clave_producto__range=(producto_inicial, producto_final))\
            .order_by('clave_producto')
            
    return list(queryProductos)

def consultaCombinada(cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta combinada de Clientes y Productos donde cliente inicial: {cliente_inicial}, cliente final: {cliente_final}, producto inicial: {producto_inicial}, producto final: {producto_final}")
     
    # Obtener resultados de clientes y productos
    resultados_clientes = consultaClientes(cliente_inicial, cliente_final)
    resultados_productos = consultaProductos(producto_inicial, producto_final)

    # Unir los resultados en una lista combinada
    queryCombinada = resultados_clientes + resultados_productos

    return queryCombinada
