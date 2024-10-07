# Description: Consulta de ventas por producto por giro
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaVentaPorClienteConsignatarioPorMes(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}, sucursal_inicial: {sucursal_inicial}, sucursal_final: {sucursal_final}")
    
    meses = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre"
    }
    
    mes = meses.get(fecha_inicial.month)
    
    
    with connection.cursor() as cursor:
        query = f"""
            DECLARE 
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s,
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s;
            
            SELECT 
                DatosActuales.SUC AS sucursal,
                DatosActuales.GRUPO AS grupo,
                DatosActuales.CLIENTE AS clave_cliente,
                DatosActuales.CONSIG AS clave_consignatario,
                DatosActuales.NOM_CONSIG AS consignatario,
                ISNULL(DatosActuales.TOTAL, 0) AS total_mes_{mes}
            FROM (
                SELECT 
                    LTRIM(RTRIM(KDIJ.C1)) AS SUC,
                    LTRIM(RTRIM(KDUD.C66)) AS GRUPO,
                    LTRIM(RTRIM(KDUD.C2)) AS CLIENTE,
                    LTRIM(RTRIM(KDM1.C181)) AS CONSIG,
                    LTRIM(RTRIM(KDVDIREMB.C3)) AS NOM_CONSIG,
                    ISNULL(SUM(KDIJ.C14), 0) AS TOTAL
                FROM KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                LEFT JOIN KDM1 ON KDIJ.C1 = KDM1.C1 
                    AND KDIJ.C4 = KDM1.C2 
                    AND KDIJ.C5 = KDM1.C3 
                    AND KDIJ.C6 = KDM1.C4 
                    AND KDIJ.C7 = KDM1.C5 
                    AND KDIJ.C8 = KDM1.C6
                LEFT JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 
                    AND KDM1.C181 = KDVDIREMB.C2
                WHERE 
                    KDII.C1 BETWEEN @producto_inicial AND @producto_final
                    AND KDIJ.C10 BETWEEN @fecha_inicial AND @fecha_final
                    AND KDIJ.C1 BETWEEN @sucursal_inicial AND @sucursal_final
                    AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                    AND KDIJ.C16 NOT IN (
                        '902', '903', '904', '905', '906', '907', '908', '909', '910', 
                        '911', '912', '913', '914', '915', '916', '917', '918', '919', 
                        '920', '921', '922', '923', '924'
                    )
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C7 IN (
                        '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', 
                        '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', 
                        '79', '80', '81', '82', '86', '87', '88', '94', '96', '97'
                    )
                GROUP BY 
                    KDIJ.C1, 
                    KDUD.C66, 
                    KDUD.C2, 
                    KDM1.C181, 
                    KDVDIREMB.C3
            ) AS DatosActuales;
                
        """

        # Definir los parámetros para las fechas
        params = [
                    fecha_inicial, fecha_final,
                    cliente_inicial, cliente_final,
                    producto_inicial, producto_final,
                    sucursal_inicial, sucursal_final
                ]

        for param in params:
            print(param, type(param))

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result
