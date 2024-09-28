from datetime import datetime, timedelta
from django.db.models import Value, CharField,OuterRef, Subquery, Sum, FloatField, ExpressionWrapper, F, Case, When, Window, DecimalField, Q
from django.db.models.functions import Concat, Round, RowNumber, LTrim, RTrim, Coalesce
from django.db.models.expressions import CombinedExpression
from .models import *
from decimal import Decimal
from django.db import connection
from .queries_reportes.producto_con_refacturacion import * 
from .queries_reportes.venta_cliente_con_refacturacion import * 
from .queries_reportes.venta_credito_contable import * 
from .queries_reportes.clientes_por_grupo import * 
from .queries_reportes.cierre_de_mes import * 
from .queries_reportes.ventas_por_producto import * 
from .queries_reportes.ventas_familia_kg_con_refacturacion import * 
from .queries_reportes.presupuesto_vs_ventas import * 
from .queries_reportes.trazabilidad_por_producto import * 
from .queries_reportes.ventas_en_general import * 
from .queries_reportes.lista_precios_producto import * 
from .queries_reportes.ventas_por_zona_pesos import * 
from .queries_reportes.semana_80_20 import *
from .queries_reportes.clientes_consignatarios_activos import *
from .queries_reportes.informe_ventas_por_zona_kilos_marca import *
from .queries_reportes.informe_ventas_por_zona_pesos_marca import *
from .queries_reportes.venta_por_zona_kilos import *
from .queries_reportes.ventas_por_familia_pesos_sin_refacturacion import *
from .queries_reportes.ventas_por_familia_kilos_sin_refacturacion import *
from .queries_reportes.tendencia_ventas import *
from .queries_reportes.tendencia_ventas_por_giro import *

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
        
    elif tipo_reporte == "Ventas por Zonas Kilos (Sin Refacturación)":
        resultados.extend(consultaVentasPorZonaKilos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final))
        
    elif tipo_reporte == "Análisis Semanal de los Principales Contribuyentes a través del Principio 80/20":
        resultados.extend(consultaSemana8020(fecha_inicial, fecha_final, sucursal))
        
    elif tipo_reporte == "Clientes y Consignatarios Activos":
        resultados.extend(consultaConsignatariosClientesActivos(fecha_inicial, fecha_final))
        
    elif tipo_reporte == "Informe de Ventas por Zonas en Pesos":
        resultados.extend(consultaVentasPorZonaPesosMarca(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, marca_inicial, marca_final))
    
    elif tipo_reporte == "Informe de Ventas por Zonas en Kilogramos y por Marca (Sin Refacturación)":
        resultados.extend(consultaVentasPorZonaKilosMarca(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, marca_inicial, marca_final))
    
    elif tipo_reporte == "Ventas por Familia en Pesos (Sin Refacturación)":
        resultados.extend(consutlaVentasPorFamiliaPesosSinRefacturacion(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, producto_inicial, producto_final, familia_inicial, familia_final))
    
    elif tipo_reporte == "Ventas por Familia en Kilos (Sin Refacturación)":
        resultados.extend(consutlaVentasPorFamiliaKilosSinRefacturacion(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, producto_inicial, producto_final, familia_inicial, familia_final))
        
    elif tipo_reporte == "Tendencia de las Ventas":
        resultados.extend(consultaTendenciaVentas(fecha_inicial, fecha_final))
        
    elif tipo_reporte == "Tendencia de las Ventas por Sector (2020)":
        resultados.extend(consultaTendenciaVentasPorGiro(fecha_inicial, fecha_final))
        
        
        
    
    return resultados
    
def parse_date(date_str):
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    except ValueError:
        return None