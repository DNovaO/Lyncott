from django.db.models import Q, F, Value
from django.db.models.functions import LTrim, RTrim
from .models import *
from django.db.models import Count

def printAllSelectedItems(parametrosSeleccionados):
    cliente_inicial = None
    cliente_final = None
    print("All Selected Items:")
    
    for key, value in parametrosSeleccionados.items():
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            for item in value:
                print(f" {key}: {item[list(item.keys())[0]].strip()}")
                if key == 'cliente_inicial' or key == 'cliente_final':
                    cliente = item[list(item.keys())[0]].strip()
                    if key == 'cliente_inicial':
                        cliente_inicial = cliente
                    elif key == 'cliente_final':
                        cliente_final = cliente
        else:
            print(f"{key}: {value}")
    
    if cliente_inicial and cliente_final:
        consultaClientes(cliente_inicial, cliente_final)

        
def consultaClientes(cliente_inicial, cliente_final):
    print(f"Consulta de Clientes donde cliente inicial: {cliente_inicial} y cliente final: {cliente_final}")
    
    query = Kdud.objects.values('clave_cliente', 'nombre_cliente', 'calle_numero_direccion') \
            .distinct() \
            .filter(clave_cliente__range=(cliente_inicial, cliente_final)) \
            .order_by('clave_cliente')
    
    print("Query result:")
    for result in query:
        print(f"Clave Cliente: {result['clave_cliente']}")
        print(f"Nombre Cliente: {result['nombre_cliente']}")
        print(f"Calle y Número: {result['calle_numero_direccion']}")
        print("-" * 20)