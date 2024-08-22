from datetime import datetime
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim
from django.db.models.expressions import CombinedExpression
from .models import *

def clasificarParametros(parametrosSeleccionados, tipo_reporte):
    filtros = {}
    
    for key, value in parametrosSeleccionados.items():
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            for item in value:
                key_value = item[list(item.keys())[0]].strip()
                if key in ('fecha_inicial', 'fecha_final', 'cliente_inicial', 'cliente_final', 'producto_inicial', 'producto_final', 'sucursal', 'sucursal_inicial', 'sucursal_final', 'vendedor_inicial', 'vendedor_final', 'linea_inicial', 'linea_final', 'familia', 'familia_inicial', 'familia_final', 'marca_inicial', 'marca_final', 'grupoCorporativo', 'grupoCorporativo_inicial', 'grupoCorporativo_final', 'segmento_inicial', 'segmento_final', 'status', 'zona', 'grupo', 'region'):
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

    fecha_inicial = parse_date(fecha_inicial_str)
    fecha_final = parse_date(fecha_final_str)
    
    resultados = []
                        
    if tipo_reporte == "Por Producto (con Refacturación)":
        resultados.extend(consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final))
    
    elif tipo_reporte == "Por Tipo de Cliente (con Refacturación)":
        resultados.extend(consultaVentarPorCliente(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final))
    
    elif tipo_reporte == "Por Familia en Kilos (con Refacturación)":
        resultados.extend(consultaVentarPorFamiliaEnKilos(fecha_inicial, fecha_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final, familia_inicial, familia_final))
   
    elif tipo_reporte == "Credito Contable (con Refacturación)":
        resultados.extend(consultaVentaPorCreditoContable(fecha_inicial, fecha_final, cliente_inicial, cliente_final))
        
    elif tipo_reporte == "Clientes por Grupos":
        resultados.extend(consultaClientesPorGrupo(grupoCorporativo_inicial, grupoCorporativo_final))
    
    return resultados
    
def parse_date(date_str):
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    except ValueError:
        return None

def consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final):
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
    # kdud.clave_cliente -> c2 que es igual kdm1.clave_cliente -> c10
    # kdud.nombre_cliente -> c3
    # kdud.clave_corporativo -> c66
    
    #kdcorpo.clave_corporativo -> c1 que es = a kdud.clave_corporativo -> c66
    #kdcorpo.descripcion_corporativo -> c2
    
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
    
def consultaVentaPorCreditoContable(fecha_inicial, fecha_final, cliente_inicial, cliente_final):
    print(f"Consulta de ventas por crédito contable desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial}, cliente final: {cliente_final}")

  # Consulta principal con agregaciones
    queryVentaPorCreditoContable = Kdm1.objects.filter(
        clave_cliente__gte=cliente_inicial,
        clave_cliente__lte=cliente_final,
        fecha__gte=fecha_inicial,
        fecha__lte=fecha_final,
        genero='U',
        naturaleza='D',
        grupo_movimiento__in=['5', '45'],
        numero_tipo_documento__in=['2', '4', '6', '19', '22', '26', '1', '3', '5', '18', '21', '25']
    ).values(
        'sucursal'
    ).annotate(
        contado=Sum(Case(
            When(numero_tipo_documento__in=['2', '4', '6', '19', '22', '26'], then=F('importe') - F('ieps_retencion_isr')),
            default=0,
            output_field=FloatField()
        )),
        credito=Sum(Case(
            When(numero_tipo_documento__in=['1', '3', '5', '18', '21', '25'], then=F('importe') - F('ieps_retencion_isr')),
            default=0,
            output_field=FloatField()
        )),
        
        total=ExpressionWrapper(F('contado') + F('credito'), output_field=FloatField()),
        
        porcentaje_contado=ExpressionWrapper(
            F('contado') / Case(
                When(total=0, then=Value(1)),
                default=F('total'),
                output_field=FloatField()
            ) * 100,
            output_field=FloatField()
        ),
        
        porcentaje_credito=ExpressionWrapper(
            F('credito') / Case(
                When(total=0, then=Value(1)),
                default=F('total'),
                output_field=FloatField()
            ) * 100,
            output_field=FloatField()
        )
    ).values(
        'sucursal',
        'contado',
        'porcentaje_contado',
        'credito',
        'porcentaje_credito',
        'total',
    )


    # queryVentaPorCreditoContable = subquery_kdm1.annotate(

    #     sucursal_nombre=Case(
    #         When(sucursal_anotada='1', then=Value('1&nbsp;-&nbsp;Autoservicio')),
    #         When(sucursal_anotada='2', then=Value('2&nbsp;-&nbsp;Norte')),
    #         When(sucursal_anotada='3', then=Value('3&nbsp;-&nbsp;Sur')),
    #         When(sucursal_anotada='4', then=Value('4&nbsp;-&nbsp;Vent. Especiales')),
    #         When(sucursal_anotada='5', then=Value('5&nbsp;-&nbsp;Cadenas')),
    #         When(sucursal_anotada='6', then=Value('6&nbsp;-&nbsp;Centro')),
    #         output_field=CharField()
    #     ),

    #     total=F('contado') + F('credito'),
        
    #     porcentaje_contado=ExpressionWrapper(
    #         F('contado') / Case(
    #             When(total=0, then=Value(1)),
    #             default=F('total'),
    #             output_field=FloatField()
    #         ) * 100,
    #         output_field=FloatField()
    #     ),
        
    #     porcentaje_credito=ExpressionWrapper(
    #         F('credito') / Case(
    #             When(total=0, then=Value(1)),
    #             default=F('total'),
    #             output_field=FloatField()
    #         ) * 100,
    #         output_field=FloatField()
    #     ),
    # ).values(
    #     'sucursal_nombre',
    #     'contado',
    #     'porcentaje_contado',
    #     'credito',
    #     'porcentaje_credito',
    #     'total' 
    # )
    
    return list(queryVentaPorCreditoContable)

def consultaVentarPorCliente(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final):
    print(f"Consulta de ventas por cliente desde {fecha_inicial} hasta {fecha_final}, cliente inicial: {cliente_inicial} y cliente final: {cliente_final}, producto inicial: {producto_inicial} y producto final: {producto_final}")

def consultaVentarPorFamiliaEnKilos(fecha_inicial, fecha_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final, familia_inicial, familia_final):
    print(f"Consulta de ventas por familia en kilos desde {fecha_inicial} hasta {fecha_final}, producto inicial: {producto_inicial} y producto final: {producto_final}, sucursal inicial: {sucursal_inicial} y sucursal final: {sucursal_final}, familia inicial: {familia_inicial} y familia final: {familia_final}")
    
    
    