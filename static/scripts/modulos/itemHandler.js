import { cargarData } from "./renderModal.js";
import { fullItemsArray } from "./main.js";

export const handlers = {
    'cliente_inicial': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.clientes);
        cargarData(data, 'clientesPaginados', dataType);
    },
    'cliente_final': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.clientes);
        cargarData(data, 'clientesPaginados', dataType);
    },
    'producto_inicial': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.productos);
        cargarData(data, 'productosPaginados', dataType);
    },
    'producto_final': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.productos);
        cargarData(data, 'productosPaginados', dataType);
    },
    'sucursal_inicial': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.sucursales);
        cargarData(data, 'sucursalesPaginados', dataType);
    },
    'sucursal_final': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.sucursales);
        cargarData(data, 'sucursalesPaginados', dataType);
    },
    'sucursal': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.sucursales);
        cargarData(data, 'sucursalesPaginados', dataType);
    },
    'vendedor_inicial': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.vendedores);
        cargarData(data, 'vendedoresPaginados', dataType);
    },
    'vendedor_final': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.vendedores);
        cargarData(data, 'vendedoresPaginados', dataType);
    },
    'linea_inicial': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.lineas);
        cargarData(data, 'lineasPaginados', dataType);
    },
    'linea_final': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.lineas);
        cargarData(data, 'lineasPaginados', dataType);
    },
    'marca_inicial': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.lineas);
        cargarData(data, 'lineasPaginados', dataType);
    },
    'marca_final': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.lineas);
        cargarData(data, 'lineasPaginados', dataType);
    },
    'familia_inicial': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.familias);
        cargarData(data, 'familiasPaginados', dataType);
    },
    'familia_final': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.familias);
        cargarData(data, 'familiasPaginados', dataType);
    },
    'familia': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.familias);
        cargarData(data, 'familiasPaginados', dataType);
    },
    'grupoCorporativo_inicial': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.gruposCorporativos);
        cargarData(data, 'gruposCorporativosPaginados', dataType);
    },
    'grupoCorporativo_final': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.gruposCorporativos);
        cargarData(data, 'gruposCorporativosPaginados', dataType);
    },
    'grupoCorporativo': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.gruposCorporativos);
        cargarData(data, 'gruposCorporativosPaginados', dataType);
    },
    'segmento_inicial': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.segmentos);
        cargarData(data, 'segmentosPaginados', dataType);
    },
    'segmento_final': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.segmentos);
        cargarData(data, 'segmentosPaginados', dataType);
    },
    'status': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.estatus);
        cargarData(data, 'estatusPaginados', dataType);
    },
    'zona': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.zonas);
        cargarData(data, 'zonasPaginados', dataType);
    },
    'region': function(data, dataType) {
        fullItemsArray.length = 0;
        fullItemsArray.push(...data.regiones);
        cargarData(data, 'regionesPaginados', dataType);
    },
}; 