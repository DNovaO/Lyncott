from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from .models import *
from decimal import Decimal
from django.db import connection

def clasificarParametros(parametrosSeleccionados, tipo_reporte):
    filtros = {}
    
    for key, value in parametrosSeleccionados.items():
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            for item in value:
                key_value = item[list(item.keys())[0]].strip()
                if key in ('fecha_inicial', 'fecha_final', 'cliente_inicial', 'cliente_final', 'producto_inicial', 'producto_final', 'sucursal', 'sucursal_inicial', 'sucursal_final', 'vendedor_inicial', 'vendedor_final', 'linea_inicial', 'linea_final', 'familia', 'familia_inicial', 'familia_final', 'marca_inicial', 'marca_final', 'grupoCorporativo', 'grupoCorporativo_inicial', 'grupoCorporativo_final', 'segmento_inicial', 'segmento_final', 'status', 'zona', 'grupo', 'region', 'year'):
                    filtros[key] = key_value
        else:
            if isinstance(value, list) and len(value) > 0:
                value = value[0]
                if isinstance(value, dict):
                    value = value[list(value.keys())[0]].strip()
                    
            filtros[key] = value
    
    return ejecutarConsulta(filtros, tipo_reporte)

def ejecutarConsulta(filtros, tipo_reporte):
    fecha_inicial_str = filtros.get('fecha_inicial')
    fecha_final_str = filtros.get('fecha_final')
    cliente_inicial = filtros.get('cliente_inicial')
    cliente_final = filtros.get('cliente_final')
    producto_inicial = filtros.get('producto_inicial')
    producto_final = filtros.get('producto_final')
    sucursal = filtros.get('sucursal')
    sucursal_inicial = filtros.get('sucursal_inicial')
    sucursal_final = filtros.get('sucursal_final')
    vendedor_inicial = filtros.get('vendedor_inicial')
    vendedor_final = filtros.get('vendedor_final')
    linea_inicial = filtros.get('linea_inicial')
    linea_final = filtros.get('linea_final')
    familia = filtros.get('familia')
    familia_inicial = filtros.get('familia_inicial')
    familia_final = filtros.get('familia_final')
    marca_inicial = filtros.get('marca_inicial')
    marca_final = filtros.get('marca_final')
    grupoCorporativo = filtros.get('grupoCorporativo')
    grupoCorporativo_inicial = filtros.get('grupoCorporativo_inicial')
    grupoCorporativo_final = filtros.get('grupoCorporativo_final')
    segmento_inicial = filtros.get('segmento_inicial')
    segmento_final = filtros.get('segmento_final')
    status = filtros.get('status')
    zona = filtros.get('zona')
    grupo = filtros.get('grupo')
    region = filtros.get('region')
    year = filtros.get('year')

    fecha_inicial = parse_date(fecha_inicial_str)
    fecha_final = parse_date(fecha_final_str)
    
    resultados = []
                        
    if tipo_reporte == "Por Producto (con Refacturación)":
        resultados.extend(consultaVentasPorProductoConRefacturacion(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final))
    
    elif tipo_reporte == "Por Tipo de Cliente (con Refacturación)":
        resultados.extend(consultaVentaPorCliente(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final))
    
    elif tipo_reporte == "Credito Contable (con Refacturación)":
        resultados.extend(consultaVentaPorCreditoContable(fecha_inicial, fecha_final, cliente_inicial, cliente_final))
        
    elif tipo_reporte == "Clientes por Grupos":
        resultados.extend(consultaClientesPorGrupo(grupoCorporativo_inicial, grupoCorporativo_final))
    
    elif tipo_reporte == "Cierre de Mes":
        resultados.extend(consultaCierreDeMes(fecha_inicial, fecha_final, sucursal))
        
    elif tipo_reporte == "Por Producto":
        resultados.extend(consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final, familia_inicial, familia_final))
    
    elif tipo_reporte == "Por Familia en Kilos (con Refacturación)":
        resultados.extend(consultaVentasPorFamiliaKgConRefacturacion(fecha_inicial, fecha_final, producto_inicial, producto_final, familia_inicial, familia_final, sucursal))
    
    elif tipo_reporte == "Comparativa de Ventas y Presupuesto por Zonas en Pesos":
        resultados.extend(consultaPresupuestoVsVentas(sucursal, year))
        
    elif tipo_reporte == "Trazabilidad por Producto":
        resultados.extend(consultaTrazabilidadPorProducto(fecha_inicial, fecha_final, producto_inicial, producto_final, status, sucursal))
        
    elif tipo_reporte == "Ventas en General (Pesos Sin Refacturación)":
        resultados.extend(consultaVentasEnGeneral(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final))

    
    return resultados
    
