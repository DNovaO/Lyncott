// renderTabla.js
import { formatNumber, transformHeader } from './utils.js';
import { currentPageTable, renderPaginationTabla } from './main.js';

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

export function renderizarDatosEnTabla(data, dataType) {
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
