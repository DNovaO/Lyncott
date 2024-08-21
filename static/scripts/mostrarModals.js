//mostrarModals.js
const parametrosReporte = document.getElementById("parametros-reporte");
const modal = document.getElementById("genericModal");
const modalLabel = modal.querySelector(".modal-title");
const modalContent = modal.querySelector("#genericModalContent");
const modalFooter = modal.querySelector("#genericModalPagination");
const categoria_reporte = document.getElementById("categoria_reporte").textContent.trim();
const tipo_reporte = document.getElementById("tipo_reporte").textContent.trim();
const btnMostrarGrafico = document.getElementById('btnMostrarGrafico');
const btnReset = document.getElementById('btnLimpiar');
const btnGenerarInforme = document.getElementById('btnGenerarInforme');
const btnMostrarFiltros = document.getElementById('btnMostrarFiltros');
const btnBorrarReporte = document.getElementById('btnBorrarReporte');
const fechaInicialInput = document.getElementById('fecha_inicial');
const fechaFinalInput = document.getElementById('fecha_final');
let cache = {};
let dataType;
let debouncedBuscador;
let parametrosSeleccionados = {};
let currentPage = 1;
let currentPageTable = 1;
let fullItemsArray = [];

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

async function fetchData(endpoint, body, cacheKey, prefetch = false) {
    console.log('Datos enviados a fetchData:', body); // Agrega esta línea

    if (cache[cacheKey]) {
        console.log(`Cache hit for key: ${cacheKey}`);
        return cache[cacheKey];
    }

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        cache[cacheKey] = data;

        if (!prefetch) {
            return data;
        }

        // Prefetch adicional si es necesario
        return data;
    } catch (error) {
        console.error("Error:", error);
        if (!prefetch) {
            mostrarError('Ocurrió un error al obtener los datos. Por favor, inténtelo de nuevo.');
            throw error;
        }
    }
}

function sendDataToServer(dataType, currentPage) {
    const endpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&page=${currentPage}`;
    const body = { data_type: dataType, page: currentPage };
    const cacheKey = `${dataType}_${currentPage}`;

    showLoaderModal();

    fetchData(endpointURL, body, cacheKey)
        .then(data => {
            handleResponseData(data);
            
            const nextPage = currentPage + 1;
            const nextCacheKey = `${dataType}_${nextPage}`;
            const nextEndpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&page=${nextPage}`;
            fetchData(nextEndpointURL, { data_type: dataType, page: nextPage }, nextCacheKey, true);
        
        })
        .catch(error => console.error("Error:", error));
}

function sendParametersToServer(parametrosInforme, currentPageTable, tipoReporte) {
    console.log('Parametros que fueron seleccionados y seran manipulados', parametrosInforme);

    // Establece dataType como 'resultado' siempre
    const dataType = 'resultado';

    const endpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipoReporte)}&page=${currentPageTable}`;
    const body = { parametros_seleccionados: parametrosInforme, page: currentPageTable, tipo_reporte: tipoReporte, data_type: dataType };

    // Usa tipoReporte y currentPageTable para el cacheKey
    const cacheKey = `${tipoReporte}_${currentPageTable}`;

    showLoaderTabla();

    console.log('Datos enviados a fetchData:', body); // Verifica los datos enviados

    fetchData(endpointURL, body, cacheKey)
    .then(data => {
        renderizarDatosEnTabla(data, tipoReporte);
        console.log('Los datos recibidos son:', data);
        
        if (data.resultadoPaginado.pagination_info.has_next) {
            // Prefetch de la siguiente página
            const nextPage = currentPageTable + 1;
            const nextCacheKey = `${tipoReporte}_${nextPage}`;
            const nextEndpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipoReporte)}&page=${nextPage}`;
            fetchData(nextEndpointURL, { parametros_seleccionados: parametrosInforme, page: nextPage, tipo_reporte: tipoReporte, data_type: dataType }, nextCacheKey, true);
        }
    })
    .catch(error => console.error("Error:", error));
}


function transformHeader(header) {
    return header.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
}

function renderizarDatosEnTabla(data, dataType) {
    const tabla = document.querySelector('.table tbody');
    const thead = document.querySelector('.table thead');
    const tablaFooter = document.getElementById('genericTablaPagination');

    // Limpiar tbody y thead antes de renderizar nuevos datos
    tabla.innerHTML = '';
    thead.innerHTML = '';

    // Renderizar encabezados de tabla (thead)
    const theadHTML = `
        <tr>
            <th scope="col">#</th>
            ${data.campos_reporte.map(campo => {
                const transformedHeader = transformHeader(campo);
                return `<th scope="col">${transformedHeader}</th>`;
            }).join('')}
        </tr>
    `;
    thead.innerHTML = theadHTML;

    // Renderizar datos en el cuerpo de la tabla (tbody)
    if (data.resultadoPaginado.objList.length > 0) {
        const tbodyHTML = data.resultadoPaginado.objList.map((fila, index) => {
            const filaHTML = `
                <tr>
                    <th scope="row">${index + 1}</th>
                    ${data.campos_reporte.map(campo => {
                        const value = fila[campo];
                        return `<td>${formatNumber(value, false, campo)}</td>`;
                    }).join('')}
                </tr>
            `;
            return filaHTML;
        }).join('');
        tabla.innerHTML = tbodyHTML;

        // Renderizar paginación
        tablaFooter.innerHTML = renderPaginationTabla(data.resultadoPaginado.pagination_info, currentPageTable, dataType);
    } else {
        // Mostrar mensaje de "No hay datos disponibles"
        tabla.innerHTML = `<tr><td colspan="${data.campos_reporte.length + 1}" class="text-center">No hay datos disponibles</td></tr>`;
    }
}

function formatNumber(value, isCurrency = false, key = '') {
    // Lista de claves que no deben ser formateadas
    const keysToExcludeFromFormatting = ['clave_producto', 'sucursal', 'clave_cliente'];

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

function showLoaderTabla() {
    const tabla = document.querySelector('.table tbody');

    tabla.innerHTML = '<tr><td colspan="100%" class="text-center"><div class="lds-ellipsis">Cargando<div></div><div></div><div></div><div></div></div></td></tr>';
}

function showLoaderModal() {
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

// Función para manejar la selección de un ítem
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

    // Imprimir para verificar
    console.log('Parámetros seleccionados:', parametrosSeleccionados);
    
    // Retornar los parámetros seleccionados para su uso posterior
    return parametrosSeleccionados;
}

function errorParametros(estado) {
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


function renderPagination(paginationInfo, currentPage, dataType, isTable = false) {
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


function renderPaginationTabla(paginationInfo, currentPageTable, dataType) {
    return renderPagination(paginationInfo, currentPageTable, dataType, true);
}

// Función para cambiar de página
function changePageTabla(pageNumber) {
    const tipo_reporte = document.getElementById("tipo_reporte").textContent.trim();
    currentPageTable = pageNumber;

    sendParametersToServer(parametrosSeleccionados, currentPageTable, tipo_reporte);
}  

function resetTabla() {
    const tabla = document.querySelector('.table tbody');
    const thead = document.querySelector('.table thead');
    const tablaFooter = document.getElementById('genericTablaPagination');

    // Limpiar encabezado y cuerpo de la tabla
    thead.innerHTML = '';
    tabla.innerHTML = '';

    const theadHTML = `
        <tr>
            <th scope="col">#</th>
        </tr>
    `;

    thead.innerHTML = theadHTML;
    tabla.innerHTML = `<tr class="alert alert-success" role="alert"><td class="text-center" >¡Reporte eliminado con éxito!</td></tr>`;        
    tablaFooter.innerHTML = ''
}


function resetFormulario() {
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
    },
}; 