// renderModal.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script que contiene funciones de utilidad para el manejo de los modales, desde el renderizado de los datos hasta la paginación de los mismos. 
    Los datos que se cargan al modal son gracias a las funciones de fetch.
*/ 


import { modalContent, modalFooter, fechaInicialInput, fechaFinalInput } from './config.js';
import { handlers } from './itemHandler.js';
import { fullItemsArray, parametrosSeleccionados } from './main.js';

// Variable global para manejar la página actual del modal
let currentModalPage = 1;
const modalPageSize = 10; // Tamaño de página para el modal

document.querySelector('#genericModal .close').addEventListener('click', function () {
    $('#genericModal').modal('hide');
});

// Muestra un loader en el modal
export function showLoaderModal() {
    modalContent.innerHTML = `
        <div class="spinner-container">
            <div class="lds-ring">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
            <p>Cargando...</p>
        </div>
    `;
}

// Maneja los datos de la respuesta y muestra el modal
export function handleResponseData(data) {
    const dataType = data.data_type;
    const handler = handlers[dataType];

    if (handler) {
        handler(data, dataType);
    } else {
        console.error('Tipo de dato no reconocido');
    }

    // Mostrar el modal
    $("#genericModal").modal("show");

    // Establecer la página actual en el modal
    setCurrentModalPage(1); // O cualquier otra lógica para establecer la página que deseas

    // Capture the event of closing the modal
    $("#genericModal").on("hidden.bs.modal", function () {
        setCurrentModalPage(1);
    });

    // Manejar la selección de un elemento de la lista
    modalContent.querySelectorAll('.selectable-item').forEach(item => {
        item.addEventListener('click', function() {
            handleItemSelected(dataType, this);
        });
    });
}

// Carga los datos en el modal
export function cargarData(data, key, dataType) {
    if (data[key] && data[key].length > 0) {
        if (fullItemsArray.length === 0) {
            fullItemsArray.push(...data[key]);
        }

        const paginatedItems = paginarDatos(fullItemsArray, modalPageSize, currentModalPage);

        modalContent.innerHTML = renderGeneral(paginatedItems);
        modalFooter.innerHTML = renderPaginadoModal({
            totalPages: Math.ceil(fullItemsArray.length / modalPageSize),
            currentPage: currentModalPage
        }, dataType);

        // Volver a agregar manejadores de eventos
        modalContent.querySelectorAll('.selectable-item').forEach(item => {
            item.addEventListener('click', function() {
                handleItemSelected(dataType, this);
            });
        });
    } else {
        console.error('Datos inválidos para paginar:', data[key]);
    }
}

export function renderGeneral(paginatedItems) {
    let html = '<ul class="list-group mt-3">';
    
    paginatedItems.forEach(item => {
        let line = '';
        for (const key in item) {
            if (Object.hasOwnProperty.call(item, key)) {
                if (line !== '') {
                    line += ' - ';
                }
                line += `${item[key]}`;
            }
        }
        html += `<li type="button" class="list-group-item list-group-item-action selectable-item" data-item='${JSON.stringify(item)}'>${line}</li>`;
    });

    html += '</ul>';
    return html;
}

// Función para paginar datos
function paginarDatos(data, pageSize, pageNumber) {
    const startIndex = (pageNumber - 1) * pageSize;
    return data.slice(startIndex, startIndex + pageSize);
}

// Maneja la selección de un ítem
export function handleItemSelected(dataType, selectedItem) {
    // Obtener el texto del elemento seleccionado
    const buttonText = selectedItem.innerText.trim();
    
    // Obtener el objeto JSON del elemento seleccionado
    const parsedItem = JSON.parse(selectedItem.getAttribute('data-item'));
    
    // Actualizar el texto del botón con el texto del elemento seleccionado
    const button = document.querySelector(`.modal-trigger[data-type="${dataType}"]`);
    if (button) {
        button.textContent = buttonText;
    }
    
    // Si ya hay elementos seleccionados para este dataType, agregarlos, si no, crear una nueva lista
    if (!parametrosSeleccionados[dataType]) {
        parametrosSeleccionados[dataType] = [];
    }

    // Agregar el nuevo elemento seleccionado al arreglo de parámetros
    parametrosSeleccionados[dataType] = [parsedItem];

    // Actualizar las fechas
    parametrosSeleccionados['fecha_inicial'] = fechaInicialInput.value;
    parametrosSeleccionados['fecha_final'] = fechaFinalInput.value;

    // Cerrar el modal
    $("#genericModal").modal("hide");
    setCurrentModalPage(1);

    // Retornar los parámetros seleccionados para su uso posterior
    return parametrosSeleccionados;
}

