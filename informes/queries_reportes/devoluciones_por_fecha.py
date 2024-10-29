#Description: Consulta de devoluciones por fecha

# Description: Consulta de tendencia ventas por giro
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection
from informes.f_DifDias import *
from informes.f_DifDiasTotales import *


def consultaDevolucionesPorFecha(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, grupo_corporativo):
    print (f"fecha_inicial: {fecha_inicial}, fecha_final: {fecha_final}, sucursal_inicial: {sucursal_inicial}, sucursal_final: {sucursal_final}, grupo_corporativo: {grupo_corporativo}")
    
    # Si grupo_corporativo es 'ALL', cambia a '%' para incluir todos los grupos
    if grupo_corporativo == 'ALL':
        grupo_corporativo = '%'  # Esto hará que LIKE funcione para todos los grupos
    
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
            DECLARE @fecha_inicial VARCHAR(20) = %s,
                    @fecha_final VARCHAR(20) = %s,
                    @sucursal_inicial VARCHAR(20) = %s,
                    @sucursal_final VARCHAR(20) = %s,
                    @grupo_corporativo VARCHAR(20) = %s;
                    
            SELECT 
                DBKL.ID_GrupoCorporativo AS clave_grupo_corporativo,
                GrupoCorporativo.C2 AS grupo_corporativo,
                Sucursal.C2 AS sucursal,
                DBKL.ID_Cliente AS clave_cliente,
                Cliente.C3 AS cliente,
                DBKL.ID_Consignatario AS clave_consignatario,
                Consignatario.C3 AS consignatario,
                DBKL.ID_Producto AS clave_producto,
                Producto.C2 AS producto,
                ISNULL(DBKL.CANTIDAD, 0) AS cantidad,
                ISNULL(DBKL.KGSLTS, 0) AS kgslts,
                ISNULL(DBKL.VENTA, 0) AS venta,
                CONVERT(varchar, DBKL.FECHA, 103) AS fecha 
            FROM (
                SELECT 
                    KDUD.C66 AS ID_GrupoCorporativo,
                    KDIJ.C1 AS ID_Sucursal,
                    KDIJ.C15 AS ID_Cliente,
                    KDM1.C181 AS ID_Consignatario,
                    KDIJ.C3 AS ID_Producto,
                    SUM(KDIJ.C11) AS CANTIDAD, 
                    SUM(KDIJ.C11 * KDII.C13) AS KGSLTS, 
                    SUM(KDIJ.C14) AS VENTA,
                    KDIJ.C10 AS FECHA
                FROM KDIJ  
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1 
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2 
                INNER JOIN KDM1 ON KDIJ.C1 = KDM1.C1 
                    AND KDIJ.C4 = KDM1.C2 
                    AND KDIJ.C5 = KDM1.C3 
                    AND KDIJ.C6 = KDM1.C4 
                    AND KDIJ.C7 = KDM1.C5 
                    AND KDIJ.C8 = KDM1.C6
                WHERE 
                    KDIJ.C10 >= CONVERT(DATETIME, @fecha_inicial, 102)
                    AND KDIJ.C10 <= CONVERT(DATETIME, @fecha_final, 102)
                    {filtro_sucursal}
                    AND KDUD.C66 LIKE @grupo_corporativo
                    AND KDIJ.C16 NOT IN (
                        '902', '903', '904', '905', '906', '907', '908', '909', '910', 
                        '911', '912', '913', '914', '915', '916', '917', '918', '919', 
                        '920', '921', '922', '923', '924'
                    )
                    AND KDIJ.C4 = 'N' 
                    AND KDIJ.C5 = 'D' 
                    AND KDIJ.C6 IN ('25') 
                    AND KDIJ.C7 IN ('12')
                GROUP BY 
                    KDUD.C66, KDIJ.C1, KDIJ.C15, KDM1.C181, KDIJ.C3, KDIJ.C10
            ) AS DBKL 
            INNER JOIN (
                SELECT C1, C2 FROM KDCORPO
            ) AS GrupoCorporativo ON DBKL.ID_GrupoCorporativo = GrupoCorporativo.C1
            INNER JOIN (
                SELECT C2, C3 FROM KDUD
            ) AS Cliente ON DBKL.ID_Cliente = Cliente.C2
            INNER JOIN (
                SELECT C1, C2, C3 FROM KDVDIREMB
            ) AS Consignatario ON Consignatario.C1 = DBKL.ID_Cliente AND DBKL.ID_Consignatario = Consignatario.C2
            INNER JOIN (
                SELECT C1, C2 FROM KDII
            ) AS Producto ON DBKL.ID_Producto = Producto.C1
            INNER JOIN (
                SELECT C1, C2 FROM KDMS
            ) AS Sucursal ON DBKL.ID_Sucursal = Sucursal.C1
            ORDER BY 
                DBKL.ID_Consignatario, DBKL.ID_Producto;
        """

        params = [
                    fecha_inicial, fecha_final,
                    sucursal_inicial, sucursal_final, 
                    grupo_corporativo
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