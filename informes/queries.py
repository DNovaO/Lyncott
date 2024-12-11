# handlers.py

# Diego Nova Olguín
# Ultima modificación: 17/10/2024

# Funcion para manejar tanto las funciones de los reportes, como el ajustar los parametros para
# un mejor manejo de los mismos en las queries correspondientes.
# retorna los resultados de la consulta.



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
from .queries_reportes.consignatarios_por_familia import *
from .queries_reportes.consignatarios_por_segmento import *
from .queries_reportes.devoluciones_por_fecha import *
from .queries_reportes.devoluciones_por_sucursal import *
from .queries_reportes.venta_por_tipo_cliente_sin_refacturacion import *
from .queries_reportes.venta_credito_contado_sin_refacturacion import *
from .queries_reportes.comparativo_precios_reales_vs_teoricos import *
from .queries_reportes.venta_sin_cargo_por_zona import *
from .queries_reportes.venta_sin_cargo import *
from .queries_reportes.avance_ventas import *
from .queries_reportes.ventas_vs_devoluciones import *
from .queries_reportes.consignatario_por_codigo_postal import *
from .queries_reportes.por_cliente import *
from .queries_reportes.folios_facturas import *
from .queries_reportes.venta_cliente_grupo_consignatario_producto import *
from .queries_reportes.analisis_ventas_vendedor import *
from .queries_reportes.venta_por_producto_por_giro import *
from .queries_reportes.venta_por_familia_por_producto import *
from .queries_reportes.venta_por_familia_por_region import *
from .queries_reportes.venta_cliente_consignatario_por_mes import *
from .queries_reportes.comparativo_ventas_producto_sin_refacturacion import *
from .queries_reportes.venta_sin_cargo_zona_mes import *
from .queries_reportes.comparativo_notas_credito_kilogramos import *
from .queries_reportes.ventas_cadena_foodservice import *
from .queries_reportes.ventas_sin_notas_de_credito_en_pesos import *
from .queries_reportes.devoluciones_por_zona import *
from .queries_reportes.devolucion_por_zona_en_kilos import *
from .queries_reportes.ventas_foodservice_KAM import *
from .queries_reportes.ventas_autoservice_KAM import *
from .queries_reportes.devoluciones_a_clientes_consignatarios_por_mes import *
from .queries_reportes.devoluciones_clientes_consignatarios_por_semana import *
from .queries_reportes.conciliacion_ventas import *

