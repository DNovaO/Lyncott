//main.js
export let cache = {};
export let dataType;
export let debouncedBuscador; 
export let parametrosSeleccionados = {};
export let fullItemsArray = [];
export let currentPage = 1;
export let currentPageTable = 1;
export let parametrosInforme = {};

import { tipo_reporte, btnMostrarGrafico, btnReset, btnGenerarInforme, btnBorrarReporte, modalContent, modalFooter} from "./config.js"; 
import { sendDataToServer, sendParametersToServer } from './apiHandler.js';
import { handleItemSelected, renderGeneral } from './renderModal.js';
import { errorParametros} from './utils.js'; // Asegúrate de importar las funciones necesarias
import { resetTabla } from './renderTabla.js';

document.addEventListener("DOMContentLoaded", function(){
    const modalButtons = document.querySelectorAll(".modal-trigger");
    
    modalButtons.forEach(button => {
        
        button.addEventListener("click", function(){
            dataType = this.getAttribute("data-type");
            
            console.log('El tipo de dato que vamos a enviar es:', dataType);

            debouncedBuscador = debounce(() => {
                console.log("dataType recibido:", dataType);
                buscador(dataType);
            }, 300);

            window.debouncedBuscador = debouncedBuscador;
            currentPage = 1;

            $("#genericModal").modal("show");

            sendDataToServer(dataType, currentPage);
        });
    });
    
    if (btnReset) {
        btnReset.addEventListener('click', function(e) {
            e.preventDefault();
            resetFormulario();
        });
    } 

    // Evento cuando se presiona el botón de generar informe
    if (btnGenerarInforme) {
        btnGenerarInforme.addEventListener('click', function(e) {
            cache = {};
            console.log('boton activado, y cache vacio', cache);
            e.preventDefault();
        
            
            // Actualizar dataType al inicio
            dataType = this.getAttribute("data-type");
            parametrosSeleccionados =  handleItemSelected(dataType, this);
            
            // Copiar valores seleccionados en parametrosInforme
            for (const parametro in parametrosSeleccionados) {
                parametrosInforme[parametro] = parametrosSeleccionados[parametro];
            }


            console.log(Object.keys(parametrosInforme).length);

            console.log(numeroParametro);
            
            // Verificar si el número de parámetros seleccionados es menor que el requerido
            if (Object.keys(parametrosInforme).length >= numeroParametro) {
                console.log('boton activado mandando informacion');
                errorParametros(false);

                currentPageTable = 1;

                console.log('dataType en sendParametersToServer:', dataType);
                sendParametersToServer(parametrosInforme, currentPageTable, tipo_reporte, dataType);
            } else {
                errorParametros(true);
            }
        });
    }

    if (btnBorrarReporte){
        btnBorrarReporte.addEventListener('click', function(e) {
            e.preventDefault();
            resetTabla();
        });
    }

    if (btnMostrarGrafico)
        document.getElementById('btnMostrarGrafico').addEventListener('click', function() {
            this.classList.toggle('btn-active-green');
        });

});


export function renderPagination(paginationInfo, currentPage, dataType, isTable = false) {
    let html = '<nav aria-label="Page navigation"><ul class="pagination justify-content-center">';

    html += '<li class="page-item">';
    if (paginationInfo && paginationInfo.has_previous) {
        html += `<a class="page-link" onclick="changePage(1, '${dataType}', ${isTable})">&laquo;</a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true">&laquo;</span>';
    }
    html += '</li>';

    html += '<li class="page-item">';
    if (paginationInfo && paginationInfo.has_previous) {
        html += `<a class="page-link" onclick="changePage(${paginationInfo.previous_page_number}, '${dataType}', ${isTable})">&lt;</a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true">&lt;</span>';
    }
    html += '</li>';

    html += `<li class="page-item disabled"><span class="page-link">Page ${currentPage} of ${paginationInfo.num_pages}</span></li>`;

    html += '<li class="page-item">';
    if (paginationInfo && paginationInfo.has_next) {
        html += `<a class="page-link" onclick="changePage(${paginationInfo.next_page_number}, '${dataType}', ${isTable})">&gt;</a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true">&gt;</span>';
    }
    html += '</li>';

    html += '<li class="page-item">';
    if (paginationInfo && paginationInfo.has_next) {
        html += `<a class="page-link" onclick="changePage(${paginationInfo.num_pages}, '${dataType}', ${isTable})">&raquo;</a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true">&raquo;</span>';
    }
    html += '</li>';

    html += '</ul></nav>';

    return html;
}

function changePage(pageNumber, dataType, isTable = false) {
    if (isTable) {
        currentPageTable = pageNumber;
        sendParametersToServer(parametrosSeleccionados, currentPageTable, tipo_reporte, dataType);
    } else {
        currentPage = pageNumber;
        sendDataToServer(dataType, currentPage);
    }
}

// Exponer changePage globalmente
window.changePage = changePage;

export function renderPaginationTabla(paginationInfo, currentPageTable, dataType) {
    return renderPagination(paginationInfo, currentPageTable, dataType, true);
}

export function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

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

        // Reemplazar eventos después de actualizar la lista
        resultList.querySelectorAll('.selectable-item').forEach(item => {
            item.addEventListener('click', function() {
                handleItemSelected(dataType, this);
                input.value = ""; // Resetear el input después de seleccionar
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