from decimal import Decimal
from datetime import datetime
from django.db import connection

def distribucion_venta_productos(fecha=None, fecha_final=None):
    print(f"Fecha Inicial: {fecha}")
    print(f" Fecha Final: {fecha_final}")
    
    # Establecer la fecha por defecto si no se pasa ninguna
    fecha_inicial_parseada = parse_date(fecha) or '2024-01-01'
    fecha_final_parseada = parse_date(fecha_final) or '2024-01-31'
    
    with connection.cursor() as cursor:
        query_ventas_indivuales = """
            SELECT 
                SUM(KDIJ.C14) AS venta,
                KDII.C2 AS producto
            FROM KDIJ
                INNER JOIN KDII ON KDIJ.C3 = dbo.KDII.C1
            WHERE
                KDIJ.C10 BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE)
                AND KDII.C1 >= '0101'
                AND KDII.C1 <= '9999'
            GROUP BY KDII.C2
            ORDER BY KDII.C2;
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


def parse_date(date_str):
    if not date_str:
        return None
    try:
        # Asegurar que las fechas se conviertan a formato yyyy-MM-dd
        return datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
    except ValueError:
        return None
