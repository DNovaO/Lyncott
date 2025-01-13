from decimal import Decimal
from datetime import datetime
from django.db import connection


def ventas_contra_devoluciones(fecha=None, fecha_final=None):
    print(f"Fecha Inicial: {fecha}")
    print(f" Fecha Final: {fecha_final}")
    
    # Establecer la fecha por defecto si no se pasa ninguna
    fecha_inicial_parseada = parse_date(fecha) or '2024-01-01'
    fecha_final_parseada = parse_date(fecha_final) or '2024-01-31'
    
    with connection.cursor() as cursor:
        query_ventas_indivuales = """
            SELECT
                ventas.VENTAS AS ventas,
                devoluciones.DEVOLUCIONES AS devoluciones
            FROM (
                SELECT 
                    SUM(KDM1.C16) AS VENTAS
                FROM KDM1
                WHERE
                    KDM1.C2 = 'U' 
                    AND KDM1.C3 = 'D'
                    AND KDM1.C4 IN ('5', '45')
                    AND KDM1.C5 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26')
                    AND KDM1.C9 >= CAST(%s AS DATE)
                    AND KDM1.C9 <= CAST(%s AS DATE)
            ) AS ventas
            FULL JOIN (
                SELECT
                    SUM(KDM1.C16) AS DEVOLUCIONES
                FROM KDM1
                WHERE 
                    KDM1.C2 = 'N' 
                    AND KDM1.C3 = 'D'   
                    AND KDM1.C4 = '25' 
                    AND KDM1.C5 = '12'
                    AND KDM1.C9 >= CAST(%s AS DATE)
                    AND KDM1.C9 <= CAST(%s AS DATE)
            ) AS devoluciones
            ON 1=1;
        """
        
        # Ejecutar la consulta
        cursor.execute(query_ventas_indivuales, [fecha_inicial_parseada, fecha_final_parseada, fecha_inicial_parseada, fecha_final_parseada])

        # Obtener los resultados
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result


def parse_date(date_str):
    if not date_str:
        return None
    try:
        # Asegurar que las fechas se conviertan a formato yyyy-MM-dd
        return datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
    except ValueError:
        return None
