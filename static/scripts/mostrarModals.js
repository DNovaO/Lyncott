//mostrarModals.js
const modal = document.getElementById("genericModal");
const modalLabel = modal.querySelector(".modal-title");
const modalContent = modal.querySelector("#genericModalContent");
const modalFooter = modal.querySelector("#genericModalPagination");
const categoria_reporte = document.getElementById("categoria_reporte").textContent.trim();
const tipo_reporte = document.getElementById("tipo_reporte").textContent.trim();
let currentPage = 1;
let fullItemsArray = [];

document.addEventListener("DOMContentLoaded", function(){
    const modalButtons = document.querySelectorAll(".modal-trigger");

    modalButtons.forEach(button => {
        button.addEventListener("click", function(){
            const dataType = this.getAttribute("data-type");
            currentPage = 1;
            sendDataServer(dataType);
        });
    });

});

$(document).on('click', '.selectable-item', function() {
    // Obtener el texto del elemento seleccionado
    const selectedItemText = $(this).text();
    
    // Obtener el tipo de dato del botón que abrió el modal
    const dataType = $('#genericModal').data('type');
    
    // Encontrar el botón correspondiente y actualizar su texto
    $(`button[data-type="${dataType}"]`).text(selectedItemText);
    
    // Cerrar el modal
    $('#genericModal').modal('hide');
});

// Evento para abrir el modal y establecer el tipo de dato
$('.modal-trigger').on('click', function() {
    const dataType = $(this).data('type');
    $('#genericModal').data('type', dataType);
    $('#genericModal').modal('show');
});

