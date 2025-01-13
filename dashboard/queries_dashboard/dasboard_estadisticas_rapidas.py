from datetime import datetime
from decimal import Decimal
from django.db import connection


def estadisticas_rapidas():
    print("Estadisticas Rapidas")
    
    ventas_totales_resultado = ventas_totales(fecha='2024-01-01', fecha_final='2024-01-31')
    ventas_kilos_resultado = ventas_kilos()
    devoluciones_totales_resultado = devoluciones_totales(fecha='2024-01-01', fecha_final='2024-01-31')
    ingresos_resultado = ingresos()
    
    return [ventas_totales_resultado, ventas_kilos_resultado, devoluciones_totales_resultado, ingresos_resultado]
    

def ventas_totales(fecha=None, fecha_final=None):
    print("estadisticas_rapidas: ventas_totales")
    print(f"Fecha Inicial: {fecha}")
    print(f" Fecha Final: {fecha_final}")
    
    # Establecer la fecha por defecto si no se pasa ninguna
    fecha_inicial_parseada = parse_date(fecha) or '2024-01-01'
    fecha_final_parseada = parse_date(fecha_final) or '2024-01-31'
    
    with connection.cursor() as cursor:
        query_ventas_indivuales = """
            SELECT
                SUM(KDM1.C16) AS ventas
            FROM KDM1
            WHERE
                KDM1.C2 = 'U' 
                AND KDM1.C3 = 'D'
                AND KDM1.C4 IN ('5', '45')
                AND KDM1.C5 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26')
                AND KDM1.C9 BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE);
        """
        
        # Ejecutar la consulta
        cursor.execute(query_ventas_indivuales, [fecha_inicial_parseada, fecha_final_parseada])

        # Obtener los resultados
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result

    
def ventas_kilos():
    print("estadisticas_rapidas: ventas_kilos")
    
    
def devoluciones_totales(fecha=None, fecha_final=None):
    print("estadisticas_rapidas: devoluciones_totales")
    print(f"Fecha Inicial: {fecha}")
    print(f" Fecha Final: {fecha_final}")
    
    # Establecer la fecha por defecto si no se pasa ninguna
    fecha_inicial_parseada = parse_date(fecha) or '2024-01-01'
    fecha_final_parseada = parse_date(fecha_final) or '2024-01-31'
    
    with connection.cursor() as cursor:
        query_ventas_indivuales = """
            SELECT
                SUM(KDM1.C16) AS devoluciones
            FROM KDM1
            WHERE 
                KDM1.C2 = 'N' 
                AND KDM1.C3 = 'D'   
                AND KDM1.C4 = '25' 
                AND KDM1.C5 = '12'
                AND KDM1.C9 BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE);
        """
        
        # Ejecutar la consulta
        cursor.execute(query_ventas_indivuales, [fecha_inicial_parseada, fecha_final_parseada])

        # Obtener los resultados
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result
    
    
def ingresos():
    print("estadisticas_rapidas: ingresos")
    
def parse_date(date_str):
    if not date_str:
        return None
    try:
        # Asegurar que las fechas se conviertan a formato yyyy-MM-dd
        return datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
    except ValueError:
        return None
