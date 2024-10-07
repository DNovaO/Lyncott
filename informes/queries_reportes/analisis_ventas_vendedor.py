# Description: Consulta Analisis Ventas Vendedor
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *

def consultaAnalisisVentasVendedor  (fecha_inicial, fecha_final, producto_inicial, producto_final, cliente_inicial, cliente_final, vendedor_inicial, vendedor_final, sucursal):
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}, sucursal: {sucursal}")
    
    fecha_inicial_year_anterior = fecha_inicial.replace(year=fecha_inicial.year - 1)
    fecha_final_year_anterior = fecha_final.replace(year=fecha_final.year - 1)

    actual_year = str(fecha_inicial.year)
    last_year = str(fecha_inicial.year - 1)

    filtro_sucursal = ""
    
    if sucursal == 'ALL':
        filtro_sucursal = """
            AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
        """
    else:
        filtro_sucursal = f"""
            AND KDIJ.C16 >= '{vendedor_inicial}' AND KDIJ.C16 <= '{vendedor_final}'
            AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
            AND KDIJ.C1 = '{sucursal}'
        """

    with connection.cursor() as cursor:
        query = f"""
            DECLARE 
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @fecha_inicial_year_anterior DATE = CONVERT(DATE, %s, 102),
                @fecha_final_year_anterior DATE = CONVERT(DATE, %s, 102),
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s,
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @vendedor_inicial VARCHAR(20) = %s,
                @vendedor_final VARCHAR(20) = %s,
                @sucursal VARCHAR(20) = %s;
                
            WITH DatosAnt AS (
                SELECT 
                    KDUV.C2 AS clave_vendedor, 
                    KDUV.C3 AS nombre_vendedor,
                    SUM(KDIJ.C11) AS cantidad_{last_year}, 
                    SUM(KDIJ.C11 * KDII.C13) AS kgslts_{last_year}, 
                    SUM(KDIJ.C14) AS venta_{last_year}
                FROM KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1
                INNER JOIN KDM1 ON KDIJ.C1 = KDM1.C1 
                    AND KDIJ.C4 = KDM1.C2 
                    AND KDIJ.C5 = KDM1.C3 
                    AND KDIJ.C6 = KDM1.C4
                    AND KDIJ.C7 = KDM1.C5 
                    AND KDIJ.C8 = KDM1.C6
                INNER JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 
                    AND KDM1.C181 = KDVDIREMB.C2
                WHERE 
                    KDIJ.C10 >= @fecha_inicial_year_anterior
                    AND KDIJ.C10 <= @fecha_final_year_anterior
                    AND KDII.C1 >= @producto_inicial 
                    AND KDII.C1 <= @producto_final
                    AND KDUD.C2 >= @cliente_inicial
                    AND KDUD.C2 <= @cliente_final
                    {filtro_sucursal}
                    AND KDIJ.C4 = 'U' 
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                GROUP BY KDUV.C2, KDUV.C3
            ),
            DatosAct AS (
                SELECT 
                    KDUV.C2 AS clave_vendedor, 
                    KDUV.C3 AS nombre_vendedor,
                    SUM(KDIJ.C11) AS cantidad_{actual_year}, 
                    SUM(KDIJ.C11 * KDII.C13) AS kgslts_{actual_year}, 
                    SUM(KDIJ.C14) AS venta_{actual_year}
                FROM KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1
                INNER JOIN KDM1 ON KDIJ.C1 = KDM1.C1 
                    AND KDIJ.C4 = KDM1.C2 
                    AND KDIJ.C5 = KDM1.C3 
                    AND KDIJ.C6 = KDM1.C4
                    AND KDIJ.C7 = KDM1.C5 
                    AND KDIJ.C8 = KDM1.C6
                INNER JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 
                    AND KDM1.C181 = KDVDIREMB.C2
                WHERE 
                    KDIJ.C10 >= @fecha_inicial
                    AND KDIJ.C10 <= @fecha_final
                    AND KDII.C1 >= @producto_inicial
                    AND KDII.C1 <= @producto_final
                    AND KDUD.C2 >= @cliente_inicial
                    AND KDUD.C2 <= @cliente_final
                    {filtro_sucursal}
                    AND KDIJ.C4 = 'U' 
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                GROUP BY KDUV.C2, KDUV.C3
            )
            SELECT 
                COALESCE(DatosAnt.clave_vendedor, DatosAct.clave_vendedor) AS clave_vendedor,
                COALESCE(DatosAnt.nombre_vendedor, DatosAct.nombre_vendedor) AS nombre_vendedor,
                SUM(DatosAnt.cantidad_{last_year}) AS cantidad_{last_year},
                SUM(DatosAnt.kgslts_{last_year}) AS kgslts_{last_year},
                SUM(DatosAnt.venta_{last_year}) AS venta_{last_year},
                SUM(DatosAct.cantidad_{actual_year}) AS cantidad_{actual_year},
                SUM(DatosAct.kgslts_{actual_year}) AS kgslts_{actual_year},
                SUM(DatosAct.venta_{actual_year}) AS venta_{actual_year}
            FROM DatosAnt
            FULL OUTER JOIN DatosAct 
                ON DatosAnt.clave_vendedor = DatosAct.clave_vendedor
                AND DatosAnt.nombre_vendedor = DatosAct.nombre_vendedor
            GROUP BY 
                COALESCE(DatosAnt.clave_vendedor, DatosAct.clave_vendedor),
                COALESCE(DatosAnt.nombre_vendedor, DatosAct.nombre_vendedor)
            ORDER BY clave_vendedor;
        """

        params = [
            fecha_inicial, fecha_final,
            fecha_inicial_year_anterior, fecha_final_year_anterior,
            producto_inicial, producto_final,
            cliente_inicial, cliente_final,
            vendedor_inicial, vendedor_final,
            sucursal,
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
