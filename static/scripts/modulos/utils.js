//utils.js
import { sendDataToServer, sendParametersToServer } from './apiHandler.js';
import { fullItemsArray } from './main.js'
import { parametrosReporte, tipo_reporte } from './config.js';
import { currentPage, currentPageTable } from './main.js';

export function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

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
    const keysToExcludeFromFormatting = ['clave_producto', 'sucursal', 'clave'];

    // Si la clave está en la lista de exclusión, devolver el valor sin cambios
    if (keysToExcludeFromFormatting.includes(key)) {
        return value;
    }

    if (value == null || value === '') {
        return '';
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

// Filtra los elementos según el texto de búsqueda
export function buscador(dataType) {
    console.log(dataType);
    let input = document.getElementById("inputBusqueda");
    if (!input) {
        console.error("No se encontró el elemento de input");
        return;
    }

    let filter = input.value.trim().toLowerCase();
    
    if (filter === "") {
        sendDataToServer(dataType); // Vuelve a cargar los datos originales si el filtro está vacío
        return;
    }

    let filteredItems = fullItemsArray.filter(item => {
        for (const key in item) {
            if (Object.hasOwnProperty.call(item, key)) {
                if (typeof item[key] === 'string' && item[key].toLowerCase().includes(filter)) {
                    return true;
                }
            }
        }
        return false;
    });

    let resultList = document.getElementById("genericModalContent");
    if (resultList) {
        resultList.innerHTML = renderGeneral(filteredItems);

        // Remplazar eventos después de actualizar la lista
        resultList.querySelectorAll('.selectable-item').forEach(item => {
            item.addEventListener('click', function() {
                handleItemSelected(dataType, this);
                input.value = "";
            });
        });

    } else {
        console.error("No se encontró el elemento de lista de resultados");
    }   
}

export function resetFormulario() {
    // Restablecer texto de botones que activan los modales
    const modalButtons = document.querySelectorAll('.modal-trigger');
    modalButtons.forEach(button => {
        button.textContent = `Buscar ${button.getAttribute('data-type').replace('_', ' ')}`; // Restablecer el texto del botón
    });
    
    // Limpiar contenido y pie del modal
    modalContent.innerHTML = '';
    modalFooter.innerHTML = '';
    parametrosSeleccionados = {};
    parametrosInforme = {};

}

export function changePage(pageNumber, dataType, isTable = false) {
    if (isTable) {
        currentPageTable = pageNumber;
        sendParametersToServer(parametrosSeleccionados, currentPageTable, tipo_reporte, dataType);
    } else {
        currentPage = pageNumber;
        sendDataToServer(dataType, currentPage);
    }
}
