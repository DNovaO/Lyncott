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
let debouncedBuscador;
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
    } else {
        console.error("Elemento con ID 'btnReset' no encontrado.");
    }

    // Evento cuando se presiona el botón de generar informe
    if (btnGenerarInforme) {
        btnGenerarInforme.addEventListener('click', function(e) {
            e.preventDefault();

            // Crear un nuevo objeto para almacenar todos los parámetros seleccionados
            let parametrosInforme = {};

            // Iterar sobre parametrosSeleccionados para copiar sus valores
            for (const dataType in parametrosSeleccionados) {
                if (Object.hasOwnProperty.call(parametrosSeleccionados, dataType)) {
                    parametrosInforme[dataType] = parametrosSeleccionados[dataType];
                }
            }

            // Agregar los parámetros adicionales, como fechas
            parametrosInforme['fecha_inicial'] = fechaInicialInput.value;
            parametrosInforme['fecha_final'] = fechaFinalInput.value;

            // Enviar los parámetros al servidor
            sendParametersToServer(parametrosInforme);
            console.log('Parámetros enviados!');
            resetFormulario();
        });
    }
});

function sendDataToServer(dataType, currentPage){
    const endpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&page=${currentPage}`;

    fetch(endpointURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ data_type: dataType, page: currentPage})
    })
    .then(response => response.json())
    .then(data => {
        // Llama a la función para manipular la data y mostrar el modal
        handleResponseData(data);
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}

function sendParametersToServer(parametrosSeleccionados){
    const endpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&page=${currentPage}`;

    fetch(endpointURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ parametros_seleccionados: parametrosSeleccionados })
    })
    .then(response => response.json())
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
        item.addEventListener('click', function() {
            handleItemSelected(dataType, this);
        });
    });
}

function cargarData(data, key, dataType){
    modalContent.innerHTML = renderGeneral(data[key].objList, key, dataType); // Asegúrate de pasar 'key' y 'dataType'
    modalFooter.innerHTML = renderPagination(data[key].pagination_info, currentPage, dataType);
}

// Función debounce para limitar la frecuencia de ejecución
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Ajusta la función renderGeneral para solo manejar la lista de elementos
function renderGeneral(paginatedItems) {
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

function buscador(dataType) {
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

function handleItemSelected(dataType, selectedItem) {
    // Obtener el texto del elemento seleccionado
    const buttonText = selectedItem.innerText.trim();
    
    // Obtener el objeto JSON del elemento seleccionado
    const parsedItem = JSON.parse(selectedItem.getAttribute('data-item'));
    
    console.log('Elemento seleccionado:', parsedItem);
    
    // Actualizar el texto del botón con el texto del elemento seleccionado
    const button = document.querySelector(`.modal-trigger[data-type="${dataType}"]`);
    if (button) {
        button.textContent = buttonText;
    }
    
    // Inicializar el arreglo si no existe
    if (!parametrosSeleccionados[dataType]) {
        parametrosSeleccionados[dataType] = [];
    }
    
    // Agregar el elemento seleccionado al arreglo
    parametrosSeleccionados[dataType].push(parsedItem);

    // Cerrar el modal
    $("#genericModal").modal("hide");

    // Imprimir para verificar
    console.log('Parámetros seleccionados:', parametrosSeleccionados);

    // Devolver el objeto actualizado
    return parametrosSeleccionados;
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
    sendDataToServer(dataType, pageNumber);
}


function resetFormulario() {
    // Restablecer texto de botones que activan los modales
    const modalButtons = document.querySelectorAll('.modal-trigger');
    modalButtons.forEach(button => {
        button.textContent = `Buscar ${button.getAttribute('data-type').replace('_', ' ').capitalize()}`; // Restablecer el texto del botón
    });
    
    // Limpiar contenido y pie del modal
    modalContent.innerHTML = '';
    modalFooter.innerHTML = '';
    parametrosInforme = {};
    parametrosSeleccionados = {};
    
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