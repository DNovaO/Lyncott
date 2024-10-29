# Description: Consulta de ventas por zona en kilos y marca
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaConsignatarioPorCodigoPostal(fecha_inicial, fecha_final, sucursal):
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, sucursal: {sucursal}")


    if sucursal == "ALL":
        filtro_sucursal = f"AND KDM1.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDM1.C1 = '{sucursal}'" 

    with connection.cursor() as cursor:
        query = f"""
            DECLARE
                @fecha_inicial VARCHAR(20) = %s,
                @fecha_final VARCHAR(20) = %s,
                @sucursal VARCHAR(20) = %s;
            
            SELECT 
                ISNULL(LTRIM(RTRIM(A.CP)), '-vacio-') AS 'CP',
                ISNULL(A.COLONIA, '-vacio-') AS 'colonia',
                ISNULL(A.SEGMENTACION, '-vacio-') AS 'segmentacion',
                COUNT(*) AS 'cantidad'
            FROM (
                SELECT DISTINCT
                    KDVDIREMB.C7 AS 'CP',
                    KDVDIREMB.C5 AS 'COLONIA',
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
                    AND KDM1.C12 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    AND KDM1.C2 = 'U'
                    AND KDM1.C3 = 'D'
                    AND KDM1.C4 IN ('5', '45')
                    AND KDM1.C5 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '86', '87', '88', '94', '96', '97')
            ) AS A
            GROUP BY A.CP, A.SEGMENTACION, A.COLONIA
            ORDER BY A.CP, A.SEGMENTACION, A.COLONIA;
        """

        params = [
                    fecha_inicial, fecha_final, sucursal
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