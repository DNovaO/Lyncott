// renderTabla.js
import { formatNumber, transformHeader } from './utils.js';
import { exportToCSV, exportToExcel, imprimirInformacion } from "./exportaciones.js";
import { btnExportarCSV , btnExportarExcel, btnImprimir, btnMostrarGrafico, tipo_reporte} from "./config.js"
import { mostrarGrafico } from "./graficas.js";

let dataGlobal;

document.addEventListener("DOMContentLoaded", function(){

    if (btnExportarCSV){
        btnExportarCSV.addEventListener('click', function(e) {
            exportToCSV(datos, 'data.csv');    
        });
    }

    if (btnExportarExcel){
        btnExportarExcel.addEventListener('click', function(e) {
            exportToExcel(datos, 'data.xlsx');    
        });
    }   

    if (btnImprimir){
        btnImprimir.addEventListener('click', function(e) {
            imprimirInformacion(datos, 'data.pdf');    
        });
    }

    if (btnMostrarGrafico){
        btnMostrarGrafico.addEventListener('click', function(e) {
            mostrarGrafico(dataGlobal, tipo_reporte)
        });
    }

});

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

export function renderizarDatosEnTabla(data, dataType, currentPage = 1, pageSize = 10, 
        columnasNoSumar = ['clave_producto', 'descripcion_producto', 'producto', 'sucursal', 
        'clave', 'clave_sucursal', 'numero_tipo_documento', 'grupo_movimiento',
        'detalles_tipo_documento', 'almacen_correspondiente', 'moneda','zona',
        'orden', 'orden_fecha', 'numero_folio', 'partes_folio', 'partes_fecha',
        'termina_folio', 'nombre', 'zona', 'nombre_producto','UPC','linea',
        'Promedio_Cliente', 'Promedio_Consignatario', 'fecha', 'dia','clave_cliente', 'consignatario', 'segmentacion', 'clave_grupo_corporativo', 'clave_cliente', 'clave_consignatario', 'producto', 'No', 'id_vendedor', 'id_almacen',
        'vendedor','id_grupo_corporativo','grupo_corporativo',
        'id_consignatario', 'consignatario', 'CP', 'colonia' ,'folio','RFC', 'UUID', 'serie','clave_vendedor',
        'nombre_vendedor','numero_mes', 'zona_vendedor', 'nombre_cliente'
    ]) {
    
    // Almacenar los datos globalmente
    dataGlobal = data;

    window.datos = dataGlobal;

    const tabla = document.querySelector('.table tbody');
    const thead = document.querySelector('.table thead');
    const tablaFooter = document.getElementById('genericTablaPagination');

    // Limpiar tbody y thead antes de renderizar nuevos datos
    tabla.innerHTML = '';
    thead.innerHTML = '';

    // Renderizar encabezados de tabla (thead)
    const theadHTML = `
        <tr>
            <th scope="col" class="numero-tabla">#</th>
            ${dataGlobal.campos_reporte.map(campo => {
                const transformedHeader = transformHeader(campo);
                return `<th scope="col" class="datos-tabla">${transformedHeader}</th>`;
            }).join('')}
        </tr>
    `;
    thead.innerHTML = theadHTML;

    // Paginar los datos completos
    const paginatedData = paginarDatos(dataGlobal.datos_completos, pageSize, currentPage);

    // Inicializar objetos para almacenar los totales de las columnas
    let totalesPagina = {};
    let totalesGlobales = {};

    // Inicializar los totales solo para las columnas que se deben sumar
    dataGlobal.campos_reporte.forEach(campo => {
        if (!columnasNoSumar.includes(campo)) {
            totalesPagina[campo] = 0;  // Totales de la página actual
            totalesGlobales[campo] = 0;  // Totales globales (de todos los datos)
        }
    });

    // Renderizar datos en el cuerpo de la tabla (tbody)
    if (paginatedData.length > 0) {
        const tbodyHTML = paginatedData.map((fila, index) => {
            const filaHTML = `
                <tr>
                    <th scope="row" class="numero-tabla">${(currentPage - 1) * pageSize + index + 1}</th>
                    ${dataGlobal.campos_reporte.map(campo => {
                        const value = fila[campo];
                        // Sumar a los totales de la página si es un número y no está en el arreglo columnasNoSumar
                        if (!isNaN(parseFloat(value)) && !columnasNoSumar.includes(campo)) {
                            totalesPagina[campo] += parseFloat(value);
                        }
                        return `<td class="datos-tabla">${formatNumber(value, false, campo)}</td>`;
                    }).join('')}
                </tr>
            `;
            return filaHTML;
        }).join('');
        tabla.innerHTML = tbodyHTML;

        // Calcular totales globales (para todos los datos)
        dataGlobal.datos_completos.forEach(fila => {
            dataGlobal.campos_reporte.map(campo => {
                const value = fila[campo];
                if (!isNaN(parseFloat(value)) && !columnasNoSumar.includes(campo)) {
                    totalesGlobales[campo] += parseFloat(value);
                }
            });
        });

        // Crear la fila de totales para la página actual
        const filaTotalPaginaHTML = `
            <tr>
                <th scope="row" class="numero-tabla" style="background-color:#00aae9;" style="background-color:#00aae9;">Total Página</th>
                ${dataGlobal.campos_reporte.map(campo => {
                    const totalValuePagina = (!isNaN(totalesPagina[campo]) && totalesPagina[campo] !== 0) ? formatNumber(totalesPagina[campo], false, campo) : '';
                    return `<td class="datos-tabla" style="background-color:#00aae9;" style="background-color:#00aae9;"><strong>${totalValuePagina}</strong></td>`;
                }).join('')}
            </tr>
        `;

        // Crear la fila de totales globales (de todas las páginas)
        const filaTotalGlobalHTML = `
            <tr>
                <th scope="row" class="numero-tabla" style="background-color:#00aae9;" style="background-color:#00aae9;">Total Global</th>
                ${dataGlobal.campos_reporte.map(campo => {
                    const totalValueGlobal = (!isNaN(totalesGlobales[campo]) && totalesGlobales[campo] !== 0) ? formatNumber(totalesGlobales[campo], false, campo) : '';
                    return `<td class="datos-tabla" style="background-color:#00aae9;" style="background-color:#00aae9;"><strong>${totalValueGlobal}</strong></td>`;
                }).join('')}
            </tr>
        `;

        // Agregar ambas filas de totales al final de la tabla
        tabla.innerHTML += filaTotalPaginaHTML + filaTotalGlobalHTML;

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
    const endPages = 2;   // Últimas páginas a mostrar
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
