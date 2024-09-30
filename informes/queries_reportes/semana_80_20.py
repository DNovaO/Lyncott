# Description: Analisis semanal 80/20
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaSemana8020(fecha_inicial, fecha_final, sucursal):
    print(f"Consulta de semana 80/20 desde {fecha_inicial} hasta {fecha_final}, sucursal: {sucursal}")

    with connection.cursor() as cursor:
        query = """
            SELECT 
                ISNULL(A.CODIGO,B.CODIGO)					AS 'clave_producto',
                ISNULL(A.PRODUCTO,B.PRODUCTO)				AS 'producto',
                ISNULL(A.VENDEDOR,B.VENDEDOR)				AS 'vendedor' ,
                ISNULL(A.PIEZAS,0)							AS 'devolucion_buena_piezas',
                CONCAT('$', FORMAT(ISNULL(A.PESOS, 0), 'N2')) AS 'devolucion_buena_pesos',
                ISNULL(B.PIEZAS,0)							AS 'devolucion_mala_piezas',
                CONCAT('$', FORMAT(ISNULL(B.PESOS, 0), 'N2')) AS 'devolucion_mala_pesos',
                B.PESOS/C.PESOS*100	 AS 'porcentaje',
                SUM(B.PESOS / NULLIF(C.PESOS, 0) * 100) OVER (ORDER BY B.PESOS DESC) AS '80/20'
            FROM(
                        SELECT
                            KLDB.CODIGO 									AS CODIGO,
                            KLDB.PRODUCTO 									AS PRODUCTO,
                            ISNULL(KLDB.PIEZAS,0)							AS PIEZAS,
                            ISNULL(KLDB.PESOS,0)							AS PESOS,
                            KLDB.ID_VENDEDOR 								AS ID_VENDEDOR,
                            KLDB.VENDEDOR 									AS VENDEDOR,
                            'CodigoUnion'																AS CodigoUnion
                    
                        FROM(
                                /*DEVOLUCION BUENA*/
                                SELECT   
                                    LTRIM(RTRIM(KDII.C1))														AS CODIGO,
                                    LTRIM(RTRIM(KDII.C2))														AS PRODUCTO,
                                    SUM(KDIJ.C11)																AS PIEZAS,
                                    CASE	 
                                            WHEN KDIJ.C1 IN ('02','03','04','05','08','10','11','12','13','15','16','19')	THEN SUM(KDIJ.C11 * KDII.C14)
                                            WHEN KDIJ.C1 IN ('07','18')												THEN SUM(KDIJ.C11 * KDII.C15)
                                            WHEN KDIJ.C1 IN ('06','09','14')											THEN SUM(KDIJ.C11 * KDII.C16)
                                            WHEN KDIJ.C1 IN ('17')													THEN SUM(KDIJ.C11 * KDII.C17)
                                    END																					AS PESOS,
                                    LTRIM(RTRIM(KDUV.C2))														AS ID_VENDEDOR,
                                    LTRIM(RTRIM(KDUV.C3))	                                                    AS VENDEDOR,
                                    'CodigoUnion'																		AS CodigoUnion
                                FROM KDIJ
                                    INNER JOIN KDUV ON KDUV.C24 = KDIJ.C2 AND KDUV.C1 = KDIJ.C1
                                    INNER JOIN KDMS ON KDMS.C1 = KDIJ.C1
                                    INNER JOIN KDII ON KDII.C1 = KDIJ.C3
                                WHERE	
                                        KDIJ.C1 IN (%s) /*Sucursal*/
                                    AND KDIJ.C10 >= CONVERT(DATETIME,  %s, 102) /*FInicial*/
                                    AND KDIJ.C10 <= CONVERT(DATETIME,  %s, 102) /*FFinal*/
                                    --AND KDIJ.C2   IN ('145','718','143','122','448','624','119','108','171','525','197','58','622','63','170','184','855','112','173','183')
                                    AND KDUV.C2 NOT IN ('101','102','103','104','105','106','107','108','109','110','111','112','113','114','115','116','117','118','119','120','121','122','123','124','125','126','127','128','129','130','131','135','136','139','141','144','145','146','149','152','154','155','156','162','163','164','165','172','174','175','176','177','178','179','188','189','193','201','202','203','204','233','238','293','296','297','298','300','312','314','316','317','318','322','334','335','336','337','338','342','343','344','345','346','347','349','353','366','369','373','391','399','402','403','404','405','406','407','408','409','410','411','412','413','414','415','416','417','418','419','420','421','422','423','424','426','427','428','430','431','432','433','434','436','437','438','439','440','441','442','443','444','445','446','474','496','498','512','513','514','516','517','519','520','521','522','532','535','537','538','540','542','558','561','562','563','564','565','591','592','594','595','596','597','598','599','603','605','607','610','615','616','617','618','619','620','621','623','625','626','627','628','629','631','637','638','639','640','641','642','643','644','645','646','647','648','651','655','656','658','659','660','661','662','663','664','665','666','667','668','669','670','672','675','676','677','680','681','682','688','690','691','694','695','696','697','698','699','700','701','702','703','704','748','749','750','752','753','754','755','756','757','758','771','773','774','775','776','777','778','779','781','783','784','785','786','787','788','789','790','791','792','793','794','795','833','834','835','836','844','845','846','847','851','852','856','857','858','859','862','863','864','865','866','867','868','869','877','887','888','889','890','891','892','894','895','899','902','921','922','923','924','926','927','928','929','930','931','932','933','934','935','936','937','938')
                                    AND KDIJ.C4 = 'N' 
                                    AND KDIJ.C5 = 'D' 
                                    AND KDIJ.C6 IN ('25') 
                                    AND KDIJ.C7 IN ('3') 
                                GROUP BY KDII.C1, KDII.C2, KDUV.C2, KDUV.C3, KDIJ.C1
                        ) AS KLDB 
            ) AS A FULL JOIN (
                        SELECT
                            KLDB.CODIGO 									AS CODIGO,
                            KLDB.PRODUCTO 									AS PRODUCTO,
                            ISNULL(KLDB.PIEZAS,0)							AS PIEZAS,
                            ISNULL(KLDB.PESOS,0)							AS PESOS,
                            KLDB.ID_VENDEDOR 								AS ID_VENDEDOR,
                            KLDB.VENDEDOR 									AS VENDEDOR,
                            'CodigoUnion'																AS CodigoUnion
                        FROM(
                                /*DEVOLUCION MALA*/
                                SELECT   
                                    LTRIM(RTRIM(KDII.C1))														AS CODIGO,
                                    LTRIM(RTRIM(KDII.C2))														AS PRODUCTO,
                                    SUM(KDIJ.C11)																AS PIEZAS,
                                    CASE	 
                                            WHEN KDIJ.C1 IN ('02','03','04','05','08','10','11','12','13','15','16','19')	THEN SUM(KDIJ.C11 * KDII.C14)
                                            WHEN KDIJ.C1 IN ('07','18')												THEN SUM(KDIJ.C11 * KDII.C15)
                                            WHEN KDIJ.C1 IN ('06','09','14')											THEN SUM(KDIJ.C11 * KDII.C16)
                                            WHEN KDIJ.C1 IN ('17')													THEN SUM(KDIJ.C11 * KDII.C17)
                                    END																					AS PESOS,
                                    LTRIM(RTRIM(KDUV.C2))														AS ID_VENDEDOR,
                                    /*LTRIM(RTRIM(KDUV.C2)) + '&nbsp;-&nbsp;'+*/LTRIM(RTRIM(KDUV.C3))	AS VENDEDOR,
                                    'CodigoUnion'																		AS CodigoUnion
                                FROM KDIJ
                                    INNER JOIN KDUV ON KDUV.C24 = KDIJ.C2 AND KDUV.C1 = KDIJ.C1 
                                    INNER JOIN KDMS ON KDMS.C1 = KDIJ.C1 
                                    INNER JOIN KDII ON KDII.C1 = KDIJ.C3
                                WHERE	
                                        KDIJ.C1 IN (%s) /*Sucursal*/
                                    AND KDIJ.C10 >= CONVERT(DATETIME,  %s, 102) /*FInicial*/
                                    AND KDIJ.C10 <= CONVERT(DATETIME,  %s, 102) /*FFinal*/
                                    --AND KDIJ.C2   IN ('145','718','143','122','448','624','119','108','171','525','197','58','622','63','170','184','855','112','173','183')
                                    AND KDUV.C2 NOT IN ('101','102','103','104','105','106','107','108','109','110','111','112','113','114','115','116','117','118','119','120','121','122','123','124','125','126','127','128','129','130','131','135','136','139','141','144','145','146','149','152','154','155','156','162','163','164','165','172','174','175','176','177','178','179','188','189','193','201','202','203','204','233','238','293','296','297','298','300','312','314','316','317','318','322','334','335','336','337','338','342','343','344','345','346','347','349','353','366','369','373','391','399','402','403','404','405','406','407','408','409','410','411','412','413','414','415','416','417','418','419','420','421','422','423','424','426','427','428','430','431','432','433','434','436','437','438','439','440','441','442','443','444','445','446','474','496','498','512','513','514','516','517','519','520','521','522','532','535','537','538','540','542','558','561','562','563','564','565','591','592','594','595','596','597','598','599','603','605','607','610','615','616','617','618','619','620','621','623','625','626','627','628','629','631','637','638','639','640','641','642','643','644','645','646','647','648','651','655','656','658','659','660','661','662','663','664','665','666','667','668','669','670','672','675','676','677','680','681','682','688','690','691','694','695','696','697','698','699','700','701','702','703','704','748','749','750','752','753','754','755','756','757','758','771','773','774','775','776','777','778','779','781','783','784','785','786','787','788','789','790','791','792','793','794','795','833','834','835','836','844','845','846','847','851','852','856','857','858','859','862','863','864','865','866','867','868','869','877','887','888','889','890','891','892','894','895','899','902','921','922','923','924','926','927','928','929','930','931','932','933','934','935','936','937','938')
                                    AND KDIJ.C4 = 'N' 
                                    AND KDIJ.C5 = 'D' 
                                    AND KDIJ.C6 IN ('25') 
                                    AND KDIJ.C7 IN ('4','12') 
                                GROUP BY KDII.C1, KDII.C2, KDUV.C2, KDUV.C3, KDIJ.C1
                        ) AS KLDB 
            ) AS B ON A.CODIGO = B.CODIGO AND A.ID_VENDEDOR = B.ID_VENDEDOR LEFT JOIN (
                        SELECT
                            (ISNULL(KLDB.PESOS,0))							AS PESOS,
                            'CodigoUnion'									AS CodigoUnion
                        FROM(
                                /*Sumatoria total de B.PESOS*/
                                SELECT
                                    CASE	 
                                            WHEN KDIJ.C1 IN ('02','03','04','05','08','10','11','12','13','15','16','19')	THEN SUM(KDIJ.C11 * KDII.C14)
                                            WHEN KDIJ.C1 IN ('07','18')												THEN SUM(KDIJ.C11 * KDII.C15)
                                            WHEN KDIJ.C1 IN ('06','09','14')											THEN SUM(KDIJ.C11 * KDII.C16)
                                            WHEN KDIJ.C1 IN ('17')													THEN SUM(KDIJ.C11 * KDII.C17)
                                    END																				AS PESOS,
                                    'CodigoUnion'																	AS CodigoUnion
                                FROM KDIJ 
                                    INNER JOIN KDUV ON KDUV.C24 = KDIJ.C2 AND KDUV.C1 = KDIJ.C1 
                                    INNER JOIN KDMS ON KDMS.C1 = KDIJ.C1 
                                    INNER JOIN KDII ON KDII.C1 = KDIJ.C3
                                WHERE	
                                    KDIJ.C1 IN (%s) /*sucursal*/
                                    AND KDIJ.C10 >= CONVERT(DATETIME,  %s, 102) /*FInicial*/
                                    AND KDIJ.C10 <= CONVERT(DATETIME,  %s, 102) /*FFinal*/
                                    --AND KDIJ.C2   IN ('145','718','143','122','448','624','119','108','171','525','197','58','622','63','170','184','855','112','173','183')
                                    AND KDUV.C2 NOT IN ('101','102','103','104','105','106','107','108','109','110','111','112','113','114','115','116','117','118','119','120','121','122','123','124','125','126','127','128','129','130','131','135','136','139','141','144','145','146','149','152','154','155','156','162','163','164','165','172','174','175','176','177','178','179','188','189','193','201','202','203','204','233','238','293','296','297','298','300','312','314','316','317','318','322','334','335','336','337','338','342','343','344','345','346','347','349','353','366','369','373','391','399','402','403','404','405','406','407','408','409','410','411','412','413','414','415','416','417','418','419','420','421','422','423','424','426','427','428','430','431','432','433','434','436','437','438','439','440','441','442','443','444','445','446','474','496','498','512','513','514','516','517','519','520','521','522','532','535','537','538','540','542','558','561','562','563','564','565','591','592','594','595','596','597','598','599','603','605','607','610','615','616','617','618','619','620','621','623','625','626','627','628','629','631','637','638','639','640','641','642','643','644','645','646','647','648','651','655','656','658','659','660','661','662','663','664','665','666','667','668','669','670','672','675','676','677','680','681','682','688','690','691','694','695','696','697','698','699','700','701','702','703','704','748','749','750','752','753','754','755','756','757','758','771','773','774','775','776','777','778','779','781','783','784','785','786','787','788','789','790','791','792','793','794','795','833','834','835','836','844','845','846','847','851','852','856','857','858','859','862','863','864','865','866','867','868','869','877','887','888','889','890','891','892','894','895','899','902','921','922','923','924','926','927','928','929','930','931','932','933','934','935','936','937','938')
                                    AND KDIJ.C4 = 'N' 
                                    AND KDIJ.C5 = 'D' 
                                    AND KDIJ.C6 IN ('25') 
                                    AND KDIJ.C7 IN ('4','12') 
                                GROUP BY KDIJ.C1 
                        ) AS KLDB
            ) AS C ON A.CodigoUnion = C.CodigoUnion Or  B.CodigoUnion = C.CodigoUnion
            WHERE B.PESOS > 0
            GROUP BY A.CODIGO, B.CODIGO, A.PRODUCTO, B.PRODUCTO, A.PIEZAS, A.PESOS, B.PIEZAS, B.PESOS, A.VENDEDOR, B.VENDEDOR, C.PESOS
        """

        params = [
            sucursal, fecha_inicial, fecha_final,
            sucursal, fecha_inicial, fecha_final,
            sucursal, fecha_inicial, fecha_final,
        ]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        
    return result
    
