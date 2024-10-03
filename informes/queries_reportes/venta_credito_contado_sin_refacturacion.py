#Description: Consulta de ventas por credito contable sin refacturación
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaVentasDeCreditoContadoSinRefacturacion(fecha_inicial, fecha_final, cliente_inicial, cliente_final):
    print (f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}")
    
    with connection.cursor() as cursor:
        query = f"""
            DECLARE @fecha_inicial VARCHAR(20) = %s,
                    @fecha_final VARCHAR(20) = %s,
                    @cliente_inicial VARCHAR(20) = %s,
                    @cliente_final VARCHAR(20) = %s;
            
            WITH IEPS AS (
                SELECT  
                    KDM1.C1 AS Zona,
                    CASE 
                        WHEN KDM1.C1 = '02' THEN KDUV.C22      
                        ELSE KDM1.C1 
                    END AS SUC,
                    SUM(
                        CASE 
                            WHEN KDM1.C5 IN ('2', '4', '6', '19', '22', '26') 
                            THEN ISNULL(KDM1.C16, 0) - ISNULL(KDM1.C15, 0) 
                        END
                    ) AS CONT,
                    SUM(
                        CASE 
                            WHEN KDM1.C5 IN ('2', '4', '6', '19', '22', '26') 
                            THEN ISNULL(KDM1.C15, 0) 
                        END
                    ) AS IEPS_CON,
                    SUM(
                        CASE 
                            WHEN KDM1.C5 IN ('1', '3', '5', '18', '21', '25') 
                            THEN ISNULL(KDM1.C16, 0) - ISNULL(KDM1.C15, 0) 
                        END
                    ) AS CRED,
                    SUM(
                        CASE 
                            WHEN KDM1.C5 IN ('1', '3', '5', '18', '21', '25') 
                            THEN ISNULL(KDM1.C15, 0) 
                        END
                    ) AS IEPS_CRE
                FROM 
                    KDM1
                INNER JOIN 
                    KDUV ON KDM1.C12 = KDUV.C2
                WHERE
                    KDM1.C10 >= @cliente_inicial
                    AND KDM1.C10 <= @cliente_final
                    AND KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial, 102)
                    AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final, 102)
                    AND KDM1.C2 = 'U'
                    AND KDM1.C3 = 'D'
                    AND KDM1.C4 IN ('5', '45')
                    AND KDM1.C5 IN ('2', '4', '6', '19', '22', '26', '1', '3', '5', '18', '21', '25')
                    AND KDM1.C43 <> 'C'
                    AND KDM1.C12 NOT IN (
                        '902', '903', '904', '905', '906', '907', '908', '909',
                        '910', '911', '912', '913', '914', '915', '916', '917',
                        '918', '919', '920', '921', '922', '923', '924'
                    )
                GROUP BY 
                    KDM1.C1, 
                    KDUV.C22        
            )
            SELECT 
                CASE    
                    WHEN IEPS.Zona = '02' THEN '1.-Vallejo' 
                    WHEN IEPS.Zona IN ('17', '04', '15', '16') THEN '2.-Norte'
                    WHEN IEPS.Zona IN ('05', '10', '19', '08') THEN '3.-Centro'
                    WHEN IEPS.Zona IN ('09', '14', '12', '03', '20') THEN '4.-Pacifico'
                    WHEN IEPS.Zona IN ('13', '11', '18', '07') THEN '5.-Sureste'
                    ELSE 'Sin zona' 
                END AS zona,
            
                CASE 
                    WHEN IEPS.SUC = '1' THEN '1 - Autoservicio'
                    WHEN IEPS.SUC = '2' THEN '2 - Norte'
                    WHEN IEPS.SUC = '3' THEN '3 - Sur'
                    WHEN IEPS.SUC = '4' THEN '4 - Vent. Especiales'
                    WHEN IEPS.SUC = '5' THEN '5 - Cadenas'
                    WHEN IEPS.SUC = '6' THEN '6 - Centro'
                    ELSE LTRIM(RTRIM(IEPS.SUC)) + ' - ' + SUCURSAL.C2
                END AS sucursal,
            
                SUM(IEPS.CONT) AS contado,
                SUM(IEPS.CONT) / (SUM(IEPS.CONT) + SUM(IEPS.CRED)) * 100 AS porcentaje_contado,
                SUM(IEPS.CRED) AS credito,
                SUM(IEPS.CRED) / (SUM(IEPS.CONT) + SUM(IEPS.CRED)) * 100 AS porcentaje_credito,
                SUM(IEPS.CONT) + SUM(IEPS.CRED) AS total
            FROM IEPS
            LEFT JOIN (
                SELECT 
                    C1, 
                    C2 
                FROM KDMS
            ) AS SUCURSAL 
                ON IEPS.SUC = SUCURSAL.C1
            GROUP BY 
                IEPS.Zona, 
                IEPS.SUC, 
                SUCURSAL.C2;
        """

        params = [
                    fecha_inicial, fecha_final,
                    cliente_inicial, cliente_final
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