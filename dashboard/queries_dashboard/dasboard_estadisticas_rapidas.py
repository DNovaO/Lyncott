from datetime import datetime
from decimal import Decimal
from django.db import connection
import calendar

def estadisticas_rapidas():
    print("Estadisticas Rapidas")
    
    ventas_totales_resultado = ventas_totales(fecha='2024-01-01', fecha_final='2024-01-31')
    ventas_kilos_resultado = ventas_kilos(fecha='2024-01-01', fecha_final='2024-01-31')
    devoluciones_totales_resultado = devoluciones_totales(fecha='2024-01-01', fecha_final='2024-01-31')
    notas_credito_resultado = notas_credito(fecha='2024-01-01', fecha_final='2024-01-31')
    ventas_por_sucursal_resultado = ventas_por_sucursal()
    ingresos_resultado = 0
    
    return [ventas_totales_resultado, ventas_kilos_resultado, devoluciones_totales_resultado, notas_credito_resultado, ventas_por_sucursal_resultado,ingresos_resultado]
    

def ventas_totales(fecha=None, fecha_final=None):
    print("estadisticas_rapidas: ventas_totales")
    print(f"Fecha Inicial: {fecha}")
    print(f" Fecha Final: {fecha_final}")
    
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
    
    
def ventas_kilos(fecha=None, fecha_final=None):
    print("estadisticas_rapidas: ventas_kilos")
        
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
                SUM(KDIJ.C11 * KDII.C13) AS ventas_en_kilos
            FROM KDIJ
            INNER JOIN KDII ON KDIJ.C3 = KDII.C1
            INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1
            INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
            INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
            WHERE 
                KDII.C1 >= '0101'
                AND KDII.C1 <= '9999'
                AND KDIJ.C10 BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE)
                AND KDUD.C2 >= '0000001'
                AND KDUD.C2 <= 'ZVM01'
                AND KDIJ.C4 = 'U'
                AND KDIJ.C5 = 'D'
                AND KDIJ.C6 IN ('5', '45')
                AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99')
                AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924');
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
    
def notas_credito(fecha=None, fecha_final=None):
    print("estadisticas_rapidas: notas_credito")
    
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
            ISNULL(SUM(CASE WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 = '20' THEN KDIJ.C14 END), 0) AS notas_credito 
        FROM KDIJ 
        WHERE
		    KDIJ.C10  BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE)
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

def ventas_por_sucursal():
    print("estadisticas_rapidas: ventas_por_sucursal")
    
    
    # fecha_inicial_parseada = datetime.today().replace(day=1).strftime('%Y-%m-%d')
    # fecha_final_parseada = datetime.today().strftime('%Y-%m-%d')
    
    fecha_inicial_parseada = '2024-01-01'
    fecha_final_parseada = '2024-01-31'
    
    with connection.cursor() as cursor:
        query_ventas_indivuales = """
        SELECT
            CASE
                WHEN KDIJ.C1 = '02' THEN 'venta_vallejo'
                WHEN KDIJ.C1 = '03' THEN 'venta_guadalajara'
                WHEN KDIJ.C1 = '04' THEN 'venta_monterrey'
                WHEN KDIJ.C1 = '05' THEN 'venta_queretaro'
                WHEN KDIJ.C1 = '06' THEN 'venta_hermosillo'
                WHEN KDIJ.C1 = '07' THEN 'venta_cancun'
                WHEN KDIJ.C1 = '08' THEN 'venta_puebla'
                WHEN KDIJ.C1 = '09' THEN 'venta_tijuana'
                WHEN KDIJ.C1 = '10' THEN 'venta_acapulco'
                WHEN KDIJ.C1 = '11' THEN 'venta_villahermosa'
                WHEN KDIJ.C1 = '12' THEN 'venta_culiacan'
                WHEN KDIJ.C1 = '13' THEN 'venta_veracruz'
                WHEN KDIJ.C1 = '14' THEN 'venta_los_cabos'
                WHEN KDIJ.C1 = '15' THEN 'venta_aguascalientes'
                WHEN KDIJ.C1 = '16' THEN 'venta_toluca'
                WHEN KDIJ.C1 = '17' THEN 'venta_chihuahua'
                WHEN KDIJ.C1 = '18' THEN 'venta_merida'
                WHEN KDIJ.C1 = '19' THEN 'venta_oaxaca'
                WHEN KDIJ.C1 = '20' THEN 'venta_vallarta'
                ELSE 'otra'
            END AS sucursal,
            SUM(KDIJ.C14) AS venta_pesos
        FROM KDIJ
        WHERE 
        KDIJ.C10 BETWEEN CAST(%s AS DATE) AND CAST(%s AS DATE)
        AND KDIJ.C1 BETWEEN '02' AND '20'
        GROUP BY KDIJ.C1;

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
