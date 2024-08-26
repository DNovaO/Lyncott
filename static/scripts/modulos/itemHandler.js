import { cargarData } from "./renderModal.js";
import { fullItemsArray } from "./main.js";

// Función genérica para manejar los datos
function handleData(data, key, paginado, dataType) {
    fullItemsArray.length = 0;
    fullItemsArray.push(...data[key]);
    cargarData(data, paginado, dataType);
}

// Objeto de handlers optimizado
export const handlers = {
    'cliente_inicial': (data, dataType) => handleData(data, 'clientes', 'clientesPaginados', dataType),
    'cliente_final': (data, dataType) => handleData(data, 'clientes', 'clientesPaginados', dataType),
    'producto_inicial': (data, dataType) => handleData(data, 'productos', 'productosPaginados', dataType),
    'producto_final': (data, dataType) => handleData(data, 'productos', 'productosPaginados', dataType),
    'sucursal_inicial': (data, dataType) => handleData(data, 'sucursales', 'sucursalesPaginados', dataType),
    'sucursal_final': (data, dataType) => handleData(data, 'sucursales', 'sucursalesPaginados', dataType),
    'sucursal': (data, dataType) => handleData(data, 'sucursales', 'sucursalesPaginados', dataType),
    'vendedor_inicial': (data, dataType) => handleData(data, 'vendedores', 'vendedoresPaginados', dataType),
    'vendedor_final': (data, dataType) => handleData(data, 'vendedores', 'vendedoresPaginados', dataType),
    'linea_inicial': (data, dataType) => handleData(data, 'lineas', 'lineasPaginados', dataType),
    'linea_final': (data, dataType) => handleData(data, 'lineas', 'lineasPaginados', dataType),
    'marca_inicial': (data, dataType) => handleData(data, 'lineas', 'lineasPaginados', dataType),
    'marca_final': (data, dataType) => handleData(data, 'lineas', 'lineasPaginados', dataType),
    'familia_inicial': (data, dataType) => handleData(data, 'familias', 'familiasPaginados', dataType),
    'familia_final': (data, dataType) => handleData(data, 'familias', 'familiasPaginados', dataType),
    'familia': (data, dataType) => handleData(data, 'familias', 'familiasPaginados', dataType),
    'grupoCorporativo_inicial': (data, dataType) => handleData(data, 'gruposCorporativos', 'gruposCorporativosPaginados', dataType),
    'grupoCorporativo_final': (data, dataType) => handleData(data, 'gruposCorporativos', 'gruposCorporativosPaginados', dataType),
    'grupoCorporativo': (data, dataType) => handleData(data, 'gruposCorporativos', 'gruposCorporativosPaginados', dataType),
    'segmento_inicial': (data, dataType) => handleData(data, 'segmentos', 'segmentosPaginados', dataType),
    'segmento_final': (data, dataType) => handleData(data, 'segmentos', 'segmentosPaginados', dataType),
    'status': (data, dataType) => handleData(data, 'estatus', 'estatusPaginados', dataType),
    'zona': (data, dataType) => handleData(data, 'zonas', 'zonasPaginados', dataType),
    'region': (data, dataType) => handleData(data, 'regiones', 'regionesPaginados', dataType),
};
