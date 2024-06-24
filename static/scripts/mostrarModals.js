//mostrarModals.js
let currentPage = 1; // Variable para almacenar la página actual
const formButton = document.querySelector('#desplegar_ClientesIniciales');
const categoria_reporte = document.getElementById("categoria_reporte").textContent.trim();
const tipo_reporte = document.getElementById("tipo_reporte").textContent.trim();

formButton.onclick = function(e) {
    e.preventDefault();
    const desplegarClientesIniciales = document.querySelector('#clientesContentInicial').value;
    sendData(desplegarClientesIniciales, currentPage, categoria_reporte, tipo_reporte); // Pasar currentPage, categoria_reporte, tipo_reporte y data al enviar los datos
};

async function sendData(data, pageNumber, categoria_reporte, tipo_reporte) {
    const csrftoken = getCookie('csrftoken');
    const reportUrl = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&page=${pageNumber}`;

    console.log('reportUrl:', reportUrl);
    try {
        const response = await fetch(reportUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'data': data,
            }),
        });

        console.log('response:', response);

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();

        if (result.Clientes) {
            // Limpiar el contenido anterior del modal si es necesario
            const modalContent = document.querySelector('#clientesContentInicial');
            modalContent.innerHTML = renderClientes(result.Clientes);

            // Actualizar la paginación
            const paginationContainer = document.querySelector('#paginationContainer');
            paginationContainer.innerHTML = renderPagination(result.Pagination, pageNumber, data);

            // Mostrar el modal si no se muestra automáticamente
            $('#clientesModalInicial').modal('show');

            // Actualizar la URL con el número de página
            history.pushState({}, '', `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&page=${pageNumber}`);

            // Agregar listener para cuando se oculte el modal
            $('#clientesModalInicial').on('hidden.bs.modal', function () {
                // Restablecer la URL original
                history.pushState({}, '', `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&page=${pageNumber=1}`);

            });

        } else {
            console.log("No hay datos de clientes.");
        }
    } catch (error) {
        console.log('There was a problem with the fetch operation:', error);
    }
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

// Función para renderizar la lista de clientes
function renderClientes(clientes) {
    let html = '<ul class="list-group">';
    clientes.forEach(cliente => {
        html += `<li class="list-group-item">${cliente.clave_cliente} - ${cliente.nombre_cliente}</li>`;
    });
    html += '</ul>';
    return html;
}

// Función para renderizar la paginación
function renderPagination(paginationData, currentPage, data) {
    let html = '<nav aria-label="Page navigation">';
    html += '<ul class="pagination justify-content-center">';

    // Botones de "first" y "previous"
    html += '<li class="page-item">';
    if (paginationData && paginationData.has_previous) {
        html += `<a href="#" class="page-link" onclick="sendData('${data}', 1, '${categoria_reporte}', '${tipo_reporte}')" aria-label="First"><span aria-hidden="true">&laquo;</span></a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&laquo;</span></span>';
    }
    html += '</li>';

    html += '<li class="page-item">';
    if (paginationData && paginationData.has_previous) {
        html += `<a href="#" class="page-link" onclick="sendData('${data}', ${paginationData.previous_page_number}, '${categoria_reporte}', '${tipo_reporte}')" aria-label="Previous"><span aria-hidden="true">&lt;</span></a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&lt;</span></span>';
    }
    html += '</li>';

    // Página actual
    html += '<li class="page-item disabled">';
    html += `<span class="page-link">Page ${currentPage} of ${paginationData.num_pages}</span>`;
    html += '</li>';

    // Botones de "next" y "last"
    html += '<li class="page-item">';
    if (paginationData && paginationData.has_next) {
        html += `<a href="#" class="page-link" onclick="sendData('${data}', ${paginationData.next_page_number}, '${categoria_reporte}', '${tipo_reporte}')" aria-label="Next"><span aria-hidden="true">&gt;</span></a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&gt;</span></span>';
    }
    html += '</li>';

    html += '<li class="page-item">';
    if (paginationData && paginationData.has_next) {
        html += `<a href="#" class="page-link" onclick="sendData('${data}', ${paginationData.num_pages}, '${categoria_reporte}', '${tipo_reporte}')" aria-label="Last"><span aria-hidden="true">&raquo;</span></a>`;
    } else {
        html += '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&raquo;</span></span>';
    }
    html += '</li>';

    html += '</ul>';
    html += '</nav>';

    return html;
}
