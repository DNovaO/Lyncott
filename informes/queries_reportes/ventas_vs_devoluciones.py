#Description: Consulta de ventas vs devoluciones
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *

def consultaVentasVsDevoluciones(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, grupoCorporativo_inicial, grupoCorporativo_final):


    # Calcula las fechas del año anterior
    fecha_inicial_year_anterior = fecha_inicial.replace(year=fecha_inicial.year - 1)
    fecha_final_year_anterior = fecha_final.replace(year=fecha_final.year - 1)
    
    actual_year = str(fecha_inicial.year)
    last_year = str(fecha_inicial.year - 1)

    if sucursal_inicial == 'ALL' and sucursal_final == 'ALL':
        filtro_sucursal = f"KDM1.C1 >= '02' AND KDM1.C1 <= '20'"
    elif sucursal_inicial == 'ALL':
        filtro_sucursal = f"KDM1.C1 >= '02' AND KDM1.C1 <= '20'"
    elif sucursal_final == 'ALL':
        filtro_sucursal = f"KDM1.C1 >= '02' AND KDM1.C1 <= '20'"
    else:
        filtro_sucursal = f"KDM1.C1 >= {sucursal_inicial} AND KDM1.C1 <= {sucursal_final}"

    if grupoCorporativo_inicial == 'ALL' and grupoCorporativo_final == 'ALL':
        filtro_grupoCorporativo = "AND KDCORPO.C1 >= '7 ELEV' AND KDCORPO.C1 <= 'POSAD'"
    elif grupoCorporativo_inicial == 'ALL':
        filtro_grupoCorporativo = "AND KDCORPO.C1 >= '7 ELEV' AND KDCORPO.C1 <= 'POSAD'"
    elif grupoCorporativo_final == 'ALL':
        filtro_grupoCorporativo = "AND KDCORPO.C1 >= '7 ELEV' AND KDCORPO.C1 <= 'POSAD'"
    else:
        filtro_grupoCorporativo = f"AND KDCORPO.C1 >= '{grupoCorporativo_inicial}' AND KDCORPO.C1 <= '{grupoCorporativo_final}'"
    
    with connection.cursor() as cursor:
        query = f"""
            DECLARE 
                @fecha_inicial VARCHAR(20) = %s,
                @fecha_final VARCHAR(20) = %s,
                @fecha_inicial_year_anterior VARCHAR(20) = %s,
                @fecha_final_year_anterior VARCHAR(20) = %s,
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s,
                @grupoCorporativo_inicial VARCHAR(20) = %s,
                @grupoCorporativo_final VARCHAR(20) = %s;
            
            SELECT 
                LTRIM(RTRIM(ISNULL(A.ID_GrupoCorporativo, ISNULL(B.ID_GrupoCorporativo, C.ID_GrupoCorporativo)))) AS 'id_grupo_corporativo',
                LTRIM(RTRIM(ISNULL(A.GrupoCorporativo, ISNULL(B.GrupoCorporativo, C.GrupoCorporativo)))) AS 'grupo_corporativo',
                LTRIM(RTRIM(ISNULL(A.ID_Cliente, ISNULL(B.ID_Cliente, C.ID_Cliente)))) AS 'id_cliente',
                LTRIM(RTRIM(ISNULL(A.ID_Consignatario, ISNULL(B.ID_Consignatario, C.ID_Consignatario)))) AS 'id_consignatario',
                LTRIM(RTRIM(ISNULL(A.Consignatario, ISNULL(B.Consignatario, C.Consignatario)))) AS 'consignatario',
                ISNULL(C.VENTAS, 0) AS 'venta_anterior_{last_year}',
                ISNULL((C.VENTAS * 100 / CC.VENTAS), 0) AS 'porcentaje_venta_anterior_{last_year}',
                ISNULL(A.VENTAS, 0) AS 'venta_actual_{actual_year}',
                ISNULL((A.VENTAS * 100 / AA.VENTAS), 0) AS 'porcentaje_venta_actual_{actual_year}',
                ISNULL(B.DEVOLUCIONES, 0) AS 'devolucion_{actual_year}_en_pesos',
                ISNULL((B.DEVOLUCIONES * 100 / BB.DEVOLUCIONES), 0) AS 'porcentaje_devolucion_{actual_year}',
                ISNULL(A.VENTAS, 0) - ISNULL(B.DEVOLUCIONES, 0) AS 'diferencia_{actual_year}_en_pesos'
            FROM (
                /* A */
                SELECT
                    DBL2019.SUCURSAL AS SUCURSAL,
                    DBL2019.ID_GrupoCorporativo AS ID_GrupoCorporativo,
                    DBL2019.GrupoCorporativo AS GrupoCorporativo,
                    DBL2019.ID_Cliente AS ID_Cliente,
                    DBL2019.ID_Consignatario AS ID_Consignatario,
                    DBL2019.Consignatario AS Consignatario,
                    ISNULL(DBL2019.VENTAS, 0) AS VENTAS,
                    'AA' AS AA,
                    'BB' AS BB,
                    'CC' AS CC
                FROM (
                    SELECT  
                        KDM1.C1 AS SUCURSAL,
                        KDCORPO.C1 AS ID_GrupoCorporativo,
                        KDCORPO.C2 AS GrupoCorporativo,
                        KDM1.C10 AS ID_Cliente,
                        KDM1.C181 AS ID_Consignatario,
                        KDVDIREMB.C3 AS Consignatario,
                        SUM(KDM1.C16) - SUM(KDM1.C15) AS VENTAS
                    FROM KDM1
                    INNER JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 AND KDM1.C181 = KDVDIREMB.C2
                    INNER JOIN KDUD ON KDM1.C10 = KDUD.C2
                    INNER JOIN KDCORPO ON KDUD.C66 = KDCORPO.C1
                    WHERE
                        {filtro_sucursal}
                        AND KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial, 102)
                        AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final, 102)
                        {filtro_grupoCorporativo}
                        AND KDM1.C2 = 'U' AND KDM1.C3 = 'D'
                        AND KDM1.C4 IN ('5', '45')
                        AND KDM1.C5 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26')
                        AND KDM1.C12 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    GROUP BY KDM1.C1, KDCORPO.C1, KDCORPO.C2, KDM1.C10, KDM1.C181, KDVDIREMB.C3
                ) AS DBL2019
                /* END A */
            ) AS A
            FULL JOIN (
                /* B */
                SELECT 
                    DBL2019.SUCURSAL AS SUCURSAL,
                    DBL2019.ID_GrupoCorporativo AS ID_GrupoCorporativo,
                    DBL2019.GrupoCorporativo AS GrupoCorporativo,
                    DBL2019.ID_Cliente AS ID_Cliente,
                    DBL2019.ID_Consignatario AS ID_Consignatario,
                    DBL2019.Consignatario AS Consignatario,
                    ISNULL(DBL2019.DEVOLUCIONES, 0) AS DEVOLUCIONES,
                    'BB' AS BB
                FROM (
                    SELECT  
                        KDM1.C1 AS SUCURSAL,
                        KDCORPO.C1 AS ID_GrupoCorporativo,
                        KDCORPO.C2 AS GrupoCorporativo,
                        KDM1.C10 AS ID_Cliente,
                        KDM1.C181 AS ID_Consignatario,
                        KDVDIREMB.C3 AS Consignatario,
                        SUM(KDM1.C16) - SUM(KDM1.C15) AS DEVOLUCIONES
                    FROM KDM1
                    INNER JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 AND KDM1.C181 = KDVDIREMB.C2
                    INNER JOIN KDUD ON KDUD.C2 = KDM1.C10
                    INNER JOIN KDCORPO ON KDCORPO.C1 = KDUD.C66
                    WHERE
                        {filtro_sucursal}
                        AND KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial_year_anterior, 102)
                        AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final_year_anterior, 102)
                        {filtro_grupoCorporativo}
                        AND KDM1.C2 = 'N' AND KDM1.C3 = 'D'
                        AND KDM1.C4 = '25' AND KDM1.C5 = '12'
                        AND KDM1.C12 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                    GROUP BY KDM1.C1, KDCORPO.C1, KDCORPO.C2, KDM1.C10, KDM1.C181, KDVDIREMB.C3
                ) AS DBL2019
                /* END B */
            ) AS B ON A.SUCURSAL = B.SUCURSAL AND A.ID_GrupoCorporativo = B.ID_GrupoCorporativo AND A.ID_Cliente = B.ID_Cliente AND A.ID_Consignatario = B.ID_Consignatario
            FULL JOIN (
                /* C */
                SELECT  
                    KDM1.C1 AS SUCURSAL,
                    KDCORPO.C1 AS ID_GrupoCorporativo,
                    KDCORPO.C2 AS GrupoCorporativo,
                    KDM1.C10 AS ID_Cliente,
                    KDM1.C181 AS ID_Consignatario,
                    KDVDIREMB.C3 AS Consignatario,
                    SUM(KDM1.C16) - SUM(KDM1.C15) AS VENTAS,
                    'CC' AS CC
                FROM KDM1
                INNER JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 AND KDM1.C181 = KDVDIREMB.C2
                INNER JOIN KDUD ON KDUD.C2 = KDM1.C10
                INNER JOIN KDCORPO ON KDCORPO.C1 = KDUD.C66
                WHERE
                    {filtro_sucursal}
                    AND KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial_year_anterior, 102)
                    AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final_year_anterior, 102)
                    {filtro_grupoCorporativo}
                    AND KDM1.C2 = 'U' AND KDM1.C3 = 'D'
                    AND KDM1.C4 IN ('5', '45')
                    AND KDM1.C5 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26')
                    AND KDM1.C12 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                GROUP BY KDM1.C1, KDCORPO.C1, KDCORPO.C2, KDM1.C10, KDM1.C181, KDVDIREMB.C3
                /* END C */
            ) AS C ON A.SUCURSAL = C.SUCURSAL AND A.ID_GrupoCorporativo = C.ID_GrupoCorporativo AND A.ID_Cliente = C.ID_Cliente AND A.ID_Consignatario = C.ID_Consignatario
            LEFT JOIN (
                /* AA */
                SELECT 
                    ISNULL(DBL2019.VENTAS, 0) AS VENTAS,
                    'AA' AS AA
                FROM (
                    SELECT  
                        SUM(KDM1.C16) - SUM(KDM1.C15) AS VENTAS,
                        'AA' AS AA
                    FROM KDM1
                    INNER JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 AND KDM1.C181 = KDVDIREMB.C2
                    INNER JOIN KDUD ON KDUD.C2 = KDM1.C10
                    INNER JOIN KDCORPO ON KDCORPO.C1 = KDUD.C66
                    WHERE
                        {filtro_sucursal}
                        AND KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial, 102)
                        AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final, 102)
                        {filtro_grupoCorporativo}
                        AND KDM1.C2 = 'U' AND KDM1.C3 = 'D'
                        AND KDM1.C4 IN ('5', '45')
                        AND KDM1.C5 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26')
                        AND KDM1.C12 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                ) AS DBL2019
                /* END AA */
            ) AS AA ON A.AA = AA.AA
            LEFT JOIN (
                /* BB */
                SELECT 
                    ISNULL(DBL2019.DEVOLUCIONES, 0) AS DEVOLUCIONES,
                    'BB' AS BB
                FROM (
                    SELECT  
                        SUM(KDM1.C16) - SUM(KDM1.C15) AS DEVOLUCIONES,
                        'BB' AS BB
                    FROM KDM1
                    INNER JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 AND KDM1.C181 = KDVDIREMB.C2
                    INNER JOIN KDUD ON KDUD.C2 = KDM1.C10
                    INNER JOIN KDCORPO ON KDCORPO.C1 = KDUD.C66
                    WHERE
                        {filtro_sucursal}
                        AND KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial_year_anterior, 102)
                        AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final_year_anterior, 102)
                        {filtro_grupoCorporativo}
                        AND KDM1.C2 = 'N' AND KDM1.C3 = 'D'
                        AND KDM1.C4 = '25' AND KDM1.C5 = '12'
                        AND KDM1.C12 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                ) AS DBL2019
                /* END BB */
            ) AS BB ON A.BB = BB.BB OR B.BB = BB.BB
            LEFT JOIN (
                /* CC */
                SELECT  
                    SUM(KDM1.C16) - SUM(KDM1.C15) AS VENTAS,
                    'CC' AS CC
                FROM KDM1
                INNER JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 AND KDM1.C181 = KDVDIREMB.C2
                INNER JOIN KDUD ON KDUD.C2 = KDM1.C10
                INNER JOIN KDCORPO ON KDCORPO.C1 = KDUD.C66
                WHERE
                    {filtro_sucursal}
                    AND KDM1.C9 >= CONVERT(DATETIME, @fecha_inicial_year_anterior , 102)
                    AND KDM1.C9 <= CONVERT(DATETIME, @fecha_final_year_anterior, 102)
                    {filtro_grupoCorporativo}
                    AND KDM1.C2 = 'U' AND KDM1.C3 = 'D'
                    AND KDM1.C4 IN ('5', '45')
                    AND KDM1.C5 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', '21', '22', '25', '26')
                    AND KDM1.C12 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                /* END CC */
            ) AS CC ON A.CC = CC.CC OR C.CC = CC.CC
            /**********************************************/
            GROUP BY	A.SUCURSAL, 			B.SUCURSAL,				 C.SUCURSAL,
                        A.ID_GrupoCorporativo, 	B.ID_GrupoCorporativo,	 C.ID_GrupoCorporativo, 
                        A.GrupoCorporativo, 	B.GrupoCorporativo,		 C.GrupoCorporativo, 
                        A.ID_Cliente, 			B.ID_Cliente,			 C.ID_Cliente,
                        A.ID_Consignatario, 	B.ID_Consignatario,		 C.ID_Consignatario,
                        A.Consignatario, 		B.Consignatario,		 C.Consignatario,
                        A.VENTAS, 				B.DEVOLUCIONES,			 C.VENTAS,
                        AA.VENTAS, 				BB.DEVOLUCIONES,		 CC.VENTAS
            ORDER BY id_grupo_corporativo, id_cliente, id_consignatario;
        """

        params = [
            fecha_inicial, fecha_final,
            fecha_inicial_year_anterior, fecha_final_year_anterior,
            sucursal_inicial, sucursal_final,
            grupoCorporativo_inicial, grupoCorporativo_final
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