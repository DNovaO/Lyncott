//mostrarModals.js
const modal = document.getElementById("genericModal");
const modalLabel = modal.querySelector(".modal-title");
const modalContent = modal.querySelector("#genericModalContent");
const modalFooter = modal.querySelector("#genericModalPagination");
const categoria_reporte = document.getElementById("categoria_reporte").textContent.trim();
const tipo_reporte = document.getElementById("tipo_reporte").textContent.trim();
const btnReset = document.getElementById('btnLimpiar');
const btnGenerarInforme = document.getElementById('btnGenerarInforme');
const fechaInicialInput = document.getElementById('fecha_inicial');
const fechaFinalInput = document.getElementById('fecha_final');
let parametrosSeleccionados = {};
let currentPage = 1;
let fullItemsArray = [];

document.addEventListener("DOMContentLoaded", function(){
    const modalButtons = document.querySelectorAll(".modal-trigger");

    setTimeout(function () {
        // Acceder a los valores de fecha después de la inicialización
        const fecha_inicial = fechaInicialInput.value;
        const fecha_final = fechaFinalInput.value;
    
        console.log("Fecha inicial:", fecha_inicial);
        console.log("Fecha final:", fecha_final);
    }, 500); // Ajusta este tiempo si es necesario esperar más tiempo
    
    modalButtons.forEach(button => {
        button.addEventListener("click", function(){
            const dataType = this.getAttribute("data-type");
            currentPage = 1;
            sendDataServer(dataType, currentPage);
        });
    });

    if (btnReset) {
        btnReset.addEventListener('click', function(e) {
            e.preventDefault();
            resetFormulario();
        });
    } else {
        console.error("Elemento con ID 'btnReset' no encontrado.");
    }

    if (btnGenerarInforme) {
        // Evento cuando se presiona el botón de generar informe
        btnGenerarInforme.addEventListener('click', function(e) {
            e.preventDefault();

            sendDataServer(dataType, currentPage, selectedItem)
        });
    } else {
        console.error("Elemento con ID 'btnGenerarInforme' no encontrado.");
    }
});

