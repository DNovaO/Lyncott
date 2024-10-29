# Description: Consulta de consignatarios por familia
from datetime import datetime, timedelta
from django.db.models import Value, CharField, OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaConsignatariosPorFamilia(fecha_inicial, fecha_final, cliente_inicial, cliente_final, sucursal, familia_inicial, familia_final):
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}")
    
    families = [ 
        "CREMA PARA BATIR", "CREMA ENTERA", "CREMA REDUCIDA EN GRASA", "CREMA DULCE", "CREMA PARA CAFE",
        "CREMA NATURAL", "Q. COTTAGE", "FLETE", "INTERDELI Y MERMELADA", "LECHE UHT", "LURPAK", "LOS LLANOS", 
        "MANTEQUILLA", "MARGARINA", "NATURA", "OTRO", "PORT BLEU", "QUESO COTTAGE", "QUESO CREMA", "QUESOS MADUROS", 
        "QUESO OAXACA", "QUESO PANELA", "QUESUAVE", "REJAS", "TARIMAS", "YOGURT"
    ]
    
    # Formatear las familias para la cláusula PIVOT
    familias_formateadas = ', '.join(f'[{familia[:128]}]' for familia in families)  # Truncar a 128 caracteres si es necesario

    if sucursal == "ALL":
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDIJ.C1 = '{sucursal}'" 


    # Construir la consulta SQL con las familias formateadas
    query = f"""
        DECLARE @fecha_inicial DATETIME = %s,
                @fecha_final DATETIME = %s,
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @sucursal VARCHAR(20) = %s,
                @familia_inicial VARCHAR(20) = %s,
                @familia_final VARCHAR(20) = %s;

        SELECT * 
        FROM (
            SELECT DISTINCT
                KDVDIREMB.C1 AS 'clave_cliente',
                KDVDIREMB.C2 + ' - ' + KDVDIREMB.C3 AS 'consignatario',
                KDSEGMENTACION.C2 AS 'segmentacion',
                LTRIM(RTRIM(KDIF.C2)) AS 'familias',
                1 AS 'BANDERA'
            FROM KDM1
            INNER JOIN KDIJ ON KDIJ.C15 = KDM1.C10 AND KDIJ.C8 = KDM1.C6
            LEFT JOIN KDVDIREMB ON KDVDIREMB.C1 = KDM1.C10 AND KDVDIREMB.C2 = KDM1.C181
            LEFT JOIN KDSEGMENTACION ON KDSEGMENTACION.C1 = KDVDIREMB.C78   
            INNER JOIN KDII ON KDII.C1 = KDIJ.C3
            INNER JOIN KDIF ON KDIF.C1 = KDII.C5
            WHERE 
                KDIJ.C10 >= @fecha_inicial
                AND KDIJ.C10 <= @fecha_final
                AND KDIJ.C15 >= @cliente_inicial
                AND KDIJ.C15 <= @cliente_final
                {filtro_sucursal}
                AND KDIJ.C4 = 'U' 
                AND KDIJ.C5 = 'D' 
                AND KDIJ.C6 IN ('5', '45')
                AND KDIJ.C7 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '86', '87', '88', '94', '96', '97')
                AND KDII.C5 >= @familia_inicial
                AND KDII.C5 <= @familia_final
                AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
        ) AS DBDBAlt 
        PIVOT (
            SUM(BANDERA) 
            FOR [familias] IN ({familias_formateadas})
        ) AS PivotTableL


    """

    params = [
        fecha_inicial,
        fecha_final,
        cliente_inicial,
        cliente_final,
        sucursal,
        familia_inicial,
        familia_final
    ]

    # Imprimir los parámetros para depuración
    for param in params:
        print(param, type(param))

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]

            # Convertir valores Decimal a float
            for row in result:
                for key, value in row.items():
                    if isinstance(value, Decimal):
                        row[key] = float(value)

        return result

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []
