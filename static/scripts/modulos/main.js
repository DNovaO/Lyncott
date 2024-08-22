//main.js
export let cache = {};
export let dataType;
export let debouncedBuscador;
export let parametrosSeleccionados = {};
export let fullItemsArray = [];
export let currentPage = 1;
export let currentPageTable = 1;

import { tipo_reporte, btnMostrarGrafico, btnReset, btnGenerarInforme, btnBorrarReporte } from "./config.js"; 
import { sendDataToServer, sendParametersToServer } from './apiHandler.js';
import { handleItemSelected } from './renderModal.js';
import { buscador, resetFormulario, errorParametros, debounce} from './utils.js'; // Asegúrate de importar las funciones necesarias
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

            currentPage = 1;

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
            let parametrosInforme = {};
            
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


