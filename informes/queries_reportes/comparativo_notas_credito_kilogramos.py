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

#Incompleta
def consultaComparativoNotasCreditoKilogramos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}")

    # Calcula las fechas del año anterior
    fecha_inicial_year_anterior = fecha_inicial.replace(year=fecha_inicial.year - 1)
    fecha_final_year_anterior = fecha_final.replace(year=fecha_final.year - 1)

    actual_year = str(fecha_inicial.year)
    last_year = str(fecha_inicial.year - 1)


    with connection.cursor() as cursor:
        query = f"""
            -- Declaración de variables
            DECLARE
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @fecha_inicial_year_anterior DATE = CONVERT(DATE, %s, 102),
                @fecha_final_year_anterior DATE = CONVERT(DATE, %s, 102), 
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s;

            -- Consulta genérica con cálculos del año actual y anterior
            SELECT 
                COALESCE(DatosActual.ZONA, DatosAnterior.ZONA) AS zona,
                COALESCE(DatosActual.SUC, DatosAnterior.SUC) AS clave_sucursal,
                COALESCE(DatosActual.SUCURSALNOMBRE, DatosAnterior.SUCURSALNOMBRE) AS sucursal,
                ISNULL(DatosAnterior.NotaCreditoConProducto_ANTERIOR, 0) AS nota_credito_{last_year}_kg,
                ISNULL(DatosActual.NotaCreditoConProducto_ACTUAL, 0) AS nota_credito_{actual_year}_kg,
                ISNULL(DatosActual.NotaCreditoConProducto_ACTUAL, 0) - ISNULL(DatosAnterior.NotaCreditoConProducto_ANTERIOR, 0) AS diferencia_kg,
                CASE 
                    WHEN ISNULL(DatosAnterior.NotaCreditoConProducto_ANTERIOR, 0) = 0 THEN NULL  -- Evitar división por cero
                    ELSE (ISNULL(DatosActual.NotaCreditoConProducto_ACTUAL, 0) / ISNULL(DatosAnterior.NotaCreditoConProducto_ANTERIOR, 0) - 1) * 100 
                END AS crecimiento_porcentual
            FROM (
                SELECT
                    DatosActual.zona AS ZONA,
                    DatosActual.SUC AS SUC,
                    DatosActual.SUCURSALNOMBRE AS SUCURSALNOMBRE,
                    SUM(ISNULL(DatosActual.VENTAS_ACTUAL, 0)) AS VENTAS_ACTUAL,
                    (SUM(ISNULL(DatosActual.VENTAS_ACTUAL, 0)) - SUM(ISNULL(DatosActual.NotaCreditoConProducto_ACTUAL, 0))) NotaCreditoConProducto_ACTUAL
                FROM (
                    -- Datos del año actual
                    SELECT 
                        CASE 
                            WHEN KDIJ.C1 IN ('02') THEN '1.-Vallejo'
                            WHEN KDIJ.C1 IN ('04', '15', '16', '17') THEN '2.-Norte'
                            WHEN KDIJ.C1 IN ('05', '08', '10', '19') THEN '3.-Centro'
                            WHEN KDIJ.C1 IN ('03', '09', '14', '12', '20') THEN '4.-Pacifico'
                            WHEN KDIJ.C1 IN ('07', '11', '13', '18') THEN '5.-Sureste'
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
                        SUM(CASE 
                            WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' AND KDIJ.C6 IN ('5', '45') 
                            THEN KDIJ.C11 * KDII.C13 
                            ELSE 0 
                        END) AS VENTAS_ACTUAL,
                        SUM(CASE 
                            WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 = '20' AND KDIJ.C7 = '24' 
                            THEN KDIJ.C11 * KDII.C13 
                            ELSE 0 
                        END) AS NotaCreditoConProducto_ACTUAL
                    FROM dbo.KDIJ
                    INNER JOIN dbo.KDMS ON KDIJ.C1 = KDMS.C1
                    INNER JOIN dbo.KDII ON KDIJ.C3 = KDII.C1
                    INNER JOIN dbo.KDUV ON KDIJ.C16 = KDUV.C2
                    WHERE
                        KDIJ.C10 BETWEEN @fecha_inicial AND @fecha_final  -- Filtrar por el año actual
                        AND KDIJ.C1 BETWEEN @producto_inicial AND @producto_final
                        AND KDIJ.C15 BETWEEN @cliente_inicial AND @cliente_final
                        AND KDIJ.C1 NOT IN ('06', '12')
                        AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    GROUP BY KDIJ.C1, KDUV.C22, KDMS.C2
                ) AS DatosActual
                GROUP BY DatosActual.zona, DatosActual.SUC, DatosActual.SUCURSALNOMBRE
            ) AS DatosActual
            FULL JOIN (
                SELECT
                    DatosAnterior.zona AS ZONA,
                    DatosAnterior.SUC AS SUC,
                    DatosAnterior.SUCURSALNOMBRE AS SUCURSALNOMBRE,
                    SUM(ISNULL(DatosAnterior.VENTAS_ANTERIOR, 0)) AS VENTAS_ANTERIOR,
                    (SUM(ISNULL(DatosAnterior.VENTAS_ANTERIOR, 0)) - SUM(ISNULL(DatosAnterior.NotaCreditoConProducto_ANTERIOR, 0))) NotaCreditoConProducto_ANTERIOR
                FROM (
                    -- Datos del año anterior
                    SELECT 
                        CASE 
                            WHEN KDIJ.C1 IN ('02') THEN '1.-Vallejo'
                            WHEN KDIJ.C1 IN ('04', '15', '16', '17') THEN '2.-Norte'
                            WHEN KDIJ.C1 IN ('05', '08', '10', '19') THEN '3.-Centro'
                            WHEN KDIJ.C1 IN ('03', '09', '14', '12', '20') THEN '4.-Pacifico'
                            WHEN KDIJ.C1 IN ('07', '11', '13', '18') THEN '5.-Sureste'
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
                        SUM(CASE 
                            WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' AND KDIJ.C6 IN ('5', '45') 
                            THEN KDIJ.C11 * KDII.C13 
                            ELSE 0 
                        END) AS VENTAS_ANTERIOR,
                        SUM(CASE 
                            WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 = '20' AND KDIJ.C7 = '24' 
                            THEN KDIJ.C11 * KDII.C13 
                            ELSE 0 
                        END) AS NotaCreditoConProducto_ANTERIOR
                    FROM dbo.KDIJ
                    INNER JOIN dbo.KDMS ON KDIJ.C1 = KDMS.C1
                    INNER JOIN dbo.KDII ON KDIJ.C3 = KDII.C1
                    INNER JOIN dbo.KDUV ON KDIJ.C16 = KDUV.C2
                    WHERE 
                        KDIJ.C10 BETWEEN @fecha_inicial_year_anterior AND @fecha_final_year_anterior  -- Filtrar por el año anterior
                        AND KDIJ.C1 BETWEEN @producto_inicial AND @producto_final
                        AND KDIJ.C15 BETWEEN @cliente_inicial AND @cliente_final
                        AND KDIJ.C1 NOT IN ('06', '12')
                        AND KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    GROUP BY KDIJ.C1, KDUV.C22, KDMS.C2
                ) AS DatosAnterior
                GROUP BY DatosAnterior.zona, DatosAnterior.SUC, DatosAnterior.SUCURSALNOMBRE
            ) AS DatosAnterior ON DatosActual.SUC = DatosAnterior.SUC
            ORDER BY 1, 2;


        """

        params = [ 
                  fecha_inicial, fecha_final, 
                  fecha_inicial_year_anterior, fecha_final_year_anterior,
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