export function renderPaginadoModal(paginationInfo, dataType) {
    const { totalPages } = paginationInfo;
    const startPages = 3; // Primeras páginas a mostrar
    const endPages = 2;   // Últimas páginas a mostrar
    const currentModalPage = paginationInfo.currentPage;

    const maxVisiblePages = startPages + endPages; // Total visible páginas (incluye "..." y los botones de navegación)
    
    let paginationHTML = '<nav aria-label="Page navigation"><ul class="pagination justify-content-center flex-wrap">';

    // Botón "Primera página"
    if (currentModalPage > 1) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="javascript:void(0);" onclick="cambiarPaginaModal(1, '${dataType}', event)">&laquo;&laquo;</a>
            </li>`;
    } else {
        paginationHTML += `
            <li class="page-item disabled">
                <span class="page-link">&laquo;&laquo;</span>
            </li>`;
    }

    // Botón "Anterior"
    if (currentModalPage > 1) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="javascript:void(0);" onclick="cambiarPaginaModal(${currentModalPage - 1}, '${dataType}', event)">&laquo;</a>
            </li>`;
    } else {
        paginationHTML += `
            <li class="page-item disabled">
                <span class="page-link">&laquo;</span>
            </li>`;
    }

    // Determinar el rango de páginas a mostrar
    let startPage, endPage;

    if (totalPages <= maxVisiblePages) {
        // Mostrar todas las páginas si el total es menor que el máximo visible
        startPage = 1;
        endPage = totalPages;
    } else {
        // Determinar el rango de páginas a mostrar
        if (currentModalPage <= startPages) {
            // Página actual está en el inicio
            startPage = 1;
            endPage = maxVisiblePages - 1;
        } else if (currentModalPage + endPages - 1 >= totalPages) {
            // Página actual está en el final
            startPage = totalPages - maxVisiblePages + 2;
            endPage = totalPages;
        } else {
            // Página actual está en el medio
            startPage = currentModalPage - Math.floor(startPages / 2);
            endPage = currentModalPage + Math.floor(endPages / 2);
        }
    }

    // Mostrar las páginas dentro del rango determinado
    for (let i = startPage; i <= endPage; i++) {
        if (i === currentModalPage) {
            paginationHTML += `
                <li class="page-item active">
                    <span class="page-link">${i}</span>
                </li>`;
        } else {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link" href="javascript:void(0);" onclick="cambiarPaginaModal(${i}, '${dataType}', event)">${i}</a>
                </li>`;
        }
    }

    // Mostrar "..." si hay más páginas que las visibles
    if (endPage < totalPages - endPages) {
        paginationHTML += `
            <li class="page-item disabled">
                <span class="page-link">...</span>
            </li>`;
        
        // Mostrar las últimas páginas
        for (let i = totalPages - endPages + 1; i <= totalPages; i++) {
            if (i === currentModalPage) {
                paginationHTML += `
                    <li class="page-item active">
                        <span class="page-link">${i}</span>
                    </li>`;
            } else {
                paginationHTML += `
                    <li class="page-item">
                        <a class="page-link" href="javascript:void(0);" onclick="cambiarPaginaModal(${i}, '${dataType}', event)">${i}</a>
                    </li>`;
            }
        }
    } else {
        // Si no hay "..." para mostrar, solo las páginas desde endPage+1 hasta totalPages
        for (let i = endPage + 1; i <= totalPages; i++) {
            if (i === currentModalPage) {
                paginationHTML += `
                    <li class="page-item active">
                        <span class="page-link">${i}</span>
                    </li>`;
            } else {
                paginationHTML += `
                    <li class="page-item">
                        <a class="page-link" href="javascript:void(0);" onclick="cambiarPaginaModal(${i}, '${dataType}', event)">${i}</a>
                    </li>`;
            }
        }
    }

    // Botón "Siguiente"
    if (currentModalPage < totalPages) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="javascript:void(0);" onclick="cambiarPaginaModal(${currentModalPage + 1}, '${dataType}', event)">&raquo;</a>
            </li>`;
    } else {
        paginationHTML += `
            <li class="page-item disabled">
                <span class="page-link">&raquo;</span>
            </li>`;
    }

    // Botón "Última página"
    if (currentModalPage < totalPages) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="javascript:void(0);" onclick="cambiarPaginaModal(${totalPages}, '${dataType}', event)">&raquo;&raquo;</a>
            </li>`;
    } else {
        paginationHTML += `
            <li class="page-item disabled">
                <span class="page-link">&raquo;&raquo;</span>
            </li>`;
    }

    paginationHTML += '</ul></nav>';

    return paginationHTML;
}

// Función para cambiar la página
function cambiarPaginaModal(pageNumber, dataType, event) {
    if (event) {
        event.preventDefault(); // Prevenir que la página se desplace hacia arriba
    }
    console.log('Cambiando a la página:', pageNumber, 'dataType:', dataType); // Agrega esto para depuración
    setCurrentModalPage(pageNumber);
    // Usa `fullItemsArray` para obtener los datos completos
    cargarData({[dataType]: fullItemsArray}, dataType, dataType); // Cargar la página seleccionada
}

// Función para establecer la página actual en el modal
function setCurrentModalPage(page) {
    currentModalPage = page;
}

window.cambiarPaginaModal = cambiarPaginaModal; // Hacer disponible para los enlaces