def parse_date(date_str):
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    except ValueError:
        return None

def consultaVentasPorProductoConRefacturacion(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final):
    print(f"Consulta de ventas por productos desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}, sucursal inicial: {sucursal_inicial} y sucursal final: {sucursal_final}")
    
    kdii_subquery = Kdii.objects.filter(
        clave_producto=OuterRef('clave_producto')
    ).values(
        'descripcion_producto',
        'unidad_medida',
        'unidad_alternativa',
        'factor_conversion'
    )[:1]

    subqueryVentaPorProducto = Kdij.objects.filter(
        clave_cliente__gte=cliente_inicial,
        clave_cliente__lte=cliente_final,
        clave_producto__gte=producto_inicial,
        clave_producto__lte=producto_final,
        fecha__gte=fecha_inicial,
        fecha__lte=fecha_final,
        clave_sucursal__gte=sucursal_inicial,
        clave_sucursal__lte=sucursal_final,
        genero='U',
        naturaleza='D',
        grupo_movimiento__in=['5', '45']
    ).values(
        'clave_producto'
    ).annotate(
        descripcion_producto=Subquery(kdii_subquery.values('descripcion_producto')),
        
        unidad_medida=Subquery(kdii_subquery.values('unidad_medida')),
        
        unidad_alternativa=Subquery(kdii_subquery.values('unidad_alternativa')),
        
        factor_conversion=Subquery(kdii_subquery.values('factor_conversion')),
        
        cantidad=Round(Sum('cantidad_unidades_entrada'), 2),
        
        venta_sumatoria=Sum('monto_venta'),
        
        venta=Concat(
            Value('$'),
            'venta_sumatoria',
            output_field=CharField()
        ),
        
        kgslts=ExpressionWrapper(
            Round(F('cantidad') * F('factor_conversion'), 2),
            output_field=FloatField()
        ),
        
        venta_sobre_Kg = ExpressionWrapper(
            F('venta_sumatoria') / F('kgslts'),
            output_field=FloatField()
        ),
        
        venta_sobre_UV = ExpressionWrapper(
            Round(F('venta_sumatoria') / F('cantidad'), 2),
            output_field=FloatField()
        ),   
    )

    queryVentaPorProducto = subqueryVentaPorProducto.values(
        'clave_producto',
        'descripcion_producto',
        'cantidad',
        'unidad_medida',
        'kgslts',
        'unidad_alternativa',
        'venta_sobre_Kg',
        'venta_sobre_UV',
        'venta',
    ).order_by(
        'clave_producto'
    )

    return list(queryVentaPorProducto)

def consultaClientesPorGrupo(grupoCorporativo_inicial, grupoCorporativo_final):
    print(f"Consulta de clientes por grupo corporativo desde {grupoCorporativo_inicial} hasta {grupoCorporativo_final}")

    # Query principal
    queryClientesporGrupo = Kdud.objects.filter(
        clave_corporativo__gte=grupoCorporativo_inicial,
        clave_corporativo__lte=grupoCorporativo_final,
    ).annotate(
        id_grupo=Subquery(
            Kdcorpo.objects.filter(
                clave_corporativo=OuterRef('clave_corporativo')
            ).values(
                'clave_corporativo'
            )[:1]
        ),
        grupo=Subquery(
            Kdcorpo.objects.filter(
                clave_corporativo=OuterRef('clave_corporativo')
            ).values(
                'descripcion_corporativo'
            )[:1]
        ),
    ).values(
        id_grupo=F('id_grupo'),
        grupo=F('grupo'),
        clave=LTrim(RTrim('clave_cliente')),
        cliente=LTrim(RTrim('nombre_cliente')),
    ).order_by(
        'id_grupo',
        'clave',
    )
    
    return list(queryClientesporGrupo)

def consultaCierreDeMes(fecha_inicial, fecha_final, sucursal):
    print(f"Consulta de cierre de mes desde {fecha_inicial} hasta {fecha_final}, sucursal: {sucursal}")

    with connection.cursor() as cursor:
        query = """
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

def consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final, familia_inicial, familia_final):
    print(f"Consulta de ventas por producto desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}, sucursal inicial: {sucursal_inicial} y sucursal final: {sucursal_final}, familia inicial: {familia_inicial} y familia final: {familia_final}")

    with connection.cursor() as cursor:
        # Construcción dinámica de la consulta SQL
        query = """
            SELECT 
                dbo.KDII.C1 AS clave_producto,
                dbo.KDII.C2 AS producto,
                SUM(dbo.KDIJ.C11) AS cantidad,
                dbo.KDII.C11 AS tipo_unidad,
                SUM(dbo.KDIJ.C11 * dbo.KDII.C13) AS kgslts,
                dbo.KDII.C12 AS unidad_medida,
                SUM(dbo.KDIJ.C14) AS VENTA,
                SUM(dbo.KDIJ.C14) / SUM(dbo.KDIJ.C11 * dbo.KDII.C13) AS KG,
                SUM(dbo.KDIJ.C14) / SUM(dbo.KDIJ.C11) AS unidad_vendida
            FROM dbo.KDIJ
            INNER JOIN dbo.KDII ON dbo.KDIJ.C3 = dbo.KDII.C1
            INNER JOIN dbo.KDIF ON dbo.KDII.C5 = dbo.KDIF.C1
            INNER JOIN dbo.KDUD ON dbo.KDIJ.C15 = dbo.KDUD.C2
        """
        
        # Condicional para la tabla KDUV
        if sucursal_inicial == '02' and sucursal_final == '02':
            query += "INNER JOIN dbo.KDUV ON dbo.KDIJ.C16 = dbo.KDUV.C2 "

        query += """
            WHERE dbo.KDIF.C1 >= %s -- Familia Inicial
            AND dbo.KDIF.C1 <= %s -- Familia Final
            AND dbo.KDII.C1 >= %s -- Producto Inicial
            AND dbo.KDII.C1 <= %s -- Producto Final
            AND dbo.KDIJ.C1 >= %s -- Sucursal Inicial
            AND dbo.KDIJ.C1 <= %s -- Sucursal Final
            AND dbo.KDIJ.C10 >= %s -- Fecha Inicial
            AND dbo.KDIJ.C10 <= %s -- Fecha Final
            AND dbo.KDUD.C2 >= %s -- Cliente Inicial
            AND dbo.KDUD.C2 <= %s -- Cliente Final
            AND dbo.KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
            AND dbo.KDIJ.C4 = 'U'
            AND dbo.KDIJ.C5 = 'D'
            AND dbo.KDIJ.C6 IN ('5','45')
            AND dbo.KDIJ.C7 IN ('1','2','3','4','5','6','18','19','21','22','25','26','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97')
        """

        # Condicional para la zona si aplica
        if sucursal_inicial == '02' and sucursal_final == '02':
            query += "AND dbo.KDUV.C22 IN (%s) "

        query += """
            GROUP BY dbo.KDII.C1, dbo.KDII.C2, dbo.KDII.C11, dbo.KDII.C12
            ORDER BY dbo.KDII.C1;
        """

        # Parámetros para la consulta
        params = [
            familia_inicial, familia_final, producto_inicial, producto_final, 
            sucursal_inicial, sucursal_final, fecha_inicial, fecha_final, 
            cliente_inicial, cliente_final
        ]

        # Ejecutar la consulta
        cursor.execute(query, params)

        # Obtener los resultados
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
    
    return result

def consultaVentasPorFamiliaKgConRefacturacion(fecha_inicial, fecha_final, producto_inicial, producto_final, familia_inicial, familia_final, sucursal):
    print(f"Consulta de ventas por familia en kilos con refacturación desde {fecha_inicial} hasta {fecha_final}, producto inicial: {producto_inicial} y producto final: {producto_final}, familia inicial: {familia_inicial} y familia final: {familia_final}, sucursal: {sucursal}")
    
    # Si la sucursal es 'ALL', ajustamos el rango de sucursal
    if sucursal == "ALL":
        sucursal_inicial = '01'
        sucursal_final = '20'
    else:
        sucursal_inicial = sucursal
        sucursal_final = sucursal

    with connection.cursor() as cursor:
        query = """ 
            SELECT 
                dbo.KDIF.C1 AS familia, 
                dbo.KDIF.C2 AS descripcion_familia,  
                SUM(dbo.KDIJ.C11) AS unidad, 
                SUM(dbo.KDIJ.C11 * dbo.KDII.C13) AS kg, 
                SUM(dbo.KDIJ.C14) AS ventas
            FROM dbo.KDIJ
                INNER JOIN dbo.KDII ON dbo.KDIJ.C3 = dbo.KDII.C1
                INNER JOIN dbo.KDIF ON dbo.KDII.C5 = dbo.KDIF.C1
                INNER JOIN dbo.KDUV ON dbo.KDIJ.C16 = dbo.KDUV.C2
            WHERE dbo.KDIF.C1 >= %s -- Familia inicial
                AND dbo.KDIF.C1 <= %s -- Familia final
                AND dbo.KDII.C1 >= %s -- Producto inicial
                AND dbo.KDII.C1 <= %s -- Producto final
                AND dbo.KDIJ.C1 >= %s -- Sucursal inicial
                AND dbo.KDIJ.C1 <= %s -- Sucursal final
                AND dbo.KDIJ.C10 >= %s -- Fecha inicial
                AND dbo.KDIJ.C10 <= %s -- Fecha final
                AND dbo.KDIJ.C16 NOT IN ('902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924')
                AND dbo.KDIJ.C4 = 'U'
                AND dbo.KDIJ.C5 = 'D'
                AND dbo.KDIJ.C6 IN ('5', '45')
                AND dbo.KDIJ.C7 IN ('1','2','3','4','5','6','18','19','21','22','25','26','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97')
            GROUP BY dbo.KDIF.C1, dbo.KDIF.C2
            ORDER BY dbo.KDIF.C1
        """
        
        params = [
            familia_inicial, familia_final, producto_inicial, producto_final,
            sucursal_inicial, sucursal_final, fecha_inicial, fecha_final
        ]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
    
    return result

    
def consultaVentaPorCreditoContable(fecha_inicial, fecha_final, cliente_inicial, cliente_final):
    print(f"Consulta de ventas por crédito contable desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial}, cliente final: {cliente_final}")

def consultaVentaPorCliente(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta de ventas por cliente desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}")

def consultaPresupuestoVsVentas(sucursal, year):
    print(f"Consulta de ventas por sucursal: {sucursal} y el año {year}")

    with connection.cursor() as cursor:
        query = """
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
                kdv.C1 = %s -- CLAVE SUCURSAL 
                AND kdv.C3 = %s; -- YEAR DE LOS DATOS
        """

        params = [sucursal, year]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result

#Tabla con formato especial
def consultaTrazabilidadPorProducto(fecha_inicial, fecha_final, producto_inicial, producto_final, status, sucursal):
    print(f"Consulta de trazabilidad por producto de: {fecha_inicial} a: {fecha_final}, del producto: {producto_inicial} al {producto_final}, con status {status} y de la sucursal {sucursal}")

    # Si el status es "Todos", entonces buscamos tanto 'A' (Activo) como 'I' (Inactivo)
    if status == 'Activo':
        status_filter = "= 'A'"
    elif status == 'Inactivo':
        status_filter = "= 'I'"
    elif status == 'Todos':
        status_filter = "IN ('A', 'I')"
        
    with connection.cursor() as cursor:
        # Construcción dinámica de la consulta SQL
        query = f"""
            SELECT
                Orden.CLAVE AS clave_producto,
                Orden.Producto AS producto,
                CASE 
                    WHEN Orden.OStatus = 'A' THEN 'Activo'
                    WHEN Orden.OStatus = 'I' THEN 'Inactivo'
                    ELSE '-'
                END AS status,
                Orden.OOrden AS orden,
                Orden.OFecha AS orden_fecha,
                Orden.OFolio AS numero_folio,
                Orden.OCantidad AS cantidad,
                Orden.PFecha AS partes_fecha,
                Parte.Folio AS partes_folio,
                Termina.Folio AS termina_folio,
                Termina.Cantidad AS termina_cantidad,
                Orden.DiferenciaDias AS diferencia_de_dias,
                Orden.OCantidad - Termina.Cantidad AS diferencia_de_cantidad
            FROM (
                SELECT 
                    KDPORD.C3 AS CLAVE,
                    KDII.C2 AS Producto,
                    KDPORD.C2 AS OStatus,
                    KDPORD.C1 AS OOrden,
                    FORMAT(KDPORD.C6, 'd', 'en-gb') AS OFecha,
                    KDPORD.C24 AS OFolio,
                    KDPORD.C9 AS OCantidad,
                    FORMAT(KDM1.C9, 'd', 'en-gb') AS PFecha,
                    DATEDIFF(day, KDPORD.C6, KDM1.C9) AS DiferenciaDias
                FROM KL2020.dbo.KDPORD 
                INNER JOIN KL2020.dbo.KDII ON KDPORD.C3 = KDII.C1
                INNER JOIN KL2020.dbo.KDM1 ON KDPORD.C1 = KDM1.C11
                WHERE KDPORD.C19 = %s  /*Sucursal*/
                AND KDPORD.C6 >= %s  /*Fecha inicial*/
                AND KDPORD.C6 <= %s  /*Fecha final*/
                AND KDPORD.C3 >= %s  /*Producto inicial*/
                AND KDPORD.C3 <= %s  /*Producto final*/
                AND KDPORD.C2 {status_filter}  /*Status (A, I, o ambos)*/
            ) AS Orden
            LEFT JOIN (
                SELECT DISTINCT
                    KDPORD3.C1 AS OORden,
                    KDPORD3.C16 AS Folio
                FROM KL2020.dbo.KDPORD3
                WHERE C13 = 'D'
            ) AS Parte ON Orden.OOrden = Parte.OORden
            LEFT JOIN (
                SELECT DISTINCT
                    KDPORD3.C1 AS OORden,
                    KDPORD3.C16 AS Folio,
                    KDPORD3.C6 AS Cantidad
                FROM KL2020.dbo.KDPORD3
                WHERE C13 = 'A'
            ) AS Termina ON Orden.OOrden = Termina.OORden
            ORDER BY Orden.CLAVE
        """

        params = [sucursal, fecha_inicial, fecha_final, producto_inicial, producto_final]
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result

def consultaVentasEnGeneral(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta de ventas en general desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}")
    
    with connection.cursor() as cursor:
        query = """
            -- SQL VENTA
                SELECT 
                    dbo.KDIJ.C1 AS SUC,
                    CASE 
                        WHEN dbo.KDUV.C22 = 1 THEN 'Autoservicio'
                        WHEN dbo.KDUV.C22 = 2 THEN 'Norte'
                        WHEN dbo.KDUV.C22 = 3 THEN 'Sur'
                        WHEN dbo.KDUV.C22 = 4 THEN 'Vent. Especiales'
                        WHEN dbo.KDUV.C22 = 5 THEN 'Cadenas'
                        WHEN dbo.KDUV.C22 = 6 THEN 'Centro'
                        ELSE 'sin asignar a Vallejo'
                    END AS NOM,
                    CONCAT('1 - ', dbo.KDMS.C2) AS ZONA,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_ENE,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_FEB,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_MAR,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_ABR,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_MAY,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_JUN,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_JUL,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_AGO,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_SEP,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_OCT,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_NOV,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_DIC
                FROM 
                    dbo.KDIJ
                    INNER JOIN dbo.KDII ON dbo.KDIJ.C3 = dbo.KDII.C1
                    INNER JOIN dbo.KDUD ON dbo.KDIJ.C15 = dbo.KDUD.C2
                    INNER JOIN dbo.KDUV ON dbo.KDIJ.C16 = dbo.KDUV.C2
                    INNER JOIN dbo.KDMS ON KDIJ.C1 = KDMS.C1
                WHERE 
                    dbo.KDII.C1 >= %s
                    AND dbo.KDII.C1 <= %s
                    AND dbo.KDIJ.C10 >= %s
                    AND dbo.KDIJ.C10 <= %s
                    AND dbo.KDIJ.C1 IN ('02')
                    AND dbo.KDUV.C22 BETWEEN '1' AND '6'
                    AND dbo.KDUD.C2 BETWEEN %s AND %s
                    AND dbo.KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    AND dbo.KDIJ.C4 = 'U'
                    AND dbo.KDIJ.C5 = 'D'
                    AND dbo.KDIJ.C6 IN ('5','45')
                GROUP BY 
                    dbo.KDIJ.C1,
                    dbo.KDUV.C22,
                    dbo.KDMS.C2

                UNION

                SELECT 
                    dbo.KDIJ.C1 AS SUC, 
                    dbo.KDMS.C2 AS NOM,
                    CASE 
                        WHEN dbo.KDIJ.C1 IN ('04','15','16','17') THEN '2 - Norte'
                        WHEN dbo.KDIJ.C1 IN ('05','08','10','19') THEN '4 - Centro'
                        WHEN dbo.KDIJ.C1 IN ('03','09','12','14','06','20') THEN '3 - Pacifico'
                        WHEN dbo.KDIJ.C1 IN ('07','11','13','18') THEN '5 - Sureste'
                        ELSE 'Sin zona'
                    END AS ZONA,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_ENE,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_FEB,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_MAR,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_ABR,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_MAY,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_JUN,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_JUL,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_AGO,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_SEP,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_OCT,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_NOV,
                    SUM(CASE WHEN dbo.KDIJ.C10 >= %s AND dbo.KDIJ.C10 <= %s THEN dbo.KDIJ.C14 END) AS VENTA_DIC
                FROM 
                    dbo.KDIJ
                    INNER JOIN dbo.KDII ON dbo.KDIJ.C3 = dbo.KDII.C1
                    INNER JOIN dbo.KDUD ON dbo.KDIJ.C15 = dbo.KDUD.C2
                    INNER JOIN dbo.KDMS ON KDIJ.C1 = KDMS.C1
                WHERE 
                    dbo.KDII.C1 >= %s
                    AND dbo.KDII.C1 <= %s
                    AND dbo.KDIJ.C10 >= %s
                    AND dbo.KDIJ.C10 <= %s
                    AND dbo.KDIJ.C1 IN ('03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20')
                    AND dbo.KDUD.C2 BETWEEN %s AND %s
                    AND dbo.KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                    AND dbo.KDIJ.C4 = 'U'
                    AND dbo.KDIJ.C5 = 'D'
                    AND dbo.KDIJ.C6 IN ('5','45')
                GROUP BY 
                    dbo.KDIJ.C1,
                    dbo.KDMS.C2

                ORDER BY 
                    3, 1;
        """

        # Lista de parámetros para la consulta SQL
        params = [
            # Parámetros de fechas (12 pares para los meses y 6 pares adicionales para el UNION)
            fecha_inicial.replace(day=1), fecha_inicial.replace(day=31),  # Enero
            fecha_inicial.replace(day=1) + timedelta(days=31), fecha_inicial.replace(day=31) + timedelta(days=31),  # Febrero
            fecha_inicial.replace(day=1) + timedelta(days=62), fecha_inicial.replace(day=31) + timedelta(days=62),  # Marzo
            fecha_inicial.replace(day=1) + timedelta(days=93), fecha_inicial.replace(day=31) + timedelta(days=93),  # Abril
            fecha_inicial.replace(day=1) + timedelta(days=124), fecha_inicial.replace(day=31) + timedelta(days=124),  # Mayo
            fecha_inicial.replace(day=1) + timedelta(days=155), fecha_inicial.replace(day=31) + timedelta(days=155),  # Junio
            fecha_inicial.replace(day=1) + timedelta(days=186), fecha_inicial.replace(day=31) + timedelta(days=186),  # Julio
            fecha_inicial.replace(day=1) + timedelta(days=217), fecha_inicial.replace(day=31) + timedelta(days=217),  # Agosto
            fecha_inicial.replace(day=1) + timedelta(days=248), fecha_inicial.replace(day=31) + timedelta(days=248),  # Septiembre
            fecha_inicial.replace(day=1) + timedelta(days=279), fecha_inicial.replace(day=31) + timedelta(days=279),  # Octubre
            fecha_inicial.replace(day=1) + timedelta(days=310), fecha_inicial.replace(day=31) + timedelta(days=310),  # Noviembre
            fecha_inicial.replace(day=1) + timedelta(days=341), fecha_inicial.replace(day=31) + timedelta(days=341),  # Diciembre

            # Parámetros de cliente, producto, y rango de fechas
            cliente_inicial, cliente_final,
            fecha_inicial, fecha_final,
            producto_inicial, producto_final
        ]

        for param in params:
            print('El parametro es: ', param, type(param))

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result
