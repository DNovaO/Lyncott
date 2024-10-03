#Description: Consulta de ventas por tipo de cliente sin refacturación
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaVentasPorTipoClienteSinRefacturacion(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    print (f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, cliente_inicial: {cliente_inicial}, cliente_final: {cliente_final}, producto_inicial: {producto_inicial}, producto_final: {producto_final}")
    
    with connection.cursor() as cursor:
        query = f"""
            DECLARE 
                @fecha_inicial VARCHAR(20) = %s,
                @fecha_final VARCHAR(20) = %s,
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s;

            SELECT 
                DBKL2019.ZONA AS 'zona',
                DBKL2019.No AS 'No',
                DBKL2019.SUCURSAL AS 'sucursal',
                ISNULL(DBKL2019.KG_AUTOSERVICIO, 0) AS 'kg_autoservicio',
                ISNULL(DBKL2019.PESOS_AUTOSERVICIO, 0) AS 'pesos_autoservicio',
                ISNULL(DBKL2019.KG_FOODSERVICE, 0) AS 'kg_foodservice',
                ISNULL(DBKL2019.PESOS_FOODSERVICE, 0) AS 'pesos_foodservice',
                ISNULL(DBKL2019.KG_TOTAL, 0) AS 'kg_total',
                ISNULL(DBKL2019.PESOS_TOTAL, 0) AS 'pesos_total'
            FROM (
                -- Zonas Vallejo Autoservicio
                SELECT 
                    '1.-Vallejo' AS 'ZONA',
                    KDUV.C22 AS 'No',
                    CASE
                        WHEN KDUV.C22 IN ('1') THEN 'Autoservicio'
                        WHEN KDUV.C22 IN ('2') THEN 'Norte'
                        WHEN KDUV.C22 IN ('3') THEN 'Sur'
                        WHEN KDUV.C22 IN ('4') THEN 'Vent. Especial'
                        WHEN KDUV.C22 IN ('5') THEN 'Cadenas'
                        WHEN KDUV.C22 IN ('6') THEN 'Centro'
                        ELSE 'Sucursal sin asignar'
                    END AS 'SUCURSAL',
                    ISNULL(SUM(KDIJ.C11 * KDII.C13), 0) AS 'KG_AUTOSERVICIO',
                    ISNULL(SUM(KDIJ.C14), 0) AS 'PESOS_AUTOSERVICIO',
                    '0' AS 'KG_FOODSERVICE',
                    '0' AS 'PESOS_FOODSERVICE',
                    ISNULL(SUM(KDIJ.C11 * KDII.C13), 0) AS 'KG_TOTAL',
                    ISNULL(SUM(KDIJ.C14), 0) AS 'PESOS_TOTAL'
                FROM KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                WHERE 
                    KDII.C1 BETWEEN @producto_inicial AND @producto_final
                    AND KDIJ.C10 BETWEEN CONVERT(DATETIME, @fecha_inicial, 102) AND CONVERT(DATETIME, @fecha_final, 102)
                    AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C1 = '02'
                    AND KDIJ.C7 IN (
                        '1', '2', '3', '4', '5', '6', '18', '19', '20', '21',
                        '22', '25', '26', '71', '72', '73', '74', '75', '76',
                        '77', '78', '79', '80', '81', '82', '86', '87', '88',
                        '94', '96', '97'
                    )
                    AND KDUV.C22 = '1'
                    AND KDIJ.C16 NOT IN (
                        '902', '903', '904', '905', '906', '907', '908', '909',
                        '910', '911', '912', '913', '914', '915', '916', '917',
                        '918', '919', '920', '921', '922', '923', '924'
                    )
                GROUP BY 
                    KDUV.C22, 
                    KDIJ.C1

                UNION 

                -- Foodservice Vallejo Zonas
                SELECT
                    '1.-Vallejo' AS 'ZONA',
                    KDUV.C22 AS 'No',
                    CASE
                        WHEN KDUV.C22 IN ('1') THEN 'Autoservicio'
                        WHEN KDUV.C22 IN ('2') THEN 'Norte'
                        WHEN KDUV.C22 IN ('3') THEN 'Sur'
                        WHEN KDUV.C22 IN ('4') THEN 'Vent. Especial'
                        WHEN KDUV.C22 IN ('5') THEN 'Cadenas'
                        WHEN KDUV.C22 IN ('6') THEN 'Centro'
                        ELSE 'Sucursal sin asignar'
                    END AS 'SUCURSAL',
                    '0' AS 'KG',
                    '0' AS '$',
                    ISNULL(SUM(KDIJ.C11 * KDII.C13), 0) AS 'AUT',
                    ISNULL(SUM(KDIJ.C14), 0) AS 'AUTa',
                    ISNULL(SUM(KDIJ.C11 * KDII.C13), 0) AS 'KG',
                    ISNULL(SUM(KDIJ.C14), 0) AS 'PESOS'
                FROM KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                WHERE
                    KDII.C1 BETWEEN @producto_inicial AND @producto_final
                    AND KDIJ.C10 BETWEEN CONVERT(DATETIME, @fecha_inicial, 102) AND CONVERT(DATETIME, @fecha_final, 102)
                    AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND KDIJ.C6 IN ('5', '45')
                    AND KDIJ.C1 = '02'
                    AND KDIJ.C7 IN (
                        '1', '2', '3', '4', '5', '6', '18', '19', '20', '21',
                        '22', '25', '26', '71', '72', '73', '74', '75', '76',
                        '77', '78', '79', '80', '81', '82', '86', '87', '88',
                        '94', '96', '97'
                    )
                    AND KDUV.C22 IN ('2', '3', '4', '5', '6')
                    AND KDIJ.C16 NOT IN (
                        '902', '903', '904', '905', '906', '907', '908', '909',
                        '910', '911', '912', '913', '914', '915', '916', '917',
                        '918', '919', '920', '921', '922', '923', '924'
                    )
                GROUP BY 
                    KDUV.C22, 
                    KDIJ.C1

                UNION

                -- Código para Sucursales
                SELECT  
                    ISNULL(A.ZONA, B.ZONA) AS 'ZONA', 
                    ISNULL(A.No, B.S_D) AS 'No.', 
                    ISNULL(A.SUCURSAL, B.SUCURSAL) AS 'SUCURSAL', 
                    ISNULL(A.KG, 0) AS 'KG_AUTOSERVICIO', 
                    ISNULL(A.Dinero, 0) AS '$_AUTOSERVICIO',
                    ISNULL(B.KG, 0) AS 'KG_FOODSERVICE', 
                    ISNULL(B.Dinero, 0) AS '$_FOODSERVICE',
                    ISNULL(SUM(A.KG + B.KG), 0) AS 'KG_TOTAL',
                    ISNULL(SUM(A.Dinero + B.Dinero), 0) AS 'PESOS_TOTAL'
                FROM (
                    -- Autoservicio Sucursales
                    SELECT 
                        CASE
                            WHEN KDIJ.C1 IN ('17', '04', '15', '16') THEN '2.-Norte'
                            WHEN KDIJ.C1 IN ('05', '10', '19', '08') THEN '3.-Centro'
                            WHEN KDIJ.C1 IN ('09', '14', '03', '12', '06', '20') THEN '4.-Pacifico'
                            WHEN KDIJ.C1 IN ('13', '11', '18', '07') THEN '5.-Sureste'
                            ELSE 'Sin zona'
                        END AS 'ZONA',
                        KDIJ.C1 AS 'No',
                        KDMS.C2 AS 'SUCURSAL', /* Nombre de sucursal */
                        SUM(KDIJ.C11 * KDII.C13) AS 'KG',
                        SUM(KDIJ.C14) AS 'Dinero'
                    FROM KDIJ
                    INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                    INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                    INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1
                    WHERE 
                        KDII.C1 BETWEEN @producto_inicial AND @producto_final
                        AND KDIJ.C10 BETWEEN CONVERT(DATETIME, @fecha_inicial, 102) AND CONVERT(DATETIME, @fecha_final, 102)
                        AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND KDIJ.C6 IN ('5', '45')
                        AND KDIJ.C1 IN (
                            '03', '04', '15', '17', '05', '08', '10', '16',
                            '06', '09', '12', '14', '07', '11', '13', '18',
                            '19', '20'
                        )
                        AND KDUD.C33 = 'A'
                        AND KDIJ.C16 NOT IN (
                            '902', '903', '904', '905', '906', '907', '908', '909',
                            '910', '911', '912', '913', '914', '915', '916', '917',
                            '918', '919', '920', '921', '922', '923', '924'
                        )
                    GROUP BY 
                        KDIJ.C1, 
                        KDMS.C2
                ) AS A
                FULL JOIN (
                    -- Foodservice Sucursales
                    SELECT 
                        SUM(KDIJ.C11 * KDII.C13) AS 'KG', 
                        SUM(KDIJ.C14) AS 'Dinero',
                        CASE
                            WHEN KDIJ.C1 IN ('17', '04', '15', '16') THEN '2.-Norte'
                            WHEN KDIJ.C1 IN ('05', '10', '19', '08') THEN '3.-Centro'
                            WHEN KDIJ.C1 IN ('09', '14', '03', '12', '06', '20') THEN '4.-Pacifico'
                            WHEN KDIJ.C1 IN ('13', '11', '18', '07') THEN '5.-Sureste'
                            ELSE 'Sin zona'
                        END AS 'ZONA',
                        KDMS.C2 AS 'SUCURSAL', /* Nombre de sucursal */
                        KDIJ.C1 AS 'S_D'
                    FROM KDIJ
                    INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                    INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                    INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1
                    WHERE 
                        KDII.C1 BETWEEN @producto_inicial AND @producto_final
                        AND KDIJ.C10 BETWEEN CONVERT(DATETIME, @fecha_inicial, 102) AND CONVERT(DATETIME, @fecha_final, 102)
                        AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND KDIJ.C6 IN ('5', '45')
                        AND KDIJ.C1 IN (
                            '03', '04', '15', '17', '05', '08', '10', '16',
                            '06', '09', '12', '14', '07', '11', '13', '18',
                            '19', '20'
                        )
                        AND KDUD.C33 <> 'A'
                        AND KDIJ.C16 NOT IN (
                            '902', '903', '904', '905', '906', '907', '908', '909',
                            '910', '911', '912', '913', '914', '915', '916', '917',
                            '918', '919', '920', '921', '922', '923', '924'
                        )
                    GROUP BY 
                        KDIJ.C1, 
                        KDMS.C2
                ) AS B 
                ON A.No = B.S_D 
            GROUP BY 
                A.ZONA, 
                B.ZONA, 
                A.No, 
                B.S_D, 
                A.SUCURSAL, 
                B.SUCURSAL, 
                A.KG, 
                A.Dinero, 
                B.KG, 
                B.Dinero
            ) AS DBKL2019;

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