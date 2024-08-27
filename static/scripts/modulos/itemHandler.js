import { cargarData } from "./renderModal.js";
import { fullItemsArray } from "./main.js";

// Función genérica para manejar los datos
function handleData(data, datosCompletos, dataType) {
    fullItemsArray.length = 0;
    fullItemsArray.push(...data[datosCompletos]);

    cargarData(data, datosCompletos, dataType);
}

// Objeto de handlers optimizado
export const handlers = {
    'cliente_inicial': (data, dataType) => handleData(data, 'clientes', dataType),
    'cliente_final': (data, dataType) => handleData(data, 'clientes', dataType),
    'producto_inicial': (data, dataType) => handleData(data, 'productos', dataType),
    'producto_final': (data, dataType) => handleData(data, 'productos', dataType),
    'sucursal_inicial': (data, dataType) => handleData(data, 'sucursales', dataType),
    'sucursal_final': (data, dataType) => handleData(data, 'sucursales', dataType),
    'sucursal': (data, dataType) => handleData(data, 'sucursales', dataType),
    'vendedor_inicial': (data, dataType) => handleData(data, 'vendedores', dataType),
    'vendedor_final': (data, dataType) => handleData(data, 'vendedores', dataType),
    'linea_inicial': (data, dataType) => handleData(data, 'lineas', dataType),
    'linea_final': (data, dataType) => handleData(data, 'lineas', dataType),
    'marca_inicial': (data, dataType) => handleData(data, 'lineas', dataType),
    'marca_final': (data, dataType) => handleData(data, 'lineas', dataType),
    'familia_inicial': (data, dataType) => handleData(data, 'familias', dataType),
    'familia_final': (data, dataType) => handleData(data, 'familias', dataType),
    'familia': (data, dataType) => handleData(data, 'familias', dataType),
    'grupoCorporativo_inicial': (data, dataType) => handleData(data, 'gruposCorporativos', dataType),
    'grupoCorporativo_final': (data, dataType) => handleData(data, 'gruposCorporativos', dataType),
    'grupoCorporativo': (data, dataType) => handleData(data, 'gruposCorporativos', dataType),
    'segmento_inicial': (data, dataType) => handleData(data, 'segmentos', dataType),
    'segmento_final': (data, dataType) => handleData(data, 'segmentos', dataType),
    'status': (data, dataType) => handleData(data, 'estatus', dataType),
    'zona': (data, dataType) => handleData(data, 'zonas', dataType),
    'region': (data, dataType) => handleData(data, 'regiones', dataType),
};