function sendDataServer(dataType, currentPage, selectedItem){
    const endpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&page=${currentPage}`;

    fetch(endpointURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ data_type: dataType, page: currentPage, selected_item: selectedItem })
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

function handleResponseData(data) {
    const dataType = data.data_type;
    const handler = handlers[dataType];

    if (handler) {
        handler(data, dataType);
    } else {
        console.error('Tipo de dato no reconocido');
    }

    // Mostrar el modal
    $("#genericModal").modal("show");

    // Manejar la selección de un elemento de la lista
    modalContent.querySelectorAll('.selectable-item').forEach(item => {
        item.addEventListener('click', function(event) {
            const selectedItem = JSON.parse(this.getAttribute('data-item'));
            const button = document.querySelector(`.modal-trigger[data-type="${dataType}"]`);
            
            // Obtener el texto del elemento seleccionado
            const buttonText = event.target.innerText.trim();
    
            // Actualizar el texto del botón con el texto del elemento seleccionado
            if (button) {
                button.textContent = buttonText;
                console.log('Texto del botón actualizado:', button.textContent);
            }
    
            // Cerrar el modal
            $("#genericModal").modal("hide");
        });
    });
    
}

function cargarData(data, key, dataType){
    console.log('cargar data', data[key]);
    modalContent.innerHTML = renderGeneral(data[key].objList, dataType);
    modalFooter.innerHTML = renderPagination(data[key].pagination_info, currentPage, dataType);
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

function resetFormulario() {
    // Limpiar campos de búsqueda si existen
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.value = ''; // Vaciar el valor del campo de búsqueda
    });
    
    // Restablecer texto de botones que activan los modales
    const modalButtons = document.querySelectorAll('.modal-trigger');
    modalButtons.forEach(button => {
        button.textContent = `Buscar ${button.getAttribute('data-type').replace('_', ' ').capitalize()}`; // Restablecer el texto del botón
    });
    
    // Limpiar contenido y pie del modal
    modalContent.innerHTML = '';
    modalFooter.innerHTML = '';
}

// Función para capitalizar la primera letra de cada palabra
String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

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


const handlers = {
    'cliente_inicial': function(data, dataType) {
        fullItemsArray = data.clientes;
        cargarData(data, 'clientesPaginados', dataType);
    },
    'cliente_final': function(data, dataType) {
        fullItemsArray = data.clientes;
        cargarData(data, 'clientesPaginados', dataType);
    },
    'producto_inicial': function(data, dataType) {
        fullItemsArray = data.productos;
        cargarData(data, 'productosPaginados', dataType);
    },
    'producto_final': function(data, dataType) {
        fullItemsArray = data.productos;
        cargarData(data, 'productosPaginados', dataType);
    },
    'sucursal_inicial': function(data, dataType) {
        fullItemsArray = data.sucursales;
        cargarData(data, 'sucursalesPaginados', dataType);
    },
    'sucursal_final': function(data, dataType) {
        fullItemsArray = data.sucursales;
        cargarData(data, 'sucursalesPaginados', dataType);
    },
    'sucursal': function(data, dataType) {
        fullItemsArray = data.sucursales;
        cargarData(data, 'sucursalesPaginados', dataType);
    },
    'vendedor_inicial': function(data, dataType) {
        fullItemsArray = data.vendedores;
        cargarData(data, 'vendedoresPaginados', dataType);
    },
    'vendedor_final': function(data, dataType) {
        fullItemsArray = data.vendedores;
        cargarData(data, 'vendedoresPaginados', dataType);
    },
    'linea_inicial': function(data, dataType) {
        fullItemsArray = data.lineas;
        cargarData(data, 'lineasPaginados', dataType);
    },
    'linea_final': function(data, dataType) {
        fullItemsArray = data.lineas;
        cargarData(data, 'lineasPaginados', dataType);
    },
    'marca_inicial': function(data, dataType) {
        fullItemsArray = data.lineas;
        cargarData(data, 'lineasPaginados', dataType);
    },
    'marca_final': function(data, dataType) {
        fullItemsArray = data.lineas;
        cargarData(data, 'lineasPaginados', dataType);
    },
    'familia_inicial': function(data, dataType) {
        fullItemsArray = data.familias;
        cargarData(data, 'familiasPaginados', dataType);
    },
    'familia_final': function(data, dataType) {
        fullItemsArray = data.familias;
        cargarData(data, 'familiasPaginados', dataType);
    },
    'familia': function(data, dataType) {
        fullItemsArray = data.familias;
        cargarData(data, 'familiasPaginados', dataType);
    },
    'grupoCorporativo_inicial': function(data, dataType) {
        fullItemsArray = data.gruposCorporativos;
        cargarData(data, 'gruposCorporativosPaginados', dataType);
    },
    'grupoCorporativo_final': function(data, dataType) {
        fullItemsArray = data.gruposCorporativos;
        cargarData(data, 'gruposCorporativosPaginados', dataType);
    },
    'grupoCorporativo': function(data, dataType) {
        fullItemsArray = data.gruposCorporativos;
        cargarData(data, 'gruposCorporativosPaginados', dataType);
    },
    'segmento_inicial': function(data, dataType) {
        fullItemsArray = data.segmentos;
        cargarData(data, 'segmentosPaginados', dataType);
    },
    'segmento_final': function(data, dataType) {
        fullItemsArray = data.segmentos;
        cargarData(data, 'segmentosPaginados', dataType);
    },
    'status': function(data, dataType) {
        fullItemsArray = data.estatus;
        cargarData(data, 'estatusPaginados', dataType);
    },
    'zona': function(data, dataType) {
        fullItemsArray = data.zonas;
        cargarData(data, 'zonasPaginados', dataType);
    },
    'region': function(data, dataType) {
        fullItemsArray = data.regiones;
        cargarData(data, 'regionesPaginados', dataType);
    }
};