# Description: Consulta de presupuesto vs ventas por sucursal y año
from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from informes.models import *
from decimal import Decimal
from django.db import connection

def consultaPresupuestoVsVentas(sucursal, year):
    print(f"Consulta de ventas por sucursal: {sucursal} y el año {year}")

    if sucursal == 'ALL':
        filtro_sucursal = f"kdv.C1 BETWEEN '02' AND '20'"
    else:
        filtro_sucursal = f"kdv.C1 = '{sucursal}'"

    with connection.cursor() as cursor:
        query = f"""
            SELECT
                kdv.C1 AS "clave_sucursal",
                kdms.C2 AS "sucursal",
                kdv.C2 AS "moneda",
                CASE
                    WHEN kdv.C1 = '02' THEN 
                        CASE
                            WHEN kdv.C4 = 1 THEN 'Autoservicio'
                            WHEN kdv.C4 = 2 THEN 'FoodService Norte'
                            WHEN kdv.C4 = 3 THEN 'FoodService Sur'
                            WHEN kdv.C4 = 4 THEN 'Ventas Especiales'
                            WHEN kdv.C4 = 5 THEN 'Cadenas'
                            WHEN kdv.C4 = 6 THEN 'Centro'
                            ELSE 'Sin asignar a Vallejo'
                        END
                    WHEN kdv.C1 IN ('17', '04', '15', '16') THEN '2 - Norte'
                    WHEN kdv.C1 IN ('05', '10', '19', '08') THEN '3 - Centro'
                    WHEN kdv.C1 IN ('09', '14', '03', '12', '06', '20') THEN '4 - Pacifico'
                    WHEN kdv.C1 IN ('13', '11', '18', '07') THEN '5 - Sureste'
                    ELSE 'Sin zona'
                END AS "zona",
                FORMAT(
                    COALESCE(kdv.C5, 0) +
                    COALESCE(kdv.C6, 0) +
                    COALESCE(kdv.C7, 0) +
                    COALESCE(kdv.C8, 0) +
                    COALESCE(kdv.C9, 0) +
                    COALESCE(kdv.C10, 0) +
                    COALESCE(kdv.C11, 0) +
                    COALESCE(kdv.C12, 0) +
                    COALESCE(kdv.C13, 0) +
                    COALESCE(kdv.C14, 0) +
                    COALESCE(kdv.C15, 0) +
                    COALESCE(kdv.C16, 0), 'C', 'en_US') AS "presupuesto_total",
                FORMAT(COALESCE(kdv.C5, 0), 'C', 'en_US') AS "presupuesto_enero",
                FORMAT(COALESCE(kdv.C6, 0), 'C', 'en_US') AS "presupuesto_febrero",
                FORMAT(COALESCE(kdv.C7, 0), 'C', 'en_US') AS "presupuesto_marzo",
                FORMAT(COALESCE(kdv.C8, 0), 'C', 'en_US') AS "presupuesto_abril",
                FORMAT(COALESCE(kdv.C9, 0), 'C', 'en_US') AS "presupuesto_mayo",
                FORMAT(COALESCE(kdv.C10, 0), 'C', 'en_US') AS "presupuesto_junio",
                FORMAT(COALESCE(kdv.C11, 0), 'C', 'en_US') AS "presupuesto_julio",
                FORMAT(COALESCE(kdv.C12, 0), 'C', 'en_US') AS "presupuesto_agosto",
                FORMAT(COALESCE(kdv.C13, 0), 'C', 'en_US') AS "presupuesto_septiembre",
                FORMAT(COALESCE(kdv.C14, 0), 'C', 'en_US') AS "presupuesto_octubre",
                FORMAT(COALESCE(kdv.C15, 0), 'C', 'en_US') AS "presupuesto_noviembre",
                FORMAT(COALESCE(kdv.C16, 0), 'C', 'en_US') AS "presupuesto_diciembre"
            FROM
                KDVPRESXSUC kdv
            JOIN
                KDMS kdms ON kdv.C1 = kdms.C1
            WHERE
                {filtro_sucursal} 
                AND kdv.C3 = %s; -- YEAR DE LOS DATOS
        """

        params = [year]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result