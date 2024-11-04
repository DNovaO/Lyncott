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

def consultaVentasFoodServiceKAM(fecha_inicial, fecha_final, producto_inicial, producto_final,sucursal_inicial, sucursal_final):
    
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
                aut.grupo AS "subgrupo",
                aut.seccion AS "KAM",
                aut.CADENA AS "cadena",
                Y.DESCRIPCION AS "descripcion",
                ISNULL(X.VENTA, 0) - ISNULL(W.VENTA, 0) AS "ventas_{last_year}_sin_cremero_OXXO",
                ISNULL(V.VENTA, 0) AS "ventas_{last_year}_cremero_OXXO", 
                ISNULL(X.VENTA, 0) AS "ventas_totales_{last_year}",
                ISNULL(aut.VENTA, 0) - ISNULL(Z.VENTA, 0) AS "ventas_{actual_year}_sin_cremero_OXXO",
                ISNULL(U.VENTA, 0) AS "ventas_{actual_year}_cremero_OXXO",
                ISNULL(aut.VENTA, 0) AS "ventas_totales_{actual_year}",
                ISNULL(aut.VENTA / @Dias, 0) AS "venta_por_dia",
                ISNULL(aut.VENTA / @Dias * @DiasTotales, 0) AS "proyeccion",
                ISNULL(((aut.VENTA / ISNULL(x.VENTA, aut.VENTA / 2)) - 1) * 100, 0) AS "porcentaje_crecimiento_o_decrecimiento"
                FROM (
                    SELECT 
                        DBKL2019.CADENA AS CADENA,
                        ISNULL(DBKL2019.VENTA, 0) AS VENTA,
                        DBKL2019.grupo AS grupo,
                        DBKL2019.seccion AS seccion
                    FROM (
                        SELECT 
                            KDUD.C66 AS CADENA,
                            SUM(KDIJ.C14) AS VENTA,
                            CASE 
                                WHEN KDUD.C66 IN ('GAER', 'GIHG', 'GTIHO', 'GVIN', 'GLHS', 'GCALY', 'GCAFF', 'CAFFENIO', 'GHHIL', 'GFRU', 'GHCE01', 'GHPR01', 'GPAL', 'BOS01', 'GDIE', 'GPOS01', 'GSHE', 'VM01', 'GPS', 'GPANB', 'GACCO', 'GACOR') 
                                    THEN 'KAM1 - FOODSERVICE'
                                WHEN KDUD.C66 IN ('GSIX', 'GNGRI', 'GQUA', 'GTH01', 'GDEN', 'CAFFENIO', 'GCMR01', 'GHNH01', 'GAREA', 'GCM', 'GHKR', 'GHCR01', 'GLVA','GPS01') 
                                    THEN 'KAM2 - FOODSERVICE'
                                WHEN KDUD.C66 IN ('GLPIZ') 
                                    THEN 'KAM2 - SUCURSALES'
                                WHEN KDUD.C66 IN ('GIHOP', 'GALS01', 'GLIV', 'MACD', 'GOAG', 'GALB', 'GAL01', 'GAL02', 'GAL03', 'GAL04') 
                                    THEN 'KAM3 - FOODSERVICE'
                                WHEN KDUD.C66 IN ('GTO01', 'GBIM', 'GGOM01', 'GSG', 'GSEV01', 'GOXO01', 'GRCOS', 'GPACI', 'GPRIS', 'GHOTS', 'GPES01', 'GCALL') 
                                    THEN 'KAM4 - FOODSERVICE'
                                ELSE 'KAM indefinido'
                            END AS grupo,
                            CASE 
                                WHEN KDUD.C66 IN (
                                    'GFRU', 'GHCE01', 'GHPR01', 'GPOS01', 'GCAFF',
                                    'GSHE', 'GPAL', 'GAER', 'GTIHO', 'GVIN', 'GPANB',
                                    'GDIE', 'BOS01', 'GLHS', 'GCALY', 'VM01', 'GIHG',
                                    'GPS', 'GACCO', 'GACOR'
                                ) 
                                    THEN 'KAM1'
                                WHEN KDUD.C66 IN (
                                    'GHHIL', 'GNGRI', 'GHNH01',
                                    'GSIX', 'GAREA', 'GDEN',
                                    'GLPIZ', 'GCM', 'GCMR01',
                                    'GHCR01', 'GHKR', 'GLVA',
                                    'GTH01', 'GQUA'
                                ) 
                                    THEN 'KAM2'
                                WHEN KDUD.C66 IN ('GIHOP', 'GALS01', 'GLIV', 'MACD', 'GOAG', 'GALB') 
                                    THEN 'KAM3'
                                WHEN KDUD.C66 IN (
                                    'GTO01', 'GBIM', 'GGOM01', 'GSG', 'GSEV01', 
                                    'GOXO01', 'GRCOS', 'GPACI', 'GPRIS', 'GHOTS', 
                                    'GPES01', 'GCALL'
                                ) 
                                    THEN 'KAM4'
                                ELSE 'KAM indefinido'
                            END AS seccion
                        FROM KDIJ
                        INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                        INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                        WHERE 
                            KDII.C1 >= @producto_inicial 
                            AND KDII.C1 <= @producto_final
                            AND KDIJ.C10 >= @fecha_inicial
                            AND KDIJ.C10 <= @fecha_final
                            {filtro_sucursal}
                            AND KDUD.C66 IN (
                                'GCMR01', 'GFRU', 'GHCE01', 'GHNH01', 'GHPR01', 'GPAL', 
                                'GTH01', 'GAER', 'GTIHO', 'GVIN', 'GQUA', 'GNGRI', 'GDEN', 
                                'GDIE', 'GHCR01', 'GAREA', 'GHKR', 'BOS01', 'GCM', 'GLVA', 
                                'GALS01', 'GHHIL', 'GLIV', 'GPOS01', 'GSG', 'GSHE', 'GTO01', 
                                'GRCOS', 'GALB', 'GGOM01', 'MACD', 'GOXO01', 'GSEV01', 'GSIX', 
                                'GBIM', 'GPACI', 'GOAG', 'GIHOP', 'GLPIZ', 'GHOTS', 'GCALL', 
                                'GLHS', 'GCALY', 'GPRIS', 'GPES01', 'GCAFF', 'CAFFENIO', 
                                'GIHG', 'GPS', 'GPANB', 'GACCO', 'GACOR','GPS01', 
                                'GAL01', 'GAL02', 'GAL03', 'GAL04'
                            )
                            AND KDIJ.C16 NOT IN (
                                '902', '903', '904', '905', '906', '907', '908', 
                                '909', '910', '911', '912', '913', '914', '915', 
                                '916', '917', '918', '919', '920', '921', '922', 
                                '923', '924'
                            )
                            AND KDIJ.C4 = 'U'
                            AND KDIJ.C5 = 'D'
                            AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                            AND KDIJ.C7 IN (
                                '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', 
                                '22', '25', '26', '71', '72', '73', '74', '75', '76', 
                                '77', '78', '79', '80', '86', '87', '88', '96', '97'
                            )
                        GROUP BY KDUD.C66
                    ) AS DBKL2019
                ) aut
                LEFT JOIN (
                    SELECT 
                        KDUD.C66 AS CADENA,
                        SUM(KDIJ.C14) AS VENTA
                    FROM KDIJ
                    INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                    INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                    WHERE 
                        KDII.C1 >= @producto_inicial
                        AND KDII.C1 <= @producto_final
                        AND KDIJ.C10 >= @fecha_inicial_year_anterior
                        AND KDIJ.C10 <= @fecha_final_year_anterior
                        {filtro_sucursal}
                        AND KDUD.C66 IN (
                            'GCMR01', 'GFRU', 'GHCE01', 'GHNH01', 'GHPR01', 'GPAL', 
                            'GTH01', 'GAER', 'GTIHO', 'GVIN', 'GQUA', 'GNGRI', 'GDEN', 
                            'GDIE', 'GHCR01', 'GAREA', 'GHKR', 'BOS01', 'GCM', 'GLVA', 
                            'GALS01', 'GHHIL', 'GLIV', 'GPOS01', 'GSG', 'GSHE', 'GTO01', 
                            'GRCOS', 'GALB', 'GGOM01', 'MACD', 'GOXO01', 'GSEV01', 'GSIX', 
                            'GBIM', 'GPACI', 'GOAG', 'GIHOP', 'GLPIZ', 'GHOTS', 'GCALL', 
                            'GLHS', 'GCALY', 'GPRIS', 'GPES01', 'GCAFF', 'CAFFENIO', 
                            'GIHG', 'GPS', 'GPANB', 'GACCO', 'GACOR','GPS01',
                            'GAL01', 'GAL02', 'GAL03', 'GAL04'
                        )
                        AND KDIJ.C16 NOT IN (
                            '902', '903', '904', '905', '906', '907', '908', 
                            '909', '910', '911', '912', '913', '914', '915', 
                            '916', '917', '918', '919', '920', '921', '922', 
                            '923', '924'
                        )
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                        AND KDIJ.C7 IN (
                            '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', 
                            '22', '25', '26', '71', '72', '73', '74', '75', '76', 
                            '77', '78', '79', '80', '86', '87', '88', '96', '97'
                        )
                    GROUP BY KDUD.C66 
                ) X ON aut.CADENA = X.CADENA
                LEFT JOIN (
                    SELECT 
                        DBKL2019.GrupoID AS GrupoID,
                        DBKL2019.DESCRIPCION AS DESCRIPCION
                    FROM (
                        SELECT
                            KDCORPO.C1 AS GrupoID,	
                            KDCORPO.C2 AS DESCRIPCION
                        FROM KDCORPO
                    ) AS DBKL2019 
                ) Y ON aut.CADENA = Y.GrupoID
                LEFT JOIN (
                    SELECT 
                        KDUD.C66 AS CADENA,
                        SUM(KDIJ.C14) AS VENTA 
                    FROM KDIJ
                    INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                    INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                    WHERE 
                        KDII.C1 >= @producto_inicial
                        AND KDII.C1 <= @producto_final
                        AND KDIJ.C10 >= @fecha_inicial_year_anterior
                        AND KDIJ.C10 <= @fecha_final_year_anterior
                        {filtro_sucursal}
                        AND KDIJ.C3 = '0559'
                        AND KDIJ.C16 NOT IN (
                            '902', '903', '904', '905', '906', '907', '908', 
                            '909', '910', '911', '912', '913', '914', '915', 
                            '916', '917', '918', '919', '920', '921', '922', 
                            '923', '924'
                        )
                        AND KDIJ.C4 = 'U'
                        AND KDIJ.C5 = 'D'
                        AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                        AND KDIJ.C7 IN (
                            '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', 
                            '22', '25', '26', '71', '72', '73', '74', '75', '76', 
                            '77', '78', '79', '80', '86', '87', '88', '96', '97'
                        )
                    GROUP BY KDUD.C66 
                ) W ON aut.CADENA = W.CADENA
                LEFT JOIN (
                    SELECT 
                        DBKL2019.CADENA AS CADENA,
                        ISNULL(DBKL2019.VENTA, 0) AS VENTA
                    FROM (
                        SELECT 
                            KDUD.C66 AS CADENA,
                            SUM(KDIJ.C14) AS VENTA 
                        FROM KDIJ
                        INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                        INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                        INNER JOIN KDCORPO ON KDUD.C66 = KDCORPO.C1
                        WHERE 
                            KDII.C1 >= @producto_inicial
                            AND KDII.C1 <= @producto_final
                            AND KDIJ.C10 >= @fecha_inicial
                            AND KDIJ.C10 <= @fecha_final
                            {filtro_sucursal}
                            AND KDIJ.C3 = '0559'
                            AND KDIJ.C16 NOT IN (
                                '902', '903', '904', '905', '906', '907', '908', 
                                '909', '910', '911', '912', '913', '914', '915', 
                                '916', '917', '918', '919', '920', '921', '922', 
                                '923', '924'
                            )
                            AND KDIJ.C4 = 'U'
                            AND KDIJ.C5 = 'D'
                            AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45')
                            AND KDIJ.C7 IN (
                                '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', 
                                '22', '25', '26', '71', '72', '73', '74', '75', '76', 
                                '77', '78', '79', '80', '86', '87', '88', '96', '97'
                            )
                        GROUP BY KDUD.C66 
                    ) AS DBKL2019 
                ) Z ON aut.CADENA = Z.CADENA
                LEFT JOIN (
                    SELECT	
                        KDUD.C66 AS CADENA, 
                        SUM(KDIJ.C14) AS VENTA 
                    FROM KDIJ 
                    INNER JOIN KDII ON KDIJ.C3 = KDII.C1 
                    INNER JOIN KDIF ON KDII.C5 = KDIF.C1 
                    INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2 
                    WHERE 
                        KDII.C1 >= @producto_inicial
                        AND KDII.C1 <= @producto_final
                        AND KDIJ.C10 >= @fecha_inicial_year_anterior
                        AND KDIJ.C10 <= @fecha_final_year_anterior
                        {filtro_sucursal} 
                        AND KDII.C1 = '0559'
                        AND KDIJ.C16 NOT IN (
                            '902', '903', '904', '905', '906', '907', '908', 
                            '909', '910', '911', '912', '913', '914', '915', 
                            '916', '917', '918', '919', '920', '921', '922', 
                            '923', '924'
                        )
                        AND KDIJ.C4 = 'U' 
                        AND KDIJ.C5 = 'D' 
                        AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45') 
                        AND KDIJ.C7 IN (
                            '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', 
                            '22', '25', '26', '71', '72', '73', '74', '75', '76', 
                            '77', '78', '79', '80', '81', '82', '86', '87', '88', 
                            '94', '96', '97'
                        ) 
                    GROUP BY KDUD.C66 
                ) V ON aut.CADENA = V.CADENA
                LEFT JOIN (
                    SELECT 
                        DBKL2019.CADENA AS CADENA,
                        ISNULL(DBKL2019.VENTA, 0) AS VENTA
                    FROM (
                        SELECT	
                            KDUD.C66 AS CADENA, 
                            SUM(KDIJ.C14) AS VENTA 
                        FROM KDIJ 
                        INNER JOIN KDII ON KDIJ.C3 = KDII.C1 
                        INNER JOIN KDIF ON KDII.C5 = KDIF.C1 
                        INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2 
                        WHERE 
                            KDII.C1 >= @producto_inicial 
                            AND KDII.C1 <= @producto_final
                            AND KDIJ.C10 >= @fecha_inicial
                            AND KDIJ.C10 <= @fecha_final
                            {filtro_sucursal}
                            AND KDII.C1 = '0559'
                            AND KDIJ.C16 NOT IN (
                                '902', '903', '904', '905', '906', '907', '908', 
                                '909', '910', '911', '912', '913', '914', '915', 
                                '916', '917', '918', '919', '920', '921', '922', 
                                '923', '924'
                            )
                            AND KDIJ.C4 = 'U' 
                            AND KDIJ.C5 = 'D' 
                            AND (KDIJ.C6 = '5' OR KDIJ.C6 = '45') 
                            AND KDIJ.C7 IN (
                                '1', '2', '3', '4', '5', '6', '18', '19', '20', '21', 
                                '22', '25', '26', '71', '72', '73', '74', '75', '76', 
                                '77', '78', '79', '80', '81', '82', '86', '87', '88', 
                                '94', '96', '97'
                            ) 
                        GROUP BY KDUD.C66
                    ) AS DBKL2019 
                ) U ON U.CADENA = aut.CADENA 
            ORDER BY aut.CADENA;
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