function sendDataServer(dataType, currentPage){
    const endpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&data_type=${encodeURIComponent(dataType)}&page=${currentPage}`;

    fetch(endpointURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ data_type: dataType, page: currentPage })
    })
    .then(response => response.json())
    .then(data => {
        // Aquí manejas la data recibida del backend
        console.log("Data received successfully desde modals:", data);

        // Llama a la función en el otro script para manipular y mostrar el modal
        handleResponseData(data);
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}

function getCookie(name) {
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


function handleResponseData(data) {
    let dataType = data.data_type;

    switch (dataType) {
        case 'cliente_inicial':
        case 'cliente_final':
            fullItemsArray = data.clientes;
            modalContent.innerHTML = renderGeneral(data.clientesPaginados.objList, 'Clientes',dataType);
            modalFooter.innerHTML = renderPagination(data.clientesPaginados.pagination_info, currentPage, dataType);
            break;

        case 'producto_inicial':
        case 'producto_final':
            fullItemsArray = data.productos;
            modalContent.innerHTML = renderGeneral(data.productosPaginados.objList, 'Productos',dataType);
            modalFooter.innerHTML = renderPagination(data.productosPaginados.pagination_info, currentPage, dataType);
            break;

        case 'sucursal_inicial':
        case 'sucursal_final':
        case 'sucursal':
            fullItemsArray = data.sucursales;
            modalContent.innerHTML = renderGeneral(data.sucursalesPaginados.objList, 'Sucursales',dataType);
            modalFooter.innerHTML = renderPagination(data.sucursalesPaginados.pagination_info, currentPage, dataType);
            break;

        case 'vendedor_inicial':
        case 'vendedor_final':
            fullItemsArray = data.vendedores;
            modalContent.innerHTML = renderGeneral(data.vendedoresPaginados.objList, 'Vendedores',dataType);
            modalFooter.innerHTML = renderPagination(data.vendedoresPaginados.pagination_info, currentPage, dataType);
            break;

        case 'linea_inicial':
        case 'linea_final':
        case 'marca_inicial':
        case 'marca_final':
            fullItemsArray = data.lineas;
            modalContent.innerHTML = renderGeneral(data.lineasPaginados.objList, 'Lineas',dataType);
            modalFooter.innerHTML = renderPagination(data.lineasPaginados.pagination_info, currentPage, dataType);
            break;

        case 'familia_inicial':
        case 'familia_final':
        case 'familia':
            fullItemsArray = data.familias;
            modalContent.innerHTML = renderGeneral(data.familiasPaginados.objList, 'Familias',dataType);
            modalFooter.innerHTML = renderPagination(data.familiasPaginados.pagination_info, currentPage, dataType);
            break;

        case 'grupoCorporativo_inicial':
        case 'grupoCorporativo_final':
        case 'grupoCorporativo':
            fullItemsArray = data.gruposCorporativos;
            modalContent.innerHTML = renderGeneral(data.gruposCorporativosPaginados.objList, 'Grupos Corporativos',dataType);
            modalFooter.innerHTML = renderPagination(data.gruposCorporativosPaginados.pagination_info, currentPage, dataType);
            break;

        case 'segmento_inicial':
        case 'segmento_final':
            fullItemsArray = data.segmentos;
            modalContent.innerHTML = renderGeneral(data.segmentosPaginados.objList, 'Segmento',dataType);
            modalFooter.innerHTML = renderPagination(data.segmentosPaginados.pagination_info, currentPage, dataType);
            break;

        case 'status':
            fullItemsArray = data.estatus;
            modalContent.innerHTML = renderGeneral(data.estatusPaginados.objList, 'Estatus',dataType);
            modalFooter.innerHTML = renderPagination(data.estatusPaginados.pagination_info, currentPage, dataType);
            break;

        case 'zona':
            fullItemsArray = data.zonas;
            modalContent.innerHTML = renderGeneral(data.zonasPaginados.objList, 'Zonas',dataType);
            modalFooter.innerHTML = renderPagination(data.zonasPaginados.pagination_info, currentPage, dataType);
            break;

        case 'region':
            fullItemsArray = data.regiones;
            modalContent.innerHTML = renderGeneral(data.regionesPaginados.objList, 'Regiones', dataType);
            modalFooter.innerHTML = renderPagination(data.regionesPaginados.pagination_info, currentPage, dataType);
        default:
            console.error('Tipo de dato no reconocido');
            break;
    }

    $("#genericModal").modal("show");
}


function renderGeneral(paginatedItems, tipo,dataType) {
    let html = '<ul class="list-group mt-3">';
    
    html += `
        <div class="search-container d-flex mb-3">
            <svg style="margin-top: auto; margin-bottom: auto; padding-right:5px;" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.3-4.3"></path>
            </svg>
            <input style="margin-top: auto; margin-bottom: auto" class="rounded search-input" type="text" id="inputBusqueda" onkeyup="buscador('${dataType}')" placeholder="Buscar ${tipo}...">
        </div>
        <div id="resultList">
    `;
    
    paginatedItems.forEach(item => {
        let line = '';
        for (const key in item) {
            if (Object.hasOwnProperty.call(item, key)) {
                if (line !== '') {
                    line += ` - `;
                }
                line += `${item[key]}`;
            }
        }
        html += `<li type='button' class="list-group-item list-group-item-action selectable-item">${line}</li>`;
    });

    html += '</ul></div>';
    return html;
}

function buscador(dataType) {
    let input = document.getElementById("inputBusqueda");
    if (!input) {
        console.error("No se encontró el elemento de input");
        return;
    }
    
    let filter = input.value.trim().toLowerCase();
    
    if(filter === "") {
        sendDataServer(dataType);
        return;
    }

    let filteredItems = (filter === "") ? fullItemsArray : fullItemsArray.filter(item => {
        for (const key in item) {
            if (Object.hasOwnProperty.call(item, key)) {
                if (typeof item[key] === 'string' && item[key].toLowerCase().includes(filter)) {
                    return true;
                }
            }
        }
        return false;
    });

    let html = '';
    filteredItems.forEach(item => {
        let line = '';
        for (const key in item) {
            if (Object.hasOwnProperty.call(item, key)) {
                if (line !== '') {
                    line += ` - `;
                }
                line += `${item[key]}`;
            }
        }
        html += `<li type='button' class="list-group-item list-group-item-action selectable-item">${line}</li>`;
    });

    let resultList = document.getElementById("resultList");
    if (resultList) {
        resultList.innerHTML = html;
    } else {
        console.error("No se encontró el elemento de lista de resultados");
    }
}

function renderPagination(paginationInfo, currentPage, dataType) {
    let html = '<nav aria-label="Page navigation"><ul class="pagination justify-content-center">';

    html += '<li class="page-item">';
    if (paginationInfo && paginationInfo.has_previous) {
        html += `<a href="#" class="page-link" onclick="changePage(1, '${dataType}')">&laquo;</a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true">&laquo;</span>';
    }
    html += '</li>';

    html += '<li class="page-item">';
    if (paginationInfo && paginationInfo.has_previous) {
        html += `<a href="#" class="page-link" onclick="changePage(${paginationInfo.previous_page_number}, '${dataType}')">&lt;</a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true">&lt;</span>';
    }
    html += '</li>';

    html += `<li class="page-item disabled"><span class="page-link">Page ${currentPage} of ${paginationInfo.num_pages}</span></li>`;

    html += '<li class="page-item">';
    if (paginationInfo && paginationInfo.has_next) {
        html += `<a href="#" class="page-link" onclick="changePage(${paginationInfo.next_page_number}, '${dataType}')">&gt;</a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true">&gt;</span>';
    }
    html += '</li>';

    html += '<li class="page-item">';
    if (paginationInfo && paginationInfo.has_next) {
        html += `<a href="#" class="page-link" onclick="changePage(${paginationInfo.num_pages}, '${dataType}')">&raquo;</a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true">&raquo;</span>';
    }
    html += '</li>';

    html += '</ul></nav>';

    return html;
}

// Función para cambiar de página
function changePage(pageNumber, dataType) {
    // Actualizar la página actual
    currentPage = pageNumber;

    // Llamar a la función para cargar los datos de la página específica
    sendDataServer(dataType, pageNumber);
}
