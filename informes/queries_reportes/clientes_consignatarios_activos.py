# Description: Consulta de clientes y consignatarios activos
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaConsignatariosClientesActivos(fecha_inicial, fecha_final):
    print(f"Consulta de clientes y consignatarios activos desde {fecha_inicial} hasta {fecha_final}")
    
    with connection.cursor() as cursor:
        query = """
            SELECT 	
                ZONA 										AS 'zona',
                SUCURSAL 									AS 'sucursal',
                ISNULL(ENE_Cl,0) 							AS 'Enero_Cliente',
                ISNULL(ENE_Co,0) 							AS 'Enero_Consignatario',
                ISNULL(FEB_Cl,0) 							AS 'Febrero_Cliente',
                ISNULL(FEB_Co,0) 							AS 'Febrero_Consignatario',
                ISNULL(MAR_Cl,0) 							AS 'Marzo_Cliente',
                ISNULL(MAR_Co,0) 							AS 'Marzo_Consignatario',
                ISNULL(ABR_Cl,0) 							AS 'Abril_Cliente',
                ISNULL(ABR_Co,0) 							AS 'Abril_Consignatario',
                ISNULL(MAY_Cl,0) 							AS 'Mayo_Cliente',
                ISNULL(MAY_Co,0) 							AS 'Mayo_Consignatario',
                ISNULL(JUN_Cl,0) 							AS 'Junio_Cliente',
                ISNULL(JUN_Co,0) 							AS 'Junio_Consignatario',
                ISNULL(JUL_Cl,0) 							AS 'Julio_Cliente',
                ISNULL(JUL_Co,0) 							AS 'Julio_Consignatario',
                ISNULL(AGO_Cl,0) 							AS 'Agosto_Cliente',
                ISNULL(AGO_Co,0) 							AS 'Agosto_Consignatario',
                ISNULL(SEP_Cl,0) 							AS 'Septiembre_Cliente',
                ISNULL(SEP_Co,0) 							AS 'Septiembre_Consignatario',
                ISNULL(OCT_Cl,0) 							AS 'Octubre_Cliente',
                ISNULL(OCT_Co,0) 							AS 'Octubre_Consignatario',
                ISNULL(NOV_Cl,0) 							AS 'Noviembre_Cliente',
                ISNULL(NOV_Co,0) 							AS 'Noviembre_Consignatario',
                ISNULL(DIC_Cl,0) 							AS 'Diciembre_Cliente',
                ISNULL(DIC_Co,0) 							AS 'Diciembre_Consignatario',
                
                (ISNULL(ENE_Cl,0)+ISNULL(FEB_Cl,0)+ISNULL(MAR_Cl,0)+ISNULL(ABR_Cl,0)+ISNULL(MAY_Cl,0)+ISNULL(JUN_Cl,0)+ISNULL(JUL_Cl,0)+ISNULL(AGO_Cl,0)+ISNULL(SEP_Cl,0)+ISNULL(OCT_Cl,0)+ISNULL(NOV_Cl,0)+ISNULL(DIC_Cl,0)) /
                (IIF(ENE_Cl is null,0,1)+IIF(FEB_Cl is null,0,1)+IIF(MAR_Cl is null,0,1)+IIF(ABR_Cl is null,0,1)+IIF(MAY_Cl is null,0,1)+IIF(JUN_Cl is null,0,1)+IIF(JUL_Cl is null,0,1)+IIF(AGO_Cl is null,0,1)+IIF(SEP_Cl is null,0,1)+IIF(OCT_Cl is null,0,1)+IIF(NOV_Cl is null,0,1)+IIF(DIC_Cl is null,0,1))	AS 'Promedio_Cliente',
                
                (ISNULL(ENE_Co,0)+ISNULL(FEB_Co,0)+ISNULL(MAR_Co,0)+ISNULL(ABR_Co,0)+ISNULL(MAY_Co,0)+ISNULL(JUN_Co,0)+ISNULL(JUL_Co,0)+ISNULL(AGO_Co,0)+ISNULL(SEP_Co,0)+ISNULL(OCT_Co,0)+ISNULL(NOV_Co,0)+ISNULL(DIC_Co,0)) /
                (IIF(ENE_Co is null,0,1)+IIF(FEB_Co is null,0,1)+IIF(MAR_Co is null,0,1)+IIF(ABR_Co is null,0,1)+IIF(MAY_Co is null,0,1)+IIF(JUN_Co is null,0,1)+IIF(JUL_Co is null,0,1)+IIF(AGO_Co is null,0,1)+IIF(SEP_Co is null,0,1)+IIF(OCT_Co is null,0,1)+IIF(NOV_Co is null,0,1)+IIF(DIC_Co is null,0,1))AS 'Promedio_Consignatario'
            FROM(
                SELECT DISTINCT
                    
                    CASE	
                            WHEN A.ZONA = '02'						THEN '1.-Vallejo'
                            WHEN A.ZONA IN ('17','04','15','16')	THEN '2.-Norte'
                            WHEN A.ZONA IN ('05','10','19','08')	THEN '3.-Centro'
                            WHEN A.ZONA IN ('09','14','03','12','20')	THEN '4.-Pacifico'
                            WHEN A.ZONA IN ('13','11','18','07')	THEN '5.-Sureste'
                            ELSE 'Sin zona'
                    END																			AS 'ZONA',
                    CASE 	WHEN A.SUC <> '02' 						THEN A.SUC +'&nbsp;-&nbsp;'+A.SUCURSAL
                            ELSE 
                                CASE	WHEN A.SubSUCURSAL = '1' THEN '1&nbsp;-&nbsp;Autoservicio'
                                        WHEN A.SubSUCURSAL = '2' THEN '2&nbsp;-&nbsp;Norte'
                                        WHEN A.SubSUCURSAL = '3' THEN '3&nbsp;-&nbsp;Sur'
                                        WHEN A.SubSUCURSAL = '4' THEN '4&nbsp;-&nbsp;Vent. Especiales'
                                        WHEN A.SubSUCURSAL = '5' THEN '5&nbsp;-&nbsp;Cadenas'
                                        ELSE 'sin asignar a Vallejo'
                                END			  						 
                    END																			AS 'SUCURSAL', 
                    A.MES, 
                    COUNT(A.BANDERA) AS BANDERA
                FROM (
                    SELECT DISTINCT
                        KDM1.C1 															AS 'ZONA', 
                        LTRIM(RTRIM(KDM1.C1)) AS SUC,
                        LTRIM(RTRIM(KDMS.C2)) AS SUCURSAL,
                        ISNULL(KDUV.C22,'') AS   SubSUCURSAL,
                        KDM1.C10														AS 'ID_CLIENTE',
                        CASE	WHEN FORMAT(KDM1.C9, 'MM')= '01' THEN 'ENE_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '02' THEN 'FEB_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '03' THEN 'MAR_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '04' THEN 'ABR_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '05' THEN 'MAY_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '06' THEN 'JUN_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '07' THEN 'JUL_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '08' THEN 'AGO_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '09' THEN 'SEP_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '10' THEN 'OCT_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '11' THEN 'NOV_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '12' THEN 'DIC_Cl'
                                ELSE 'mes sin definir'
                        END																			AS 'MES',
                        1  																		AS 'BANDERA'
                    FROM			KDM1
                        INNER JOIN KDUV		ON KDUV.C2 = KDM1.C12
                        INNER JOIN KDMS		ON KDMS.C1 = KDM1.C1
                        INNER JOIN KDUCON		ON KDUCON.C1 =  KDM1.C10 AND KDUCON.C2 =  KDM1.C70
                    WHERE 
                            KDM1.C9 >= CONVERT(DATETIME,%s, 102)
                        AND KDM1.C9 <= CONVERT(DATETIME,%s, 102)
                        AND KDM1.C10 <> ''
                        AND KDM1.C10 IS NOT NULL
                        AND KDM1.C2 = 'U'
                        AND KDM1.C3 = 'D'
                        AND KDM1.C4 IN ('5')
                        AND KDM1.C5 IN ( '18','19','20','21','22','23','24','25','26')
                        AND KDM1.C12 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    GROUP BY KDM1.C1, KDMS.C2, KDUV.C22, KDM1.C9, KDM1.C10
                    UNION /**********************************************************/
                    SELECT DISTINCT
                        KDM1.C1 															AS 'ZONA', 
                        LTRIM(RTRIM(KDM1.C1)) AS SUC,
                        LTRIM(RTRIM(KDMS.C2)) AS SUCURSAL,
                        KDUV.C22 AS   SubSUCURSAL,
                        KDM1.C10	+KDM1.C70														AS 'ID_CONSIGNATARIO', 
                        CASE	WHEN FORMAT(KDM1.C9, 'MM')= '01' THEN 'ENE_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '02' THEN 'FEB_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '03' THEN 'MAR_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '04' THEN 'ABR_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '05' THEN 'MAY_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '06' THEN 'JUN_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '07' THEN 'JUL_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '08' THEN 'AGO_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '09' THEN 'SEP_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '10' THEN 'OCT_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '11' THEN 'NOV_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '12' THEN 'DIC_Co'
                                ELSE 'mes sin definir'
                        END																			AS 'MES',
                        1  																			AS 'BANDERA'
                    FROM			KDM1
                        INNER JOIN KDUV		ON KDUV.C2 = KDM1.C12
                        INNER JOIN KDMS		ON KDMS.C1 = KDM1.C1
                        INNER JOIN KDUCON	ON KDUCON.C1 =  KDM1.C10 AND KDUCON.C2 =  KDM1.C70
                    WHERE 
                            KDM1.C9 >= CONVERT(DATETIME,%s, 102)
                        AND KDM1.C9 <= CONVERT(DATETIME,%s, 102)
                        AND KDM1.C10 <> ''
                        AND KDM1.C10 IS NOT NULL
                        AND KDM1.C2 = 'U'
                        AND KDM1.C3 = 'D'
                        AND KDM1.C4 IN ('5')
                        AND KDM1.C5 IN ( '18','19','20','21','22','23','24','25','26')
                        AND KDM1.C12 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    GROUP BY KDM1.C1, KDMS.C2, KDUV.C22, KDM1.C9, KDM1.C10, KDM1.C70
                    UNION /**********************************************************/
                        SELECT DISTINCT
                        KDM1.C1 															AS 'ZONA', 
                        LTRIM(RTRIM(KDM1.C1)) AS SUC,
                        LTRIM(RTRIM(KDMS.C2)) AS SUCURSAL,
                        KDUV.C22 AS SubSUCURSAL,
                        KDM1.C10															AS 'ID_CLIENTE',
                        CASE	WHEN FORMAT(KDM1.C9, 'MM')= '01' THEN 'ENE_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '02' THEN 'FEB_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '03' THEN 'MAR_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '04' THEN 'ABR_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '05' THEN 'MAY_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '06' THEN 'JUN_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '07' THEN 'JUL_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '08' THEN 'AGO_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '09' THEN 'SEP_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '10' THEN 'OCT_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '11' THEN 'NOV_Cl'
                                WHEN FORMAT(KDM1.C9, 'MM')= '12' THEN 'DIC_Cl'
                                ELSE 'mes sin definir'
                        END																			AS 'MES',
                        1  																		AS 'BANDERA'
                    FROM			KDM1
                        INNER JOIN KDUV		ON KDUV.C2 = KDM1.C12
                        INNER JOIN KDMS		ON KDMS.C1 = KDM1.C1
                        INNER JOIN KDVDIREMB		ON KDVDIREMB.C1 =  KDM1.C10 AND KDVDIREMB.C2 =  KDM1.C181
                    WHERE 
                            KDM1.C9 >= CONVERT(DATETIME, %s, 102)
                        AND KDM1.C9 <= CONVERT(DATETIME, %s, 102)
                        AND KDM1.C10 <> ''
                        AND KDM1.C10 IS NOT NULL
                        AND KDM1.C2 = 'U'
                        AND KDM1.C3 = 'D'
                        AND KDM1.C4 IN ('5')
                        AND KDM1.C5 IN ( '18','19','20','21','22','23','24','25','26')
                        AND KDM1.C12 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    GROUP BY KDM1.C1, KDMS.C2, KDUV.C22, KDM1.C9, KDM1.C10
                    UNION /**********************************************************/
                    SELECT DISTINCT
                        KDM1.C1 															AS 'ZONA', 
                        LTRIM(RTRIM(KDM1.C1)) AS SUC,
                        LTRIM(RTRIM(KDMS.C2)) AS SUCURSAL,
                        KDUV.C22 AS SubSUCURSAL,
                        KDM1.C10	+KDM1.C181												AS 'ID_CONSIGNATARIO', 
                        CASE	WHEN FORMAT(KDM1.C9, 'MM')= '01' THEN 'ENE_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '02' THEN 'FEB_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '03' THEN 'MAR_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '04' THEN 'ABR_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '05' THEN 'MAY_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '06' THEN 'JUN_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '07' THEN 'JUL_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '08' THEN 'AGO_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '09' THEN 'SEP_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '10' THEN 'OCT_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '11' THEN 'NOV_Co'
                                WHEN FORMAT(KDM1.C9, 'MM')= '12' THEN 'DIC_Co'
                                ELSE 'mes sin definir'
                        END																			AS 'MES',
                        1  																			AS 'BANDERA'
                    FROM			KDM1
                        INNER JOIN KDUV		ON KDUV.C2 = KDM1.C12
                        INNER JOIN KDMS		ON KDMS.C1 = KDM1.C1
                        INNER JOIN KDVDIREMB	ON KDVDIREMB.C1 =  KDM1.C10 AND KDVDIREMB.C2 =  KDM1.C181
                    WHERE 
                            KDM1.C9 >= CONVERT(DATETIME, %s, 102)
                        AND KDM1.C9 <= CONVERT(DATETIME, %s, 102)
                        AND KDM1.C10 <> ''
                        AND KDM1.C10 IS NOT NULL
                        AND KDM1.C2 = 'U'
                        AND KDM1.C3 = 'D'
                        AND KDM1.C4 IN ('5')
                        AND KDM1.C5 IN ( '18','19','20','21','22','23','24','25','26')
                        AND KDM1.C12 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    GROUP BY KDM1.C1, KDMS.C2, KDUV.C22, KDM1.C9, KDM1.C10, KDM1.C181
                ) AS A  
            GROUP BY  A.ZONA, A.SUCURSAL, A.MES, A.SUC, A.SubSUCURSAL
            ) AS AA  
            PIVOT (
                SUM(BANDERA) 
                FOR [MES] 
                IN ([ENE_Cl],[ENE_Co],[FEB_Cl],[FEB_Co],[MAR_Cl],[MAR_Co],[ABR_Cl],[ABR_Co],[MAY_Cl],[MAY_Co],[JUN_Cl],[JUN_Co],[JUL_Cl],[JUL_Co],[AGO_Cl],[AGO_Co],[SEP_Cl],[SEP_Co],[OCT_Cl],[OCT_Co],[NOV_Cl],[NOV_Co],[DIC_Cl],[DIC_Co],[PROMEDIO_Cl],[PROMEDIO_Co]) 
            ) AS PivotTable
            order by 1,2
        """

        params = [
                    fecha_inicial, fecha_final,
                    fecha_inicial, fecha_final,
                    fecha_inicial, fecha_final,
                    fecha_inicial, fecha_final
                ]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        
    return result