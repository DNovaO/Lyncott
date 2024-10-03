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


def consultaAvanceVentas(fecha_inicial, fecha_final, sucursal):
    print (f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, sucursal: {sucursal}")
    
    dif_dias = f_DifDias(fecha_inicial, fecha_final, [])
    dif_dias_totales = f_DifDiasTotales(fecha_inicial, fecha_final, [])
    
    if sucursal == 'ALL':
        sucursal = '%'
        
    with connection.cursor() as cursor:
        query = f"""
            DECLARE 
                @Dias INT = %s,
                @DiasTotales INT = %s, 
                @fecha_inicial VARCHAR(20) = %s,
                @fecha_final VARCHAR(20) = %s,
                @sucursal VARCHAR(20) = %s;
            
            SELECT 
                DBKL2019.SUCURSAL AS sucursal,
                DBKL2019.IDVENDEDOR AS id_vendedor,
                DBKL2019.VENDEDOR AS vendedor,
                DBKL2019.IDALMACEN AS id_almacen,
                ISNULL(DBKL2019.ENTREGADO_P, 0) AS entregado,
                ISNULL(DBKL2019.VENTA_P, 0) AS ventas,
                (ISNULL(DBKL2019.VENTA_P, 0)/@Dias*@DiasTotales) AS si_continuas_asi_cerraras,
                ISNULL(DBKL2019.DEVUELTO_MALO_P, 0) + ISNULL(DBKL2019.NOTA_FISICO_P, 0) AS devolucion,
                (ISNULL(DBKL2019.DEVUELTO_MALO_P, 0) + ISNULL(DBKL2019.NOTA_FISICO_P, 0)) / COALESCE(NULLIF(ISNULL(DBKL2019.VENTA_P, 0), 0), 1) * 100 AS porcentaje_devolucion,
                ISNULL(DBKL2019.PASEADO_P, 0) AS paseado,
                ISNULL(DBKL2019.PASEADO_P, 0) / COALESCE(NULLIF(ISNULL(DBKL2019.ENTREGADO_P, 0), 0), 1) * 100 AS porcentaje_paseado,
                ISNULL(DBKL2019.NC_P, 0) AS notas_credito,
                ISNULL(DBKL2019.VENTA_P, 0) - (ISNULL(DBKL2019.DEVUELTO_MALO_P, 0) + ISNULL(DBKL2019.NOTA_FISICO_P, 0)) - ISNULL(DBKL2019.NC_P, 0) AS venta_neta,
                ISNULL(DBKL2019.VTA_CONT_P, 0) AS venta_contado,
                DBKL2019.ZONA AS zona
            FROM (
                SELECT 
                    KDUV.C1 AS SUCURSAL,
                    LTRIM(RTRIM(KDUV.C2)) AS IDVENDEDOR,
                    KDUV.C24 AS IDALMACEN, 
                    LTRIM(RTRIM(KDUV.C3)) AS VENDEDOR, 
                    ISNULL(SUM(CASE 
                        WHEN KDIJ.C4 = 'N' AND KDIJ.C5 = 'A' AND KDIJ.C6 = '25' AND KDIJ.C7 IN ('2', '22') THEN 
                            CASE 
                                WHEN KDIJ.C1 IN ('02', '03', '04', '05', '08', '10', '11', '12', '13', '15', '16', '19') THEN KDIJ.C11 * KDII.C14
                                WHEN KDIJ.C1 IN ('07', '18') THEN KDIJ.C11 * KDII.C15 
                                WHEN KDIJ.C1 IN ('09', '14') THEN KDIJ.C11 * KDII.C16 
                                WHEN KDIJ.C1 IN ('17') THEN KDIJ.C11 * KDII.C17
                            END
                        END), 0) AS ENTREGADO_P, 
                    ISNULL(SUM(CASE 
                        WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' AND KDIJ.C6 IN ('5', '45') AND KDIJ.C7 IN ('3', '4', '5', '6', '18', '19', '25', '26') THEN KDIJ.C14 
                        END), 0) AS VENTA_P,
                    ISNULL(SUM(CASE 
                        WHEN KDIJ.C4 = 'N' AND KDIJ.C5 = 'D' AND KDIJ.C6 = '25' AND KDIJ.C7 IN ('4') THEN 
                            CASE 
                                WHEN KDIJ.C1 IN ('02', '03', '04', '05', '08', '10', '11', '12', '13', '15', '16', '19') THEN KDIJ.C11 * KDII.C14
                                WHEN KDIJ.C1 IN ('07', '18') THEN KDIJ.C11 * KDII.C15 
                                WHEN KDIJ.C1 IN ('09', '14') THEN KDIJ.C11 * KDII.C16 
                                WHEN KDIJ.C1 IN ('17') THEN KDIJ.C11 * KDII.C17
                            END
                        END), 0) AS DEVUELTO_MALO_P,
                    ISNULL(SUM(CASE 
                        WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'A' AND KDIJ.C6 = '20' THEN KDIJ.C14 
                        END), 0) AS NC_P,                
                    ISNULL(SUM(CASE 
                        WHEN KDIJ.C4 = 'N' AND KDIJ.C5 = 'D' AND KDIJ.C6 = '25' AND KDIJ.C7 IN ('3') THEN 
                            CASE 
                                WHEN KDIJ.C1 IN ('02', '03', '04', '05', '08', '10', '11', '12', '13', '15', '16', '19') THEN KDIJ.C11 * KDII.C14
                                WHEN KDIJ.C1 IN ('07', '18') THEN KDIJ.C11 * KDII.C15
                                WHEN KDIJ.C1 IN ('09', '14') THEN KDIJ.C11 * KDII.C16
                                WHEN KDIJ.C1 IN ('17') THEN KDIJ.C11 * KDII.C17
                            END
                        END), 0) AS PASEADO_P, 
                    ISNULL(SUM(CASE 
                        WHEN KDIJ.C4 = 'N' AND KDIJ.C5 = 'D' AND KDIJ.C6 = '25' AND KDIJ.C7 IN ('12') THEN KDIJ.C14 
                        END), 0) AS NOTA_FISICO_P,
                    ISNULL(SUM(CASE 
                        WHEN KDIJ.C4 = 'U' AND KDIJ.C5 = 'D' AND KDIJ.C6 IN ('5', '45') AND KDIJ.C7 IN ('4', '6', '19', '26') THEN KDIJ.C14 
                        END), 0) AS VTA_CONT_P,
                    CASE 
                        WHEN KDUV.C22 = '1' AND KDUV.C1 = '02' THEN '1-Autoservicio'
                        WHEN KDUV.C22 = '2' AND KDUV.C1 = '02' THEN '2-Norte'
                        WHEN KDUV.C22 = '3' AND KDUV.C1 = '02' THEN '3-Sur'
                        WHEN KDUV.C22 = '4' AND KDUV.C1 = '02' THEN '4-Vent. Especiales'
                        WHEN KDUV.C22 = '5' AND KDUV.C1 = '02' THEN '5-Cadenas'
                        ELSE ''
                    END AS ZONA
                FROM KDIJ 
                INNER JOIN KDUV ON KDIJ.C1 = KDUV.C1 AND KDIJ.C2 = KDUV.C24
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                WHERE 
                    KDIJ.C1 LIKE @sucursal
                    AND KDIJ.C10 >= CONVERT(DATETIME, @fecha_inicial, 102)
                    AND KDIJ.C10 <= CONVERT(DATETIME, @fecha_final, 102)
                    AND KDIJ.C2 NOT IN ('92', '921', '922', '923', '924')
                GROUP BY 
                    KDUV.C1, 
                    KDUV.C2, 
                    KDUV.C3, 
                    KDUV.C24, 
                    KDUV.C22
            ) AS DBKL2019;

        """

        params = [
                    dif_dias, dif_dias_totales,
                    fecha_inicial, fecha_final,
                    sucursal
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