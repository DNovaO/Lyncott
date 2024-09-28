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
        query = """
            SET LANGUAGE Español;

            -- Selección de columnas con alias para mejorar la legibilidad
            SELECT 
                KDM1.C1 AS sucursal,            -- Código de la sucursal
                KDM1.C2 AS genero,              -- Género o categoría del movimiento
                KDM1.C3 AS naturaleza,          -- Naturaleza del movimiento
                KDM1.C4 AS grupo_movimiento,    -- Grupo al que pertenece el movimiento
                KDM1.C5 AS numero_tipo_documento,  -- Número del tipo de documento
                KDMM.C5 AS detalles_tipo_documento, -- Detalles relacionados con el tipo de documento desde la tabla KDMM

                -- Suma de movimientos de crédito facturados, aplicando condiciones
                ISNULL(SUM(CASE 
                    WHEN KDM1.C5 IN ('18', '20', '21', '23', '25')  
                    THEN (KDM1.C16 - KDM1.C15) -- Diferencia entre C16 y C15 (ingresos - egresos)
                    ELSE 0 
                END), 0) AS CREDITO_FAC,

                -- Suma de movimientos de contado facturados
                ISNULL(SUM(CASE 
                    WHEN KDM1.C5 IN ('19', '22', '24', '26')  
                    THEN (KDM1.C16 - KDM1.C15) -- Diferencia entre C16 y C15 (ingresos - egresos)
                    ELSE 0 
                END), 0) AS CONTADO_FAC,

                -- Suma de movimientos de crédito remisionados
                ISNULL(SUM(CASE 
                    WHEN KDM1.C5 IN ('1', '3', '5', '21', '25', '18')  
                    THEN (KDM1.C16 - KDM1.C15) -- Diferencia entre C16 y C15 (ingresos - egresos)
                    ELSE 0 
                END), 0) AS CREDITO_REM,

                -- Suma de movimientos de contado remisionados
                ISNULL(SUM(CASE 
                    WHEN KDM1.C5 IN ('2', '4', '6', '22', '26', '19')  
                    THEN (KDM1.C16 - KDM1.C15) -- Diferencia entre C16 y C15 (ingresos - egresos)
                    ELSE 0 
                END), 0) AS CONTADO_REM

            -- Desde la tabla KDM1 (principal)    
            FROM dbo.KDM1

            -- Unión completa (FULL JOIN) con KDUD usando C10 de KDM1 y C2 de KDUD
            FULL JOIN dbo.KDUD 
                ON KDM1.C10 = KDUD.C2

            -- Unión completa con KDMM, haciendo coincidir múltiples columnas de ambas tablas
            FULL JOIN dbo.KDMM 
                ON KDM1.C2 = KDMM.C1  -- Empareja C2 de KDM1 con C1 de KDMM
                AND KDM1.C3 = KDMM.C2 -- Empareja C3 de KDM1 con C2 de KDMM
                AND KDM1.C4 = KDMM.C3 -- Empareja C4 de KDM1 con C3 de KDMM
                AND KDM1.C5 = KDMM.C4 -- Empareja C5 de KDM1 con C4 de KDMM

            -- Condiciones de filtrado para restringir los resultados
            WHERE 
                KDM1.C9 >= %s   -- Rango de fechas (inicio)
                AND KDM1.C9 <= %s   -- Rango de fechas (fin)
                AND KDM1.C1 = %s    -- Filtro por sucursal (pasada como parámetro)
                AND KDM1.C43 <> 'C' -- Excluye registros donde C43 tiene el valor 'C'
                AND KDM1.C12 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913',
                                    '914','915','916','917','918','919','920','921','922','923','924') -- Excluye ciertos códigos de C12
                AND KDM1.C2 = 'U'   -- Filtra por género 'U'
                AND KDM1.C3 = 'D'   -- Filtra por naturaleza 'D'
                AND KDM1.C4 IN ('5', '45')  -- Filtra por grupo de movimiento en un conjunto dado
                AND KDM1.C5 IN ('1','2','3','4','5','6','18','19','20','21','22','23','24','25','26') -- Filtra por tipos de documento específicos

            -- Agrupa los resultados por estas columnas
            GROUP BY 
                KDM1.C1,  -- Sucursal
                KDM1.C2,  -- Género
                KDM1.C3,  -- Naturaleza
                KDM1.C4,  -- Grupo de movimiento
                KDM1.C5,  -- Número de tipo de documento
                KDMM.C5   -- Detalles del tipo de documento

            -- Ordena el resultado final por grupo de movimiento y número de tipo de documento
            ORDER BY 
                KDM1.C4,  -- Grupo de movimiento
                KDM1.C5;  -- Número de tipo de documento

        """

        # Ejecutamos la consulta
        cursor.execute(query, [fecha_inicial, fecha_final, sucursal])
        
        
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