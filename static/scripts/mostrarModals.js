//mostrarModals.js
let currentPage = 1; // Variable para almacenar la página actual
const modal = document.getElementById('genericModal');
const modalLabel = modal.querySelector('.modal-title');
const modalContent = modal.querySelector('#genericModalContent');
const modalFooter = modal.querySelector('#genericModalPagination');
const categoria_reporte = document.getElementById("categoria_reporte").textContent.trim();
const tipo_reporte = document.getElementById("tipo_reporte").textContent.trim();

document.querySelectorAll('.modal-trigger').forEach(function(button) {
    button.addEventListener('click', function(e) {
    e.preventDefault();
    const dataType = this.getAttribute('data-type');
    currentPage = 1; // Reset page to 1 on new trigger click
    loadModalContent(dataType, currentPage, categoria_reporte, tipo_reporte);
    });
});

function loadModalContent(dataType, pageNumber, categoria_reporte, tipo_reporte) {
    const csrftoken = getCookie('csrftoken');
    const reportUrl = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&data_type=${encodeURIComponent(dataType)}&page=${pageNumber}`;

    fetch(reportUrl, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
        'data': dataType,
    }),
    })
    .then(response => response.json())
    .then(result => {
    if (result.Clientes) {
        modalContent.innerHTML = renderClientes(result.Clientes);
        modalFooter.innerHTML = renderPagination(result.Pagination, pageNumber, dataType);
        $('#genericModal').modal('show');
    } else {
        modalContent.innerHTML = '<p>No hay datos disponibles.</p>';
    }
    })
    .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
    modalContent.innerHTML = '<p>Error al cargar el contenido.</p>';
    });
}

function renderClientes(clientes) {
    let html = '<ul class="list-group">';
    clientes.forEach(cliente => {
    html += `<li class="list-group-item">${cliente.clave_cliente} - ${cliente.nombre_cliente}</li>`;
    });
    html += '</ul>';
    return html;
}

function renderPagination(paginationData, currentPage, dataType) {
    let html = '<nav aria-label="Page navigation">';
    html += '<ul class="pagination justify-content-center">';

    html += '<li class="page-item">';
    if (paginationData && paginationData.has_previous) {
    html += `<a href="#" class="page-link" onclick="loadModalContent('${dataType}', 1, '${categoria_reporte}', '${tipo_reporte}')" aria-label="First"><span aria-hidden="true">&laquo;</span></a>`;
    } else {
    html += '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&laquo;</span></span>';
    }
    html += '</li>';

    html += '<li class="page-item">';
    if (paginationData && paginationData.has_previous) {
    html += `<a href="#" class="page-link" onclick="loadModalContent('${dataType}', ${paginationData.previous_page_number}, '${categoria_reporte}', '${tipo_reporte}')" aria-label="Previous"><span aria-hidden="true">&lt;</span></a>`;
    } else {
    html += '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&lt;</span></span>';
    }
    html += '</li>';

    html += '<li class="page-item disabled">';
    html += `<span class="page-link">Page ${currentPage} of ${paginationData.num_pages}</span>`;
    html += '</li>';

    html += '<li class="page-item">';
    if (paginationData && paginationData.has_next) {
    html += `<a href="#" class="page-link" onclick="loadModalContent('${dataType}', ${paginationData.next_page_number}, '${categoria_reporte}', '${tipo_reporte}')" aria-label="Next"><span aria-hidden="true">&gt;</span></a>`;
    } else {
    html += '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&gt;</span></span>';
    }
    html += '</li>';

    html += '<li class="page-item">';
    if (paginationData && paginationData.has_next) {
    html += `<a href="#" class="page-link" onclick="loadModalContent('${dataType}', ${paginationData.num_pages}, '${categoria_reporte}', '${tipo_reporte}')" aria-label="Last"><span aria-hidden="true">&raquo;</span></a>`;
    } else {
    html += '<span class="page-link disabled" aria-disabled="true"><span aria-hidden="true">&raquo;</span></span>';
    }
    html += '</li>';

    html += '</ul>';
    html += '</nav>';

    return html;
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

//Agregar funcion para mostrar modal segun el id del boton

