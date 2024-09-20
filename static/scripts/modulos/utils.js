//utils.js
import { parametrosReporte } from './config.js';


export function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function transformHeader(header) {
    return header.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
}

export function formatNumber(value, isCurrency = false, key = '') {
    // Lista de claves que no deben ser formateadas
    const keysToExcludeFromFormatting = ['clave_producto', 'descripcion_producto', 'producto','sucursal', 
                                            'clave', 'clave_sucursal', 'numero_tipo_documento', 'grupo_movimiento',
                                            'detalles_tipo_documento', 'almacen_correspondiente', 'moneda','zona',
                                            'orden', 'orden_fecha', 'numero_folio', 'partes_folio', 'partes_fecha',
                                            'termina_folio', 'nombre,', 'zona', 'nombre_producto','UPC','linea'];

    // Si la clave está en la lista de exclusión, devolver el valor sin cambios
    if (keysToExcludeFromFormatting.includes(key)) {
        return value;
    }

    if (value == null || value === '') {
        return ' - ';
    }

    // Convertir el valor a una cadena si no lo es
    let valueStr = value.toString();

    // Si el valor es una cadena y comienza con $, limpiarlo
    if (valueStr.startsWith('$')) {
        isCurrency = true;
        valueStr = valueStr.replace(/^\$/, ''); // Elimina el símbolo $
    }
    valueStr = valueStr.replace(/,/g, ''); // Elimina comas si las hay

    // Convierte el valor a número
    const numericValue = parseFloat(valueStr);

    if (isNaN(numericValue)) {
        return value; // Devuelve el valor original si no es un número válido
    }

    // Si el valor es 0, devolverlo en rojo y negrita
    if (numericValue === 0) {
        return '<span style="color: red; font-weight: bold;">0.00</span>';
    }


    // Formatear el número con o sin símbolo de moneda
    const formattedValue = numericValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

    return isCurrency ? `$${formattedValue}` : formattedValue;
}

export function errorParametros(estado) {
    if (estado) {
        // Limpiar alertas anteriores
        parametrosReporte.querySelectorAll('.alert').forEach(alert => alert.remove());
        
        // Agregar nueva alerta
        parametrosReporte.insertAdjacentHTML('beforeend', `
            <div class="alert alert-danger fade show text-center" role="alert">
                <strong>¡Oops!</strong> ¡Verifica que los parámetros estén completos!
            </div> 
        `);
    } else {
        // Limpiar alertas cuando estado es false
        parametrosReporte.querySelectorAll('.alert').forEach(alert => alert.remove());
    }
}