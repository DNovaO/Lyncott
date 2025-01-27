# Description: Consulta de tendencia ventas para el dashboard
from decimal import Decimal
from datetime import datetime
from django.db import connection

def consultaTendenciaVentasDashboard(fecha=None, fecha_final=None):

    print(f"Fecha Inicial: {fecha}")
    print(f"Fecha Final: {fecha_final}")
    
    # Establecer la fecha por defecto si no se pasa ninguna
    fecha_inicial_parseada = parse_date(fecha) or '2024-01-01'
    fecha_final_parseada = parse_date(fecha_final) or '2024-01-31'
    
    print(f"Fecha Inicial Parseada: {fecha_inicial_parseada}")
    print(f"Fecha Final Parseada: {fecha_final_parseada}")

    with connection.cursor() as cursor:
        query_tendencia_ventas = f"""
            SET LANGUAGE Español;        
        
            DECLARE @fecha_inicial VARCHAR(20) = %s,
                    @fecha_final VARCHAR(20) = %s;
            
            SELECT
                CONCAT(
                    FORMAT(KDM1.C9, 'dd/MM/yyyy'),
                    ' (',
                    CASE
                        WHEN DATEPART(dw, KDM1.C9) = 1 THEN 'Lunes'
                        WHEN DATEPART(dw, KDM1.C9) = 2 THEN 'Martes'
                        WHEN DATEPART(dw, KDM1.C9) = 3 THEN 'Miércoles'
                        WHEN DATEPART(dw, KDM1.C9) = 4 THEN 'Jueves'
                        WHEN DATEPART(dw, KDM1.C9) = 5 THEN 'Viernes'
                        WHEN DATEPART(dw, KDM1.C9) = 6 THEN 'Sábado'
                        WHEN DATEPART(dw, KDM1.C9) = 7 THEN 'Domingo'
                        ELSE '-'
                    END,
                    ')'
                ) AS fecha_dia,
                FORMAT(KDM1.C9, 'dd/MM/yyyy') AS fecha,
                CASE
                    WHEN DATEPART(dw, KDM1.C9) = 1 THEN 'Lunes'
                    WHEN DATEPART(dw, KDM1.C9) = 2 THEN 'Martes'
                    WHEN DATEPART(dw, KDM1.C9) = 3 THEN 'Miércoles'
                    WHEN DATEPART(dw, KDM1.C9) = 4 THEN 'Jueves'
                    WHEN DATEPART(dw, KDM1.C9) = 5 THEN 'Viernes'
                    WHEN DATEPART(dw, KDM1.C9) = 6 THEN 'Sábado'
                    WHEN DATEPART(dw, KDM1.C9) = 7 THEN 'Domingo'
                    ELSE '-'
                END AS dia,
                SUM(CASE WHEN KDUD.C33 = 'A' THEN KDM1.C16 ELSE 0 END) AS venta_autoservice,
                SUM(CASE WHEN KDUD.C33 <> 'A' THEN KDM1.C16 ELSE 0 END) AS venta_foodservice,
                SUM(KDM1.C16 - KDM1.C15) AS venta,
                ROW_NUMBER() OVER (ORDER BY KDM1.C9 ASC) AS orden
            FROM KDM1
            INNER JOIN KDUD ON KDM1.C10 = KDUD.C2
            WHERE
                KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial, 102)
                AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final, 102)
                AND KDM1.C2 = 'U'
                AND KDM1.C3 = 'D'
                AND KDM1.C4 IN ('5', '45')
                AND KDM1.C5 IN ('1', '2', '3', '4', '5', '6', '18', '19', '21', '22', '25', '26')
                AND KDM1.C12 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
            GROUP BY KDM1.C9;

        """

        # Ejecutar la consulta
        cursor.execute(query_tendencia_ventas, [fecha_inicial_parseada, fecha_final_parseada])

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


