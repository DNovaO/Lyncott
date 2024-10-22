# Description: Consulta de ventas por producto por giro
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

# Diccionario de nombres de meses en español
NOMBRES_MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

# Genera una lista de tuplas (número de mes, nombre del mes) entre dos fechas
def generar_meses(fecha_inicial, fecha_final):
    meses = []
    fecha_actual = fecha_inicial.replace(day=1)  # Iniciar al principio del mes
    while fecha_actual <= fecha_final:
        meses.append((fecha_actual.month, NOMBRES_MESES[fecha_actual.month]))
        fecha_actual += timedelta(days=32)  # Avanzar al siguiente mes
        fecha_actual = fecha_actual.replace(day=1)  # Reiniciar al día 1
    return meses

def consultaDevolucionesPorClienteConsignatarioPorMes(
    fecha_inicial, fecha_final, cliente_inicial, cliente_final, 
    producto_inicial, producto_final, sucursal_inicial, sucursal_final, grupoCorporativo
):
    print(f"Fecha inicial: {fecha_inicial}, Fecha final: {fecha_final}, grupo corporativo: {grupoCorporativo}")

    # Definir la cláusula del grupo corporativo dependiendo de su valor
    grupoCorporativoClause = ''
    if grupoCorporativo == 'ALL':
        grupoCorporativoClause = "AND KDUD.C66 BETWEEN '7 ELEV' AND 'POSAD'"
    elif grupoCorporativo:  # Esto captura cualquier valor que no sea None o vacío
        grupoCorporativoClause = "AND KDUD.C66 BETWEEN '7 ELEV' AND ''"

    # Generar los nombres de los meses para el rango proporcionado
    meses_rango = generar_meses(fecha_inicial, fecha_final)

    # Crear las columnas dinámicas para cada mes
    columnas_meses = ", ".join([
        f"SUM(CASE WHEN MONTH(KDIJ.C10) = {mes_num} THEN KDIJ.C14 ELSE 0 END) AS devoluciones_{mes_nombre}"
        for mes_num, mes_nombre in meses_rango
    ])

    with connection.cursor() as cursor:
        query = f"""
            DECLARE 
                @fecha_inicial DATE = CONVERT(DATE, %s, 102),
                @fecha_final DATE = CONVERT(DATE, %s, 102),
                @cliente_inicial VARCHAR(20) = %s,
                @cliente_final VARCHAR(20) = %s,
                @producto_inicial VARCHAR(20) = %s,
                @producto_final VARCHAR(20) = %s,
                @sucursal_inicial VARCHAR(20) = %s,
                @sucursal_final VARCHAR(20) = %s,
                @grupo_corporativo VARCHAR(20) = %s;
            
            SELECT 
                LTRIM(RTRIM(KDIJ.C1)) AS sucursal,
                LTRIM(RTRIM(KDUD.C66)) AS grupo,
                LTRIM(RTRIM(KDUD.C2)) AS clave_cliente,
                LTRIM(RTRIM(KDM1.C181)) AS clave_consignatario,
                LTRIM(RTRIM(KDVDIREMB.C3)) AS consignatario,
                {columnas_meses},  -- Columnas de meses dinámicas
                SUM(KDIJ.C14) AS total_devoluciones
            FROM KDIJ
            INNER JOIN KDII ON KDIJ.C3 = KDII.C1
            INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
            LEFT JOIN KDM1 ON KDIJ.C1 = KDM1.C1 
                AND KDIJ.C4 = KDM1.C2 
                AND KDIJ.C5 = KDM1.C3 
                AND KDIJ.C6 = KDM1.C4 
                AND KDIJ.C7 = KDM1.C5 
                AND KDIJ.C8 = KDM1.C6
            LEFT JOIN KDVDIREMB ON KDM1.C10 = KDVDIREMB.C1 
                AND KDM1.C181 = KDVDIREMB.C2
            WHERE 
                KDII.C1 BETWEEN @producto_inicial AND @producto_final
                AND KDIJ.C10 BETWEEN @fecha_inicial AND @fecha_final
                AND KDIJ.C1 BETWEEN @sucursal_inicial AND @sucursal_final
                AND KDUD.C2 BETWEEN @cliente_inicial AND @cliente_final
                {grupoCorporativoClause}  -- Aquí se añade la cláusula del grupo corporativo
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
                KDIJ.C1, KDUD.C66, KDUD.C2, KDM1.C181, KDVDIREMB.C3;
        """

        # Definir los parámetros para las fechas y filtros
        params = [
            fecha_inicial, fecha_final, 
            cliente_inicial, cliente_final, 
            producto_inicial, producto_final, 
            sucursal_inicial, sucursal_final,
            grupoCorporativo if grupoCorporativo else None  # Pasar None si es vacío
        ]

        print(f"Parámetros de consulta: {params}")  # Imprimir los parámetros para depuración
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Convertir Decimals a float para evitar problemas al mostrar los datos
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result
