# Description: Consulta de ventas sin notas de crédito en pesos
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *

def consultaVentaSinNotaDeCreditoEnPesos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}")

    with connection.cursor() as cursor:
        query = f"""
            -- Declaración de variables
            DECLARE
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s;

            SELECT 
                DB.ZONA AS zona,
                DB.SUC AS clave_sucursal,
                DB.SUCURSALNOMBRE AS sucursal,
                SUM(DB.VENT) AS venta,
                SUM(DB.NoEntregado) AS nota_de_credito_no_entregado,
                SUM(DB.Devolucion) AS nota_de_credito_devolucion,
                SUM(DB.VENT) - SUM(DB.NoEntregado) - SUM(DB.Devolucion) AS venta_sin_nota_de_credito
            FROM (
                SELECT 
                    CASE 
                        WHEN KDIJ.C1 IN ('02') THEN '1.-Vallejo'
                        WHEN KDIJ.C1 IN ('04','15','16','17') THEN '2.-Norte'
                        WHEN KDIJ.C1 IN ('05','08','10','19') THEN '3.-Centro'
                        WHEN KDIJ.C1 IN ('03','09','14','12','20') THEN '4.-Pacifico'
                        WHEN KDIJ.C1 IN ('07','11','13','18') THEN '5.-Sureste'
                        ELSE 'Sin zona'
                    END AS ZONA,
                    
                    CASE 
                        WHEN KDIJ.C1 IN ('02') THEN LTRIM(RTRIM(KDUV.C22))
                        ELSE KDIJ.C1 
                    END AS SUC,
                    
                    CASE 
                        WHEN KDIJ.C1 IN ('02') THEN 
                            CASE 
                                WHEN KDUV.C22 = 1 THEN 'Autoservicio'
                                WHEN KDUV.C22 = 2 THEN 'Norte'
                                WHEN KDUV.C22 = 3 THEN 'Sur'
                                WHEN KDUV.C22 = 4 THEN 'Vent. Especiales'
                                WHEN KDUV.C22 = 5 THEN 'Cadenas'
                                ELSE 'Sin asignar a Vallejo'
                            END 
                        ELSE LTRIM(RTRIM(KDMS.C2))
                    END AS SUCURSALNOMBRE,
                    
                    ISNULL(SUM(CASE 
                        WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' AND KDIJ.C6 IN ('5','45') THEN KDIJ.C14 
                    END), 0) AS VENT,
                    
                    ISNULL(SUM(CASE 
                        WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 IN ('20') AND KDIJ.C7 IN ('24') THEN KDIJ.C14 
                    END), 0) AS NoEntregado,
                    
                    ISNULL(SUM(CASE 
                        WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 IN ('20') AND KDIJ.C7 IN ('26') THEN KDIJ.C14 
                    END), 0) AS Devolucion
                FROM 
                    KDIJ
                INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1 
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2 
                WHERE
                    KDIJ.C3 >= @producto_inicial
                    AND KDIJ.C3 <= @producto_final
                    AND KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDIJ.C15 >= @cliente_inicial
                    AND KDIJ.C15 <= @cliente_final
                    AND KDIJ.C16 NOT IN (
                        '902','903','904','905','906','907','908','909','910',
                        '911','912','913','914','915','916','917','918','919',
                        '920','921','922','923','924'
                    )
                GROUP BY KDIJ.C1, KDUV.C22, KDMS.C2
            ) AS DB
            GROUP BY DB.ZONA, DB.SUC, DB.SUCURSALNOMBRE
            ORDER BY 1, 2;


        """

        params = [ 
                  fecha_inicial, fecha_final, 
                  cliente_inicial, cliente_final, 
                  producto_inicial, producto_final
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