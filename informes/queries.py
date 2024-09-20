from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from .models import *
from decimal import Decimal
from django.db import connection
from .fechas import obtener_rango_fechas

def clasificarParametros(parametrosSeleccionados, tipo_reporte):
    filtros = {}
    
    for key, value in parametrosSeleccionados.items():
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            for item in value:
                key_value = item[list(item.keys())[0]].strip().split('-')[0].strip()  # Obtiene el valor antes del "-"
                if key in ('fecha_inicial', 'fecha_final', 'cliente_inicial', 'cliente_final', 'producto_inicial', 'producto_final', 'sucursal', 'sucursal_inicial', 'sucursal_final', 'vendedor_inicial', 'vendedor_final', 'linea_inicial', 'linea_final', 'familia', 'familia_inicial', 'familia_final', 'marca_inicial', 'marca_final', 'grupoCorporativo', 'grupoCorporativo_inicial', 'grupoCorporativo_final', 'segmento_inicial', 'segmento_final', 'status', 'zona', 'grupo', 'region', 'year'):
                    filtros[key] = key_value
                    
                print(f"Clave: {key}, Valor: {key_value}")
        else:
            if isinstance(value, list) and len(value) > 0:
                value = value[0]
                if isinstance(value, dict):
                    value = value[list(value.keys())[0]].strip().split('-')[0].strip()  # Obtiene el valor antes del "-"
                    
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

    elif tipo_reporte == "Lista de Precios por Producto y por Zonas":
        resultados.extend(consultaListaPreciosProducto(producto_inicial, producto_final))
        
    elif tipo_reporte == "Ventas por Zonas Pesos (Sin Refacturación)":
        resultados.extend(consultaVentasPorZonasPesos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final))
    
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
                WHERE KDPORD.C19 = '{sucursal}'  /*Sucursal*/
                AND KDPORD.C6 >= '{fecha_inicial}'  /*Fecha inicial*/
                AND KDPORD.C6 <= '{fecha_final}'  /*Fecha final*/
                AND KDPORD.C3 >= '{producto_inicial}'  /*Producto inicial*/
                AND KDPORD.C3 <= '{producto_final}'  /*Producto final*/
                AND KDPORD.C2 {status_filter} /*Status (A, I, o ambos)*/
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

        # params = [sucursal, fecha_inicial, fecha_final, producto_inicial, producto_final]
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        print(query)

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)

    return result

