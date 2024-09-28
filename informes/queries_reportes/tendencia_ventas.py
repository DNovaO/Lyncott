# Description: Consulta de ventas por crédito contable
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaTendenciaVentas(fecha_inicial, fecha_final):
    print (f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}")

    with connection.cursor() as cursor:
        query = f"""
            SET LANGUAGE Español;        
        
            DECLARE @fecha_inicial VARCHAR(20) = %s,
                    @fecha_final VARCHAR(20) = %s;
            
            SELECT
                CASE
                    WHEN DATEPART(dw, KDM1.C9) = 1 THEN 'Lunes'
                    WHEN DATEPART(dw, KDM1.C9) = 2 THEN 'Martes'
                    WHEN DATEPART(dw, KDM1.C9) = 3 THEN 'Miercoles'
                    WHEN DATEPART(dw, KDM1.C9) = 4 THEN 'Jueves'
                    WHEN DATEPART(dw, KDM1.C9) = 5 THEN 'Viernes'
                    WHEN DATEPART(dw, KDM1.C9) = 6 THEN 'Sabado'
                    ELSE '-'
                END AS dia,
                FORMAT(KDM1.C9, 'dd/MM/yyyy') AS fecha,
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

        params = [
                    fecha_inicial, fecha_final,
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