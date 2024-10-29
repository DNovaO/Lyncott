#Description: Consulta de ventas foodservice KAM
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *

def consultaVentasAutoServiceKAM(fecha_inicial, fecha_final, producto_inicial, producto_final,sucursal_inicial, sucursal_final):
    
    print(f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final} producto_inicial: {producto_inicial} producto_final: {producto_final} sucursal_inicial: {sucursal_inicial} sucursal_final: {sucursal_final}")
    
    # Obtener los valores tanto de f_DifDias como de f_DifDiasTotales
    dif_dias = f_DifDias(fecha_inicial, fecha_final, [])
    dif_dias_totales = f_DifDiasTotales(fecha_inicial, fecha_final, [])

    # Calcula las fechas del año anterior
    fecha_inicial_year_anterior = fecha_inicial.replace(year=fecha_inicial.year - 1)
    fecha_final_year_anterior = fecha_final.replace(year=fecha_final.year - 1)
    
    
    actual_year = str(fecha_inicial.year)
    last_year = str(fecha_inicial.year - 1)
    
    if sucursal_inicial == 'ALL' and sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_inicial == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    elif sucursal_final == 'ALL':
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDIJ.C1 BETWEEN '{sucursal_inicial}' AND '{sucursal_final}'"

    
    with connection.cursor() as cursor:
        query = f"""
            SET LANGUAGE Español;
        
            DECLARE
                @Dias INT = %s,
                @DiasTotales INT = %s,
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @fecha_inicial_year_anterior DATE = CONVERT(DATE, %s, 102),
                @fecha_final_year_anterior DATE = CONVERT(DATE, %s, 102),
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s,
                @sucursal_inicial VARCHAR(2) = %s,
                @sucursal_final VARCHAR(2) = %s;
                
            SELECT 
                aut.wecs_system AS KAM,
                LTRIM(RTRIM(aut.CADENA)) AS cadena,
                LTRIM(RTRIM(aut.DESCRIPCION)) AS "descripcion",
                ISNULL(X.VENTA, 0) AS "ventas_{last_year}",
                ISNULL(aut.VENTA, 0) AS "ventas_{actual_year}",
                ISNULL(aut.VENTA / @Dias, 0) AS "venta_por_dia",
                ISNULL(aut.VENTA / @Dias * @DiasTotales, 0) AS "proyeccion",
                CAST(ROUND(ISNULL(((aut.VENTA / ISNULL(x.VENTA, aut.VENTA / 2)) - 1) * 100, 0), 2) AS decimal(18, 2)) AS "porcentaje_crecimiento_o_decrecimiento" 
            FROM (
                SELECT 
                    KL2020.CADENA AS CADENA,
                    KL2020.DESCRIPCION AS DESCRIPCION,
                    KL2020.CLAVE AS CLAVE,
                    ISNULL(KL2020.VENTA, 0) AS VENTA,
                    KL2020.wecs_system AS wecs_system
                FROM (
                    SELECT 
                        KDUD.C1,
                        KDUD.C2 AS CADENA,
                        KDUD.C3 AS DESCRIPCION,
                        KDUD.C66 AS CLAVE,
                        SUM(dbo.KDIJ.C14) AS VENTA,
                        CASE 
                            WHEN KDUD.C2 IN (
                                'CAU01', 'PCM01', 'ISS01', 'PAR01', 'PAR13', 'PAR14', 
                                'PAR25', 'PAR26', 'PAR28', 'PAR29', 'PAR30', 'PAR31', 
                                'PAR32', 'PAR33', 'PAR35', 'PAR36', 'PAR48', 'PAR51', 
                                'PAR52', 'PAR55', 'PAR58', 'PAR63', 'PAR64', 'PAR65', 
                                'PAR67', 'PAR67', 'PAR72', 'PAR01', 'PAR75', 'PAR01') 
                            THEN 'KAM 1'
                            WHEN KDUD.C2 IN ('AUR01', 'AUR10') 
                            THEN 'KAM 2'
                            WHEN KDUD.C2 IN (
                                'TSO01', 'TSO02', 'TSO03', 'TSO04', 'GOAG', 'MACD', 
                                'GALB', 'GALS01', 'GLIV', 'GIHOP', 'GCALL', 'SIH01', 
                                'SFN01', 'CDE01') 
                            THEN 'KAM 3'
                            WHEN KDUD.C2 IN (
                                'CCF04', 'OFU01', 'TCH01', 'GBIM', 'GGOM01', 'GOXO01', 
                                'GPACI', 'GSEV01', 'GHOTS', 'GRCOS', 'GSG', 'GTO01', 
                                'GPRIS', 'GPES01', 'CLE01') 
                            THEN 'KAM 4'
                            ELSE 'KAM indefinido'
                        END AS wecs_system
                    FROM 
                        KDIJ
                    INNER JOIN 
                        KDII ON KDIJ.C3 = KDII.C1
                    INNER JOIN 
                        KDUD ON KDIJ.C15 = KDUD.C2
                    WHERE 
                        KDII.C1 >= @producto_inicial
                        AND KDII.C1 <=  @producto_final
                        AND KDIJ.C10 >= @fecha_inicial
                        AND KDIJ.C10 <= @fecha_final
                        {filtro_sucursal}
                        AND KDUD.C2 IN (
                            'CAU01', 'CCF04', 'PCM01', 'TCH01', 'OFU01', 'TSO01', 
                            'TSO03', 'TSO04', 'SIH01', 'TSO02', 'GOAG', 'MACD', 
                            'GALB', 'GALS01', 'GLIV', 'GIHOP', 'AUR01', 'AUR10', 
                            'ISS01', 'GBIM0', 'GCALL', 'GGOM01', 'GOXO01', 'GPACI', 
                            'GSEV01', 'GHOTS', 'GRCOS', 'GSG', 'GTO01', 'GPRIS', 
                            'GPES01', 'SFN01', 'CDE01', 'CLE01', 'PAR01', 
                            'PAR13', 'PAR14', 'PAR25', 'PAR26', 'PAR28', 'PAR29', 
                            'PAR30', 'PAR31', 'PAR32', 'PAR33', 'PAR35', 'PAR36', 
                            'PAR48', 'PAR51', 'PAR52', 'PAR55', 'PAR58', 'PAR63', 
                            'PAR64', 'PAR65', 'PAR67', 'PAR67', 'PAR72', 'PAR01', 
                            'PAR75', 'PAR01')
                        AND KDIJ.C16 NOT IN (
                            '902', '903', '904', '905', '906', '907', '908', '909', 
                            '910', '911', '912', '913', '914', '915', '916', '917', 
                            '918', '919', '920', '921', '922', '923', '924')
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND (dbo.KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                        AND KDIJ.C7 IN (
                            '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', 
                            '22', '25', '26', '71', '72', '73', '74', '75', '76', 
                            '77', '78', '79', '80', '86', '87', '88', '96', '97')
                    GROUP BY 
                        KDUD.C66, KDUD.C1, KDUD.C2, KDUD.C3
                ) AS KL2020 
            ) AS aut  
            LEFT JOIN (
                SELECT 
                    KDUD.C1,
                    KDUD.C66 AS CLAVE,
                    SUM(dbo.KDIJ.C14) AS VENTA,
                    KDUD.C2 AS CADENA
                FROM 
                    KDIJ
                INNER JOIN 
                    KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN 
                    KDUD ON KDIJ.C15 = KDUD.C2
                WHERE 
                    KDII.C1 >= @producto_inicial
                    AND KDII.C1 <= @producto_final
                    AND KDIJ.C10 >= @fecha_inicial_year_anterior
                    AND KDIJ.C10 <= @fecha_final_year_anterior
                    {filtro_sucursal}
                    AND KDUD.C2 IN (
                        'CAU01', 'CCF04', 'PCM01', 'TCH01', 'OFU01', 'TSO01', 
                        'TSO03', 'TSO04', 'SIH01', 'TSO02', 'GOAG', 'MACD', 
                        'GALB', 'GALS01', 'GLIV', 'GIHOP', 'AUR01', 'AUR10', 
                        'ISS01', 'GBIM0', 'GCALL', 'GGOM01', 'GOXO01', 'GPACI', 
                        'GSEV01', 'GHOTS', 'GRCOS', 'GSG', 'GTO01', 'GPRIS', 
                        'GPES01', 'SFN01', 'CDE01', 'CLE01', 'PAR01', 
                        'PAR13', 'PAR14', 'PAR25', 'PAR26', 'PAR28', 'PAR29', 
                        'PAR30', 'PAR31', 'PAR32', 'PAR33', 'PAR35', 'PAR36', 
                        'PAR48', 'PAR51', 'PAR52', 'PAR55', 'PAR58', 'PAR63', 
                        'PAR64', 'PAR65', 'PAR67', 'PAR67', 'PAR72', 'PAR01', 
                        'PAR75', 'PAR01')
                    AND KDIJ.C16 NOT IN (
                        '902', '903', '904', '905', '906', '907', '908', '909', 
                        '910', '911', '912', '913', '914', '915', '916', '917', 
                        '918', '919', '920', '921', '922', '923', '924')
                    AND KDIJ.C4 = 'U'
                    AND KDIJ.C5 = 'D'
                    AND (dbo.KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                    AND KDIJ.C7 IN (
                        '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', 
                        '22', '25', '26', '71', '72', '73', '74', '75', '76', 
                        '77', '78', '79', '80', '86', '87', '88', '96', '97')
                GROUP BY 
                    KDUD.C66, KDUD.C2, KDUD.C1
            ) AS X ON aut.CADENA = X.CADENA
            ORDER BY KAM, aut.CADENA;

                
        """
        
        params = [
                dif_dias, dif_dias_totales,
                fecha_inicial, fecha_final,
                fecha_inicial_year_anterior, fecha_final_year_anterior,
                producto_inicial, producto_final,
                sucursal_inicial, sucursal_final,
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
