from decimal import Decimal
from django.db import connection


def ventas_contra_devoluciones(fecha=None, fecha_final=None):
    
    # Establecer la fecha por defecto si no se pasa ninguna
    if not fecha and not fecha_final:
        fecha = '01-01-2024'   
        fecha_final = '01-31-2024'
        

    with connection.cursor() as cursor:
        query_ventas_indivuales = f"""
            DECLARE
                @fecha_inicial AS VARCHAR(20) = %s,
                @fecha_final as VARCHAR(20) = %s;
                
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
                    AND KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial, 102)
                    AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final, 102)
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
                    AND KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial, 102)
                    AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final, 102)
            ) AS devoluciones
            ON 1=1;
        """
        
        
        # Ejecutar la consulta
        cursor.execute(query_ventas_indivuales, [fecha, fecha_final])

        # Obtener los resultados
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result
