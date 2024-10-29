//utils.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script que contiene funciones de utilidad para el manejo de cookies, formato de números y manejo de errores.
    Permite una reutilización de código en otros scripts.
    

*/ 
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
        'termina_folio', 'nombre', 'zona', 'nombre_producto','UPC','linea',
        'Promedio_Cliente', 'Promedio_Consignatario', 'fecha', 'dia','clave_cliente', 'consignatario', 'segmentacion', 'clave_grupo_corporativo', 'clave_cliente', 'clave_consignatario', 'producto', 'No', 'id_vendedor', 'id_almacen','vendedor','id_grupo_corporativo','grupo_corporativo',
        'id_consignatario', 'consignatario', 'CP', 'colonia', 'cantidad','folio','RFC', 'UUID', 'serie','clave_vendedor','cliente', 'nombre_vendedor','numero_mes', 'zona_vendedor', 'nombre_cliente', 'descripcion'
    ];


    // Si la clave está en la lista de exclusión, devolver el valor sin cambios
    if (keysToExcludeFromFormatting.includes(key)) {
        return value;
    }

    if (value == null || value === '') {
        return ' - ';
    }

    // Convertir el valor a una cadena si no lo es
    let valueStr = value.toString().trim();

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

    // Si el valor es 0 , devolverlo en rojo y negrita
    if (numericValue === 0) {
        return '<span style="color: red; font-weight: bold;"> 0 </span>';
    }

    if(numericValue < 0){
        return '<span style="color: red; font-weight: bold;">' + numericValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '</span>';
    }


    // Formatear el número con o sin símbolo de moneda
    const formattedValue = numericValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

    return isCurrency ? `$${formattedValue}` : formattedValue;
}

export function errorParametros(estado, mensaje) {
    if (estado) {
        // Limpiar alertas anteriores
        parametrosReporte.querySelectorAll('.alert').forEach(alert => alert.remove());
        
        // Agregar nueva alerta
        parametrosReporte.insertAdjacentHTML('beforeend', `
            <div class="alert alert-danger fade show text-center" role="alert">
                <strong>¡Oops!</strong> ${mensaje || 'Ocurrió un error al procesar los parámetros.'}
            </div> 
        `);
        btnGenerarInforme.disabled = false;
    } else {
        // Limpiar alertas cuando estado es false
        parametrosReporte.querySelectorAll('.alert').forEach(alert => alert.remove());
    }
}