from decimal import Decimal
from datetime import datetime
from django.db import connection
import calendar

def distribucion_venta_productos(fecha=None, fecha_final=None):
    print(f"Fecha Inicial: {fecha}")
    print(f"Fecha Final: {fecha_final}")
    
    # Establecer la fecha por defecto si no se pasa ninguna
    # Obtener fechas por defecto (primer y último día del mes actual)
    hoy = datetime.today()
    primer_dia_mes = hoy.replace(day=1)
    ultimo_dia_mes = primer_dia_mes.replace(
        day=calendar.monthrange(primer_dia_mes.year, primer_dia_mes.month)[1]
    )

    # Establecer fechas si no se proporcionan
    if not fecha:
        fecha = primer_dia_mes.strftime('%d-%m-%Y')
    if not fecha_final:
        fecha_final = ultimo_dia_mes.strftime('%d-%m-%Y')

    fecha_inicial_parseada = parse_date(fecha)
    fecha_final_parseada = parse_date(fecha_final)
    
    
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
        # Manejar formato ISO '2023-01-01T06:00:00.000Z'
        if 'T' in date_str:
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
        # Manejar formato 'dd-mm-YYYY'
        return datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
    except ValueError:
        return None

