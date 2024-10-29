# Description: Consulta de consignatarios por segmento
from datetime import datetime, timedelta
from django.db.models import Value, CharField, OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaConsignatariosPorSegmento(fecha_inicial, fecha_final, cliente_inicial, cliente_final,sucursal_inicial, sucursal_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}")    

    if sucursal_inicial == 'ALL' and sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDM1.C1 BETWEEN '02' AND '20'"
    elif sucursal_inicial == 'ALL':
        filtro_sucursal = f"AND KDM1.C1 BETWEEN '02' AND '20'"
    elif sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDM1.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDM1.C1 BETWEEN '{sucursal_inicial}' AND '{sucursal_final}'"

    query = f"""
        DECLARE 
            @fecha_inicial DATETIME = %s,
            @fecha_final DATETIME = %s,
            @cliente_inicial VARCHAR(20) = %s,
            @cliente_final VARCHAR(20) = %s,
            @sucursal_inicial VARCHAR(20) = %s,
            @sucursal_final VARCHAR(20) = %s;
    
        SELECT  
            ISNULL(A.SEGMENTACION, 'vacío') AS 'segmento',
            COUNT(*) AS 'cantidad' 
        FROM (
            SELECT DISTINCT
                KDVDIREMB.C7 AS 'CP',
                LTRIM(RTRIM(KDSEGMENTACION.C2)) AS 'SEGMENTACION',
                KDM1.C10 AS 'ID_Cliente',
                KDM1.C181 AS 'ID_Consignatario'
            FROM KDM1
            LEFT JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1
                AND KDM1.C181 = KDVDIREMB.C2
            LEFT JOIN KDSEGMENTACION ON KDSEGMENTACION.C1 = KDVDIREMB.C78
            WHERE 
                KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial, 102)
                AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final, 102)
                {filtro_sucursal}
                AND KDM1.C10 >= @cliente_inicial
                AND KDM1.C10 <= @cliente_final
                AND KDM1.C12 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                AND KDM1.C2 = 'U'
                AND KDM1.C3 = 'D'
                AND KDM1.C4 IN ('5', '45')
                AND KDM1.C5 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '86', '87', '88', '94', '96', '97')
        ) AS A
        GROUP BY A.SEGMENTACION
        ORDER BY A.SEGMENTACION;
    """

    params = [
        fecha_inicial, fecha_final,
        cliente_inicial, cliente_final,
        sucursal_inicial, sucursal_final
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