def consultaVentasEnGeneral(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta de ventas en general desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}")

    # Obtener el rango de fechas por mes
    rangos_fechas = obtener_rango_fechas()

    with connection.cursor() as cursor:
        query = """
           SELECT 
                KDIJ.C1 AS sucursal,
                CASE 
                    WHEN KDUV.C22 = 1 THEN 'Autoservicio'
                    WHEN KDUV.C22 = 2 THEN 'Norte'
                    WHEN KDUV.C22 = 3 THEN 'Sur'
                    WHEN KDUV.C22 = 4 THEN 'Vent. Especiales'
                    WHEN KDUV.C22 = 5 THEN 'Cadenas'
                    WHEN KDUV.C22 = 6 THEN 'Centro'
                    ELSE 'sin asignar a Vallejo'
                END AS nombre,
                CONCAT('1 - ', KDMS.C2) AS zona,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_ENE,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_FEB,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_MAR,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_ABR,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_MAY,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_JUN,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_JUL,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_AGO,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_SEP,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_OCT,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_NOV,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_DIC
            FROM 
                KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                INNER JOIN KDUV ON KDIJ.C16 = KDUV.C2
                INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1
            WHERE 
                KDII.C1 BETWEEN %s AND %s
                AND KDIJ.C10 BETWEEN %s AND %s
                AND KDIJ.C1 = '02'
                AND KDUV.C22 BETWEEN '1' AND '6'
                AND KDUD.C2 BETWEEN %s AND %s
                AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                AND KDIJ.C4 = 'U'
                AND KDIJ.C5 = 'D'
                AND KDIJ.C6 IN ('5','45')
            GROUP BY 
                KDIJ.C1,
                KDUV.C22,
                KDMS.C2

            UNION

            SELECT 
                KDIJ.C1 AS sucursal, 
                KDMS.C2 AS nombre,
                CASE 
                    WHEN KDIJ.C1 IN ('04','15','16','17') THEN '2 - Norte'
                    WHEN KDIJ.C1 IN ('05','08','10','19') THEN '4 - Centro'
                    WHEN KDIJ.C1 IN ('03','09','12','14','06','20') THEN '3 - Pacifico'
                    WHEN KDIJ.C1 IN ('07','11','13','18') THEN '5 - Sureste'
                    ELSE 'Sin zona'
                END AS zona,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_ENE,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_FEB,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_MAR,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_ABR,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_MAY,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_JUN,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_JUL,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_AGO,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_SEP,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_OCT,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_NOV,
                    SUM(CASE WHEN KDIJ.C10 BETWEEN %s AND %s THEN KDIJ.C14 ELSE 0 END) AS VENTA_DIC
            FROM 
                KDIJ
                INNER JOIN KDII ON KDIJ.C3 = KDII.C1
                INNER JOIN KDUD ON KDIJ.C15 = KDUD.C2
                INNER JOIN KDMS ON KDIJ.C1 = KDMS.C1
            WHERE 
                KDII.C1 BETWEEN %s AND %s
                AND KDIJ.C10 BETWEEN %s AND %s
                AND KDIJ.C1 IN ('03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20')
                AND KDUD.C2 BETWEEN %s AND %s
                AND KDIJ.C16 NOT IN ('902','903','904','905','906','907','908','909','910','911','912','913','914','915','916','917','918','919','920','921','922','923','924')
                AND KDIJ.C4 = 'U'
                AND KDIJ.C5 = 'D'
                AND KDIJ.C6 IN ('5','45')
            GROUP BY 
                KDIJ.C1,
                KDMS.C2

            ORDER BY 
                3, 1;

        """

        # Lista de parámetros con los rangos de fechas mensuales
        params = [
            rangos_fechas['january_inicial'], rangos_fechas['january_final'],
            rangos_fechas['february_inicial'], rangos_fechas['february_final'],
            rangos_fechas['march_inicial'], rangos_fechas['march_final'],
            rangos_fechas['april_inicial'], rangos_fechas['april_final'],
            rangos_fechas['may_inicial'], rangos_fechas['may_final'],
            rangos_fechas['june_inicial'], rangos_fechas['june_final'],
            rangos_fechas['july_inicial'], rangos_fechas['july_final'],
            rangos_fechas['august_inicial'], rangos_fechas['august_final'],
            rangos_fechas['september_inicial'], rangos_fechas['september_final'],
            rangos_fechas['october_inicial'], rangos_fechas['october_final'],
            rangos_fechas['november_inicial'], rangos_fechas['november_final'],
            rangos_fechas['december_inicial'], rangos_fechas['december_final'],
            producto_inicial, producto_final,
            fecha_inicial, fecha_final,
            cliente_inicial, cliente_final,

            rangos_fechas['january_inicial'], rangos_fechas['january_final'],
            rangos_fechas['february_inicial'], rangos_fechas['february_final'],
            rangos_fechas['march_inicial'], rangos_fechas['march_final'],
            rangos_fechas['april_inicial'], rangos_fechas['april_final'],
            rangos_fechas['may_inicial'], rangos_fechas['may_final'],
            rangos_fechas['june_inicial'], rangos_fechas['june_final'],
            rangos_fechas['july_inicial'], rangos_fechas['july_final'],
            rangos_fechas['august_inicial'], rangos_fechas['august_final'],
            rangos_fechas['september_inicial'], rangos_fechas['september_final'],
            rangos_fechas['october_inicial'], rangos_fechas['october_final'],
            rangos_fechas['november_inicial'], rangos_fechas['november_final'],
            rangos_fechas['december_inicial'], rangos_fechas['december_final'],
            producto_inicial, producto_final,
            fecha_inicial, fecha_final,
            cliente_inicial, cliente_final,
        ]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        
    return result

def consultaListaPreciosProducto(producto_inicial, producto_final):
    print(f"Consulta de lista de precios por producto desde {producto_inicial} hasta {producto_final}")

    with connection.cursor() as cursor:
        query = """
            SELECT 
                KDII.C1 	AS clave_producto,
                KDII.C2 	AS nombre_producto,
                KDII.C7 	AS UPC,
                KDIG.C2 	AS linea,
                KDII.C12 AS unidad,
                KDII.C13 AS factor_conversion,
                KDII.C14 AS A_centro,
                KDII.C15 AS B_peninsula,
                KDII.C16 AS C_pacifico,
                KDII.C17 AS D_chihuahua
            FROM KDII
                INNER JOIN KDIG ON KDIG.C1 = KDII.C3
            WHERE KDII.C4 ='PT'
                AND  KDII.C1 >= %s
                AND  KDII.C1 <= %s
        """

        params = [producto_inicial, producto_final]

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
        
    with connection.cursor() as cursor:
        query = """
          
        """

        params = [ ]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        
    return result

def consultaVentaPorCliente(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta de ventas por cliente desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}")
        
    with connection.cursor() as cursor:
        query = """
          
        """

        params = [ ]

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for row in result:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        
    return result

