// renderTabla.js
import { formatNumber, transformHeader } from './utils.js';
let dataGlobal;

export function showLoaderTabla() {
    const tabla = document.querySelector('.table tbody');
    tabla.innerHTML = `
        <tr>
            <td colspan="100%" class="text-center">
                <div class="lds-ellipsis">
                    Cargando
                    <div></div><div></div><div></div><div></div>
                </div>
            </td>
        </tr>
    `;
}

export function renderizarDatosEnTabla(data, dataType, currentPage = 1, pageSize = 10) {
    // Almacenar los datos globalmente
    dataGlobal = data;

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
            ${dataGlobal.campos_reporte.map(campo => {
                const transformedHeader = transformHeader(campo);
                return `<th scope="col">${transformedHeader}</th>`;
            }).join('')}
        </tr>
    `;
    thead.innerHTML = theadHTML;

    // Paginar los datos completos
    const paginatedData = paginarDatos(dataGlobal.datos_completos, pageSize, currentPage);

    // Renderizar datos en el cuerpo de la tabla (tbody)
    if (paginatedData.length > 0) {
        const tbodyHTML = paginatedData.map((fila, index) => {
            const filaHTML = `
                <tr>
                    <th scope="row">${(currentPage - 1) * pageSize + index + 1}</th>
                    ${dataGlobal.campos_reporte.map(campo => {
                        const value = fila[campo];
                        return `<td>${formatNumber(value, false, campo)}</td>`;
                    }).join('')}
                </tr>
            `;
            return filaHTML;
        }).join('');
        tabla.innerHTML = tbodyHTML;

        // Renderizar paginación
        tablaFooter.innerHTML = renderPaginadoTabla({
            totalPages: Math.ceil(dataGlobal.datos_completos.length / pageSize),
            currentPage: currentPage
        }, currentPage, dataType);

    } else {
        // Mostrar mensaje de "No hay datos disponibles"
        tabla.innerHTML = `<tr><td colspan="${dataGlobal.campos_reporte.length + 1}" class="text-center">No hay datos disponibles</td></tr>`;
    }
}

// Función para paginar los datos
function paginarDatos(data, pageSize, pageNumber) {
    const startIndex = (pageNumber - 1) * pageSize;
    return data.slice(startIndex, startIndex + pageSize);
}

function renderPaginadoTabla(paginationInfo, currentPage, dataType) {
    const { totalPages } = paginationInfo;
    const startPages = 1; // Primeras páginas a mostrar
    const endPages = 3;   // Últimas páginas a mostrar
    const maxVisiblePages = startPages + endPages; // Total visible páginas (incluye "..." y los botones de navegación)

    let paginationHTML = `
        <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center flex-wrap">
    `;

    // Botón "Primera página"
    if (currentPage > 1) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="javascript:void(0);" aria-label="First" onclick="cambiarPagina(1, '${dataType}', event)">
                    <span aria-hidden="true">&laquo;&laquo;</span>
                </a>
            </li>
        `;
    } else {
        paginationHTML += `
            <li class="page-item disabled">
                <span class="page-link" aria-hidden="true">&laquo;&laquo;</span>
            </li>
        `;
    }

    // Botón "Anterior"
    if (currentPage > 1) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="javascript:void(0);" aria-label="Previous" onclick="cambiarPagina(${currentPage - 1}, '${dataType}', event)">
                    <span aria-hidden="true">&laquo;</span>
                </a>
            </li>
        `;
    } else {
        paginationHTML += `
            <li class="page-item disabled">
                <span class="page-link" aria-hidden="true">&laquo;</span>
            </li>
        `;
    }

    // Determinar el rango de páginas a mostrar
    let startPage, endPage;

    if (totalPages <= maxVisiblePages) {
        // Mostrar todas las páginas si el total es menor que el máximo visible
        startPage = 1;
        endPage = totalPages;
    } else {
        // Determinar el rango de páginas a mostrar
        if (currentPage <= startPages) {
            // Página actual está en el inicio
            startPage = 1;
            endPage = maxVisiblePages - 1;
        } else if (currentPage + endPages - 1 >= totalPages) {
            // Página actual está en el final
            startPage = totalPages - maxVisiblePages + 2;
            endPage = totalPages;
        } else {
            // Página actual está en el medio
            startPage = currentPage - Math.floor(startPages / 2);
            endPage = currentPage + Math.floor(endPages / 2);
        }
    }

    // Mostrar las primeras páginas
    for (let i = startPage; i <= endPage; i++) {
        if (i === currentPage) {
            paginationHTML += `
                <li class="page-item active">
                    <span class="page-link">${i}</span>
                </li>
            `;
        } else {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link" href="javascript:void(0);" onclick="cambiarPagina(${i}, '${dataType}', event)">${i}</a>
                </li>
            `;
        }
    }

    // Mostrar "..." si hay más páginas que las visibles
    if (endPage < totalPages - endPages) {
        paginationHTML += `
            <li class="page-item disabled">
                <span class="page-link">...</span>
            </li>
        `;
        // Mostrar las últimas páginas
        for (let i = totalPages - endPages + 1; i <= totalPages; i++) {
            if (i === currentPage) {
                paginationHTML += `
                    <li class="page-item active">
                        <span class="page-link">${i}</span>
                    </li>
                `;
            } else {
                paginationHTML += `
                    <li class="page-item">
                        <a class="page-link" href="javascript:void(0);" onclick="cambiarPagina(${i}, '${dataType}', event)">${i}</a>
                    </li>
                `;
            }
        }
    } else {
        // Si no hay "..." para mostrar, solo las páginas desde endPage+1 hasta totalPages
        for (let i = endPage + 1; i <= totalPages; i++) {
            if (i === currentPage) {
                paginationHTML += `
                    <li class="page-item active">
                        <span class="page-link">${i}</span>
                    </li>
                `;
            } else {
                paginationHTML += `
                    <li class="page-item">
                        <a class="page-link" href="javascript:void(0);" onclick="cambiarPagina(${i}, '${dataType}', event)">${i}</a>
                    </li>
                `;
            }
        }
    }

    // Botón "Siguiente"
    if (currentPage < totalPages) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="javascript:void(0);" aria-label="Next" onclick="cambiarPagina(${currentPage + 1}, '${dataType}', event)">
                    <span aria-hidden="true">&raquo;</span>
                </a>
            </li>
        `;
    } else {
        paginationHTML += `
            <li class="page-item disabled">
                <span class="page-link" aria-hidden="true">&raquo;</span>
            </li>
        `;
    }

    // Botón "Última página"
    if (currentPage < totalPages) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="javascript:void(0);" aria-label="Last" onclick="cambiarPagina(${totalPages}, '${dataType}', event)">
                    <span aria-hidden="true">&raquo;&raquo;</span>
                </a>
            </li>
        `;
    } else {
        paginationHTML += `
            <li class="page-item disabled">
                <span class="page-link" aria-hidden="true">&raquo;&raquo;</span>
            </li>
        `;
    }

    paginationHTML += `
            </ul>
        </nav>
    `;

    return paginationHTML;
}


function cambiarPagina(pageNumber, dataType, event) {
    if (event) {
        event.preventDefault(); // Prevenir que la página se desplace hacia arriba
    }
    renderizarDatosEnTabla(dataGlobal, dataType, pageNumber);
}

window.cambiarPagina = cambiarPagina;

export function resetTabla() {
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
    tabla.innerHTML = `<tr class="alert alert-success" role="alert"><td class="text-center">¡Reporte eliminado con éxito!</td></tr>`;        
    tablaFooter.innerHTML = '';
}
