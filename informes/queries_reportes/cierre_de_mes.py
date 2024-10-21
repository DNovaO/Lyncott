# Description: Consulta de cierre de mes
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaCierreDeMes(fecha_inicial, fecha_final, sucursal):
    print(f"Consulta de cierre de mes desde {fecha_inicial} hasta {fecha_final}, sucursal: {sucursal}")

    with connection.cursor() as cursor:
        
        # Condicional para sucursal
        if sucursal == 'ALL':
            filtro_sucursal =  "AND KDM1.C1 BETWEEN 1 AND 20"  # Asegurando que los valores sean válidos como enteros
        else:
            filtro_sucursal = f"AND KDM1.C1 = {sucursal}"  # Filtra por sucursal específica

        # Query con el condicional aplicado
        query = f"""
            SET LANGUAGE Español;

            SELECT 
                KDM1.C1 AS sucursal,          
                KDM1.C2 AS genero,            
                KDM1.C3 AS naturaleza,        
                KDM1.C4 AS grupo_movimiento,  
                KDM1.C5 AS numero_tipo_documento,  
                KDMM.C5 AS detalles_tipo_documento, 

                ISNULL(SUM(CASE 
                    WHEN KDM1.C5 IN ('18', '20', '21', '23', '25')  
                    THEN (KDM1.C16 - KDM1.C15) 
                    ELSE 0 
                END), 0) AS CREDITO_FAC,

                ISNULL(SUM(CASE 
                    WHEN KDM1.C5 IN ('19', '22', '24', '26')  
                    THEN (KDM1.C16 - KDM1.C15) 
                    ELSE 0 
                END), 0) AS CONTADO_FAC,

                ISNULL(SUM(CASE 
                    WHEN KDM1.C5 IN ('1', '3', '5', '21', '25', '18')  
                    THEN (KDM1.C16 - KDM1.C15) 
                    ELSE 0 
                END), 0) AS CREDITO_REM,

                ISNULL(SUM(CASE 
                    WHEN KDM1.C5 IN ('2', '4', '6', '22', '26', '19')  
                    THEN (KDM1.C16 - KDM1.C15) 
                    ELSE 0 
                END), 0) AS CONTADO_REM

            FROM dbo.KDM1
            FULL JOIN dbo.KDUD ON KDM1.C10 = KDUD.C2
            FULL JOIN dbo.KDMM 
                ON KDM1.C2 = KDMM.C1  
                AND KDM1.C3 = KDMM.C2 
                AND KDM1.C4 = KDMM.C3 
                AND KDM1.C5 = KDMM.C4 

            WHERE 
                KDM1.C9 >= %s  
                AND KDM1.C9 <= %s  
                {filtro_sucursal}  -- Condición dinámica según la sucursal
                AND KDM1.C43 <> 'C' 
                AND KDM1.C12 NOT IN ('902', '903', '904', '905', '906', '907', 
                                    '908', '909', '910', '911', '912', '913', 
                                    '914', '915', '916', '917', '918', '919', 
                                    '920', '921', '922', '923', '924') 
                AND KDM1.C2 = 'U'  
                AND KDM1.C3 = 'D'  
                AND KDM1.C4 IN ('5', '45')  
                AND KDM1.C5 IN ('1', '2', '3', '4', '5', '6', '18', '19', '20', 
                                '21', '22', '23', '24', '25', '26')

            GROUP BY 
                KDM1.C1, 
                KDM1.C2, 
                KDM1.C3, 
                KDM1.C4, 
                KDM1.C5, 
                KDMM.C5 

            ORDER BY 
                KDM1.C1,
                KDM1.C4, 
                KDM1.C5;
        """
        # Ejecutamos la consulta
        cursor.execute(query, [fecha_inicial, fecha_final])
        
        
        print('El parametro es: ', fecha_final, type(fecha_final))
        print('El parametro es: ', fecha_inicial, type(fecha_inicial))
        
        # Obtenemos los nombres de las columnas
        columns = [col[0] for col in cursor.description]
        
        # Obtenemos los resultados como una lista de diccionarios
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Convertimos Decimals a float
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result