def clasificarParametros(parametrosSeleccionados, tipo_reporte):
    filtros = {}
    
    for key, value in parametrosSeleccionados.items():
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
            for item in value:
                key_value = item[list(item.keys())[0]].strip().split('-')[0].strip()  # Obtiene el valor antes del "-"
                if key in ('fecha_inicial', 'fecha_final', 'cliente_inicial', 'cliente_final', 'producto_inicial', 'producto_final', 'sucursal', 'sucursal_inicial', 'sucursal_final', 'vendedor_inicial', 'vendedor_final', 'linea_inicial', 'linea_final', 'familia', 'familia_inicial', 'familia_final', 'marca_inicial', 'marca_final', 'grupoCorporativo', 'grupoCorporativo_inicial', 'grupoCorporativo_final', 'segmento_inicial', 'segmento_final', 'status', 'zona', 'grupo', 'region', 'year','mes','documento'):
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
    mes = filtros.get('mes')
    documento = filtros.get('documento')

    fecha_inicial = parse_date(fecha_inicial_str)
    fecha_final = parse_date(fecha_final_str)

    # Mapeo de tipo de reporte a funciones y sus parámetros
    reportes = {
        "Por Producto (con Refacturación)": lambda: consultaVentasPorProductoConRefacturacion(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final),
        "Por Tipo de Cliente (con Refacturación)": lambda: consultaVentaPorCliente(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final),
        "Credito Contable (con Refacturación)": lambda: consultaVentaPorCreditoContable(fecha_inicial, fecha_final, cliente_inicial, cliente_final),
        "Clientes por Grupos": lambda: consultaClientesPorGrupo(grupoCorporativo_inicial, grupoCorporativo_final),
        "Cierre de Mes": lambda: consultaCierreDeMes(fecha_inicial, fecha_final, sucursal),
        "Por Producto": lambda: consultaVentasPorProducto(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final, familia_inicial, familia_final),
        "Por Familia en Kilos (con Refacturación)": lambda: consultaVentasPorFamiliaKgConRefacturacion(fecha_inicial, fecha_final, producto_inicial, producto_final, familia_inicial, familia_final, sucursal),
        "Comparativa de Ventas y Presupuesto por Zonas en Pesos": lambda: consultaPresupuestoVsVentas(sucursal, year),
        "Trazabilidad por Producto": lambda: consultaTrazabilidadPorProducto(fecha_inicial, fecha_final, producto_inicial, producto_final, status, sucursal),
        "Ventas en General (Pesos Sin Refacturación)": lambda: consultaVentasEnGeneral(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final),
        "Lista de Precios por Producto y por Zonas": lambda: consultaListaPreciosProducto(producto_inicial, producto_final),
        "Ventas por Zonas Pesos (Sin Refacturación)": lambda: consultaVentasPorZonasPesos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final),
        "Ventas por Zonas Kilos (Sin Refacturación)": lambda: consultaVentasPorZonaKilos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final),
        "Análisis Semanal de los Principales Contribuyentes a través del Principio 80/20": lambda: consultaSemana8020(fecha_inicial, fecha_final, sucursal),
        "Clientes y Consignatarios Activos": lambda: consultaConsignatariosClientesActivos(fecha_inicial, fecha_final),
        "Informe de Ventas por Zonas en Pesos": lambda: consultaVentasPorZonaPesosMarca(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, marca_inicial, marca_final),
        "Informe de Ventas por Zonas en Kilogramos y por Marca (Sin Refacturación)": lambda: consultaVentasPorZonaKilosMarca(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, marca_inicial, marca_final),
        "Ventas por Familia en Pesos (Sin Refacturación)": lambda: consutlaVentasPorFamiliaPesosSinRefacturacion(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, producto_inicial, producto_final, familia_inicial, familia_final),
        "Ventas por Familia en Kilos (Sin Refacturación)": lambda: consutlaVentasPorFamiliaKilosSinRefacturacion(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, producto_inicial, producto_final, familia_inicial, familia_final),
        "Tendencia de las Ventas": lambda: consultaTendenciaVentas(fecha_inicial, fecha_final),
        "Tendencia de las Ventas por Sector (2020)": lambda: consultaTendenciaVentasPorGiro(fecha_inicial, fecha_final),
        "Consignatarios por Familia": lambda: consultaConsignatariosPorFamilia(fecha_inicial, fecha_final, cliente_inicial, cliente_final, sucursal, familia_inicial, familia_final),
        "Consignatarios por Segmento": lambda: consultaConsignatariosPorSegmento(fecha_inicial, fecha_final, cliente_inicial, cliente_final, sucursal_inicial, sucursal_final),
        "Devoluciones por Fecha": lambda: consultaDevolucionesPorFecha(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, grupoCorporativo),
        "Devoluciones por Sucursal": lambda: consultaDevolucionesPorSucursal(fecha_inicial, fecha_final),
        "Devoluciones por Zona en Pesos": lambda: consultaDevolucionesPorZona(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final),
        "Ventas por Tipo de Cliente (Sin Refacturación)": lambda: consultaVentasPorTipoClienteSinRefacturacion(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final),
        "Ventas de Credito y Contado (Sin Refacturación)": lambda: consultaVentasDeCreditoContadoSinRefacturacion(fecha_inicial, fecha_final, cliente_inicial, cliente_final),
        "Comparativo Precios, Reales vs Teoricos y Venta Simulada": lambda: consultaComparativoPreciosRealesvsTeoricos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, sucursal_inicial, sucursal_inicial, grupoCorporativo_inicial, grupoCorporativo_final),
        "Ventas Sin Cargo por Zona": lambda: consultaVentaSinCargoPorZona(fecha_inicial, fecha_final),
        "Ventas Sin Cargo": lambda: consultaVentaSinCargo(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final),
        "Avance de Ventas por Vendedor": lambda: consultaAvanceVentas(fecha_inicial, fecha_final, sucursal),
        "Ventas Contra Devoluciones": lambda: consultaVentasVsDevoluciones(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, grupoCorporativo_inicial, grupoCorporativo_final),
        "Consignatarios por Código Postal": lambda: consultaConsignatarioPorCodigoPostal(fecha_inicial, fecha_final, sucursal),
        "Por Cliente": lambda: consultaPorCliente(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final),
        "Folios de Facturas": lambda: consultaFoliosFacturas(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final),
        "Ventas de Clientes por Grupo, Consignatario y Producto" : lambda: consultaVentaClienteGrupoConsignatarioProducto(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final, grupoCorporativo_inicial, grupoCorporativo_final),
        "Análisis de Ventas por Vendedor": lambda: consultaAnalisisVentasVendedor(fecha_inicial, fecha_final, producto_inicial, producto_final, cliente_inicial, cliente_final, vendedor_inicial, vendedor_final ,sucursal),
        "Ventas por Producto por Giro": lambda: consultaVentaPorProductoPorGiro(fecha_inicial, fecha_final, region),
        "Ventas por Familia por Producto": lambda: consultaVentaPorFamiliaPorProducto(fecha_inicial, fecha_final, region),
        "Ventas por Familia por Región": lambda: consultaVentaPorFamiliaPorRegion(fecha_inicial, fecha_final, region),
        "Ventas a Clientes/Consignatarios por Mes": lambda: consultaVentaPorClienteConsignatarioPorMes(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final),
        "Comparativo de Ventas por Producto (Sin Refacturación)": lambda:consultaComparativoVentasProductoSinRefacturacion(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final),
        "Ventas Sin Cargo por Zona según el Mes": lambda: consultaVentaSinCargoPorZonaMes(fecha_inicial, fecha_final),
        "Comparativa de Notas de Crédito en Kilogramos": lambda: consultaComparativoNotasCreditoKilogramos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final),
        "Ventas en Cadenas FoodService": lambda:consultaVentasCadenaFoodService(fecha_inicial, fecha_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final),
        "Ventas sin Notas de Credito en Pesos": lambda: consultaVentaSinNotaDeCreditoEnPesos(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final),
        "Ventas de Cadenas FoodService KAM": lambda: consultaVentasFoodServiceKAM(fecha_inicial, fecha_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final),
        "Ventas de Cadenas AutoService KAM": lambda: consultaVentasAutoServiceKAM(fecha_inicial, fecha_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final),
        "Devoluciones por Zona en Kilogramos": lambda: consultaDevolucionPorZonaKilos(fecha_inicial, fecha_final, sucursal_inicial, sucursal_final),
        "Devoluciones a Clientes/Consignatarios por Mes": lambda: consultaDevolucionesPorClienteConsignatarioPorMes(fecha_inicial, fecha_final, cliente_inicial, cliente_final, producto_inicial, producto_final, sucursal_inicial, sucursal_final, grupoCorporativo),
        "Devoluciones a Clientes/Consignatarios por Semana": lambda: consultaDevolucionesPorClienteConsignatarioPorSemana(producto_inicial, producto_final, sucursal_inicial, sucursal_final, cliente_inicial, cliente_final, mes, year),
        "Conciliación de Ventas": lambda: consultaConciliacionVentas(fecha_inicial, fecha_final,cliente_inicial, cliente_final, vendedor_inicial, vendedor_final, sucursal, documento),
    
    }

    # Ejecutar la consulta correspondiente
    if tipo_reporte in reportes:
        resultados = reportes[tipo_reporte]()
    else:
        resultados = []

    return resultados

def parse_date(date_str):
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    except ValueError:
        return None