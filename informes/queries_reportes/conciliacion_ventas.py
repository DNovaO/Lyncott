# Description: Consulta de conciliación de ventas
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaConciliacionVentas(fecha_inicial, fecha_final,cliente_inicial, cliente_final, vendedor_inicial, vendedor_final, sucursal, documento):
   
    if sucursal == "ALL":
        filtro_sucursal = f"AND KDMS.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"AND KDMS.C1 = '{sucursal}'" 
        
    if documento == "ALL":
        filtro_documento = "AND KDM1.C5 IN ('23', '24', '27')"
    else:
        filtro_documento = f"AND KDM1.C5 = '{documento}'"
   
    with connection.cursor() as cursor:
        query = f"""
            DECLARE
                @sucursal VARCHAR(20) = %s,
                @fecha_inicial VARCHAR(20) = %s,
                @fecha_final VARCHAR(20) = %s,
                @cliente_inicial VARCHAR(20) =  %s,
                @cliente_final VARCHAR(20) = %s,
                @vendedor_inicial VARCHAR(20) = %s,
                @vendedor_final VARCHAR(20) = %s;

            SELECT 
                primeraSeleccion.C1 as 'sucursal',
                primeraSeleccion.C2 as 'genero',
                primeraSeleccion.C3 as 'naturaleza',
                primeraSeleccion.C4 as 'grupo_movimiento',
                primeraSeleccion.C5 as 'tipo_documento',
                primeraSeleccion.C6 as 'folio_documento',
                primeraSeleccion.C9 as 'fecha',
                primeraSeleccion.C10 as 'clave_cliente',
                nombreCliente.C3 as 'nombre_cliente',
                primeraSeleccion.C12 as 'clave_vendedor',
                primeraSeleccion.C11 as 'referencia',
                primeraSeleccion.C36 as 'naturaleza_documento_anexado',
                primeraSeleccion.C37 as 'grupo_documento_anexado',
                primeraSeleccion.C38 as 'tipo_documento_anexado',
                primeraSeleccion.C39 as 'folio_documento_anexado',

                segundaSeleccion.C1 as 'sucursal1',
                segundaSeleccion.C2 as 'genero1',
                segundaSeleccion.C3 as 'naturaleza1',
                segundaSeleccion.C4 as 'grupo_movimiento1',
                segundaSeleccion.C5 as 'tipo_documento1',
                segundaSeleccion.C6 as 'folio_documento1',
                segundaSeleccion.C9 as 'fecha1',
                segundaSeleccion.C10 as 'clave_cliente1',
                segundaSeleccion.C11 as 'referencia1',
                segundaSeleccion.C12 as 'clave_vendedor1',
                segundaSeleccion.C36 as 'naturaleza_documento_anexado1',
                segundaSeleccion.C37 as 'grupo_documento_anexado1',
                segundaSeleccion.C38 as 'tipo_documento_anexado1',
                segundaSeleccion.C39 as 'folio_documento_anexado1',
                segundaSeleccion.C16 as 'importe1',

                tercerSeleccion.C1 as 'sucursal2',
                tercerSeleccion.C2 as 'genero2',
                tercerSeleccion.C3 as 'naturaleza2',
                tercerSeleccion.C4 as 'grupo_movimiento2',
                tercerSeleccion.C5 as 'tipo_documento2',
                tercerSeleccion.C6 as 'folio_documento2',
                tercerSeleccion.C9 as 'fecha2',
                tercerSeleccion.C10 as 'clave_cliente2',
                tercerSeleccion.C11 as 'referencia2',
                tercerSeleccion.C12 as 'clave_vendedor2',
                tercerSeleccion.C36 as 'naturaleza_documento_anexado2',
                tercerSeleccion.C37 as 'grupo_documento_anexado2',
                tercerSeleccion.C38 as 'tipo_documento_anexado2',
                tercerSeleccion.C39 as 'folio_documento_anexado2',
                tercerSeleccion.C16 as 'PFD',

                cuartaSeleccion.C14 as 'folio_facturas'
            FROM KDM1 AS primeraSeleccion
            LEFT JOIN KDM1 AS segundaSeleccion 
                ON segundaSeleccion.C1 = primeraSeleccion.C1
                AND segundaSeleccion.C2 = 'U'
                AND segundaSeleccion.C3 = primeraSeleccion.C36
                AND segundaSeleccion.C4 = primeraSeleccion.C37
                AND segundaSeleccion.C5 = primeraSeleccion.C38
                AND segundaSeleccion.C6 = primeraSeleccion.C39
                and segundaSeleccion.C43 <> 'C'
            LEFT JOIN KDM1 AS tercerSeleccion
                ON tercerSeleccion.C1 = primeraSeleccion.C1
                AND tercerSeleccion.C2 = 'U'
                AND tercerSeleccion.C3 = 'D'
                AND tercerSeleccion.C36 = primeraSeleccion.C3
                AND tercerSeleccion.C37 = primeraSeleccion.C4
                AND tercerSeleccion.C38 = primeraSeleccion.C5
                AND tercerSeleccion.C39 = primeraSeleccion.C6
                AND tercerSeleccion.C43 <> 'C'
            INNER JOIN KDUD AS nombreCliente
                ON nombreCliente.C2 = primeraSeleccion.C10
            LEFT JOIN KDFECFDIVTA as cuartaSeleccion
                ON cuartaSeleccion.C1 = primeraSeleccion.C1
                AND cuartaSeleccion.C2 = primeraSeleccion.C2
                AND cuartaSeleccion.C3 = primeraSeleccion.C3
                AND cuartaSeleccion.C4 = primeraSeleccion.C4
                AND cuartaSeleccion.C5 = primeraSeleccion.C5
                AND cuartaSeleccion.C6 = primeraSeleccion.C6
            WHERE
                primeraSeleccion.C1 = @sucursal
                AND primeraSeleccion.C2 = 'U'
                AND primeraSeleccion.C3 = 'D'
                AND primeraSeleccion.C4 = 5
                AND primeraSeleccion.C9 BETWEEN @fecha_inicial AND @fecha_final
                AND primeraSeleccion.C10 BETWEEN @cliente_inicial AND @cliente_final
                AND primeraSeleccion.C12 BETWEEN @vendedor_inicial AND @vendedor_final
            ORDER BY primeraSeleccion.C6;     
        """
        
        # Definir los parámetros para las fechas y filtros
        params = [
            sucursal,
            fecha_inicial, fecha_final,
            cliente_inicial, cliente_final, 
            vendedor_inicial, vendedor_final
        ]

        print(f"Parámetros de consulta: {params}")  # Imprimir los parámetros para depuración
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Convertir Decimals a float y datetime a string para evitar problemas
    for row in result:
        for key, value in row.items():
            if isinstance(value, Decimal):
                row[key] = float(value)
            elif isinstance(value, datetime):  # Verifica si es un objeto datetime
                row[key] = value.strftime('%Y-%m-%d %H:%M:%S')  # Convierte a formato string


    return result