def consultaVentasPorZonasPesos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta de ventas por zonas en pesos desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}")
    
    with connection.cursor() as cursor:
        query = """
           SELECT 
                ISNULL(ANTERIOR.ZONA, ACTUAL.ZONA) AS ZONA,
                ISNULL(ANTERIOR.ZONA_ORDER, ACTUAL.ZONA_ORDER) AS ZONA_ORDER,
                ISNULL(ANTERIOR.CLAVE, ACTUAL.CLAVE) AS CLAVE,
                ISNULL(ANTERIOR.SUC, ACTUAL.SUC) AS SUC,
                SUM(ISNULL(ANTERIOR.VENTA, 0)) AS VENTA_ANTERIOR,
                SUM(ISNULL(ACTUAL.VENTA, 0)) AS VENTA_ACTUAL,
                SUM(ISNULL(ACTUAL.VENTA, 0)) - SUM(ISNULL(ANTERIOR.VENTA, 0)) AS DIFERENCIA,
                CASE 
                    WHEN SUM(ISNULL(ANTERIOR.VENTA, 0)) = 0 THEN 
                        CASE 
                            WHEN SUM(ISNULL(ACTUAL.VENTA, 0)) = 0 THEN 0
                            ELSE 100
                        END 
                    ELSE
                        CASE 
                            WHEN SUM(ISNULL(ACTUAL.VENTA, 0)) = 0 THEN -100
                            ELSE (SUM(ISNULL(ACTUAL.VENTA, 0)) / SUM(ISNULL(ANTERIOR.VENTA, 0)) * 100) - 100
                        END
                END AS DIFERENCIA_EN_PORCENTAJE,
                ISNULL(
                    SUM(ISNULL(ACTUAL.VENTA, 0)) / KL2020.dbo.f_DifDias(%s, %s) * KL2020.dbo.f_DifDiasTotales(%s, %s), 
                    0
                ) AS ESTIMADO_MES,
                CASE 
                    WHEN SUM(ISNULL(ACTUAL.KILOS, 0)) = 0 THEN 0
                    ELSE SUM(ISNULL(ACTUAL.VENTA, 0)) / SUM(ISNULL(ACTUAL.KILOS, 0)) 
                END AS PROMEDIO,
                SUM(ISNULL(ACTUAL.KILOS, 0)) AS VENTAS_anioAct_EN_KILOS
                FROM (
                -- Subconsulta ANTERIOR
                SELECT
                    ...
                WHERE
                    KL2020.dbo.KDII.C1 >= %s /*PInicial*/
                    AND KL2020.dbo.KDII.C1 <= %s /*PFinal*/
                    AND KL2020.dbo.KDIJ.C10 >=  %s /*FInicial*/
                    AND KL2020.dbo.KDIJ.C10 <= %s /*FFinal*/
                    AND KL2020.dbo.KDUD.C2 >= %s /*CInicial*/
                    AND KL2020.dbo.KDUD.C2 <= %s /*CFinal*/
                    ...
                ) AS ANTERIOR
                FULL JOIN (
                -- Subconsulta ACTUAL
                SELECT
                    ...
                WHERE
                    KL2020.dbo.KDII.C1 >= %s /*PInicial*/
                    AND KL2020.dbo.KDII.C1 <= %s /*PFinal*/
                    AND KL2020.dbo.KDIJ.C10 >= %s /*FInicial*/
                    AND KL2020.dbo.KDIJ.C10 <= %s /*FFinal*/
                    AND KL2020.dbo.KDUD.C2 >= %s /*CInicial*/
                    AND KL2020.dbo.KDUD.C2 <= %s /*CFinal*/
                    ...
                ) AS ACTUAL 
                ON ANTERIOR.SUC = ACTUAL.SUC
                GROUP BY 
                ISNULL(ANTERIOR.ZONA, ACTUAL.ZONA),
                ISNULL(ANTERIOR.ZONA_ORDER, ACTUAL.ZONA_ORDER),
                ISNULL(ANTERIOR.CLAVE, ACTUAL.CLAVE),
                ISNULL(ANTERIOR.SUC, ACTUAL.SUC)
                ORDER BY 
                ISNULL(ANTERIOR.ZONA_ORDER, ACTUAL.ZONA_ORDER),
                ISNULL(ANTERIOR.ZONA, ACTUAL.ZONA);
        """
    
        # Lista de parámetros en el orden que aparecen en la consulta
        params = [
            fecha_inicial, fecha_final, fecha_inicial, fecha_final, producto_inicial, producto_final,
            fecha_inicial, fecha_final,
            cliente_inicial, cliente_final,
            
            producto_inicial, producto_final,
            fecha_inicial, fecha_final,
            cliente_inicial, cliente_final,
        ]
    
        try:
            # Depuración: Imprimir la consulta y los parámetros
            print("Consulta SQL:", query)
            print("Parámetros:", params)
    
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
            for row in result:
                for key, value in row.items():
                    if isinstance(value, Decimal):
                        row[key] = float(value)
    
            return result
        except Exception as e:
            print(f"Error ejecutando la consulta: {e}")
            return {"error": str(e)}
