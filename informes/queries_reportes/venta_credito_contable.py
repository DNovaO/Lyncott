# Description: Consulta de ventas por crédito contable
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaVentaPorCreditoContable(fecha_inicial, fecha_final, cliente_inicial, cliente_final):
    print(f"Consulta de ventas por crédito contable desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial}, cliente final: {cliente_final}")
        
    with connection.cursor() as cursor:
        query = """
            DECLARE @cliente_inicial AS VARCHAR(10) = %s,
                    @cliente_final AS VARCHAR(10) = %s, 
                    @fecha_inicial AS DATETIME = %s,
                    @fecha_final AS DATETIME = %s;

            SELECT 
                CASE    
                    WHEN IEPS.ZONA  = '02' THEN '1.-Vallejo' 
                    WHEN IEPS.ZONA IN ('17','04','15','16') THEN '2.-Norte'
                    WHEN IEPS.ZONA IN ('05','10','19','08') THEN '3.-Centro'
                    WHEN IEPS.ZONA IN ('09','14','12','03','20','06') THEN '4.-Pacifico'
                    WHEN IEPS.ZONA IN ('13','11','18','07') THEN '5.-Sureste'
                    ELSE 'Sin zona' 
                END AS zona,
                
                CASE 
                    WHEN IEPS.SUC  = '1' THEN  '1 - Autoservicio'
                    WHEN IEPS.SUC  = '2' THEN  '2 - Norte'
                    WHEN IEPS.SUC  = '3' THEN  '3 - Sur'
                    WHEN IEPS.SUC  = '4' THEN  '4 - Vent. Especiales'
                    WHEN IEPS.SUC  = '5' THEN  '5 - Cadenas'
                    WHEN IEPS.SUC  = '6' THEN  '6 - Centro'
                    ELSE LTRIM(RTRIM(IEPS.SUC)) + ' - ' + SUCURSAL.C2
                END AS sucursal,
                
                SUM(IEPS.CONT) AS contado,
                SUM(IEPS.CONT) / (SUM(IEPS.CONT) + SUM(IEPS.CRED)) * 100 AS porcentaje_contable,
                SUM(IEPS.CRED) AS credito,
                SUM(IEPS.CRED) / (SUM(IEPS.CONT) + SUM(IEPS.CRED)) * 100 AS porcentaje_credito,
                SUM(IEPS.CONT) + SUM(IEPS.CRED) AS total
            FROM (
                SELECT  
                    KDM1.C1 AS Zona,
                    CASE 
                        WHEN KDM1.C1 = '02' THEN KDUV.C22      
                        ELSE KDM1.C1 
                    END AS SUC,
                    SUM(CASE WHEN KDM1.C5 IN ('2','4','6','19','22','26') THEN COALESCE(KDM1.C16, 0) - COALESCE(KDM1.C15, 0) END) AS CONT,
                    SUM(CASE WHEN KDM1.C5 IN ('2','4','6','19','22','26') THEN COALESCE(KDM1.C15, 0) END) AS IEPS_CON,
                    SUM(CASE WHEN KDM1.C5 IN ('1','3','5','18','21','25') THEN COALESCE(KDM1.C16, 0) - COALESCE(KDM1.C15, 0) END) AS CRED,
                    SUM(CASE WHEN KDM1.C5 IN ('1','3','5','18','21','25') THEN COALESCE(KDM1.C15, 0) END) AS IEPS_CRE
                FROM KDM1
                INNER JOIN KDUV ON KDM1.C12 = KDUV.C2
                WHERE
                    KDM1.C10 BETWEEN @cliente_inicial AND @cliente_final 
                    AND KDM1.C9 BETWEEN @fecha_inicial AND @fecha_final
                    AND KDM1.C2 = 'U'
                    AND KDM1.C3 = 'D'
                    AND KDM1.C4 IN ('5', '45')
                    AND KDM1.C5 IN ('2', '4', '6', '19', '22', '26', '1', '3', '5', '18', '21', '25')
                    AND KDM1.C43 <> 'C'
                GROUP BY KDM1.C1, KDUV.C22
            ) AS IEPS
            LEFT JOIN (
                SELECT c1, c2 FROM KDMS
            ) AS SUCURSAL ON IEPS.SUC = SUCURSAL.C1
            GROUP BY IEPS.Zona, IEPS.SUC, SUCURSAL.c2;

        """

        params = [ cliente_inicial, cliente_final, fecha_inicial, fecha_final ]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        
        
    return result