// renderTabla.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script que se encarga de renderizar los datos en la tabla, paginarlos y mostrar los totales.
    Además, se encarga de manejar el control de los botones de exportar los datos a CSV y Excel, e imprimir la información en la 
    tabla.
    
*/ 


import { formatNumber, transformHeader } from './utils.js';
import { exportToCSV, exportToExcel, imprimirInformacion } from "./exportaciones.js";
import { btnExportarCSV , btnExportarExcel, btnImprimir, btnMostrarGrafico, tipo_reporte} from "./config.js"
import { mostrarGrafico } from "./graficas.js";
import { currentPage } from './main.js';
import { datosParaBuscador } from './apiHandler.js';
import { setCancelFetch } from './breaker.js';

let debouncedBuscadorReportes;
let totalesPagina = {};
let totalesGlobales = {};
let dataGlobal;
let mensajeError;

document.addEventListener("DOMContentLoaded", function () {

    debouncedBuscadorReportes = debouncedReportes(() => {
        buscadorResultadosReporte(datosParaBuscador);
    }, 300);

    window.debouncedBuscadorReportes = debouncedBuscadorReportes;

    if (btnExportarCSV) {
        btnExportarCSV.addEventListener('click', function (e) {
            const datosNoDisponiblesElement = document.getElementById("datos-no-disponibles");
            const datosNoDisponiblesText = datosNoDisponiblesElement ? datosNoDisponiblesElement.textContent : null;

            try {
                if (!datos || datos.length === 0 || datos === '') {
                    throw new Error("No hay un reporte disponible para exportar a CSV.");
                }
                if (datosNoDisponiblesText === 'No hay datos disponibles') {
                    throw new Error("No hay un reporte disponible para exportar a CSV.");
                }
                console.log('Exportando a CSV', datos);
                exportToCSV(datos, tipo_reporte);
            } catch (error) {
                mensajeError = "No hay un reporte disponible para exportar a CSV.";
                mostrarAlertaHTML(mensajeError);
            }
        });
    }

    if (btnExportarExcel) {
        btnExportarExcel.addEventListener('click', function (e) {
            const datosNoDisponiblesElement = document.getElementById("datos-no-disponibles");
            const datosNoDisponiblesText = datosNoDisponiblesElement ? datosNoDisponiblesElement.textContent : null;

            try {
                if (!datos || datos.length === 0) {
                    throw new Error("No hay un reporte disponible para exportar a Excel.");
                }
                if (datosNoDisponiblesText === 'No hay datos disponibles') {
                    throw new Error("No hay un reporte disponible para exportar a Excel.");
                }
                console.log('Exportando a Excel', datos);
                exportToExcel(datos, tipo_reporte);
            } catch (error) {
                mensajeError = "No hay un reporte disponible para exportar a Excel.";
                mostrarAlertaHTML(mensajeError);
            }
        });
    }

    if (btnImprimir) {
        btnImprimir.addEventListener('click', function (e) {
            const datosNoDisponiblesElement = document.getElementById("datos-no-disponibles");
            const datosNoDisponiblesText = datosNoDisponiblesElement ? datosNoDisponiblesElement.textContent : null;

            try {
                if (!datos || datos.length === 0) {
                    throw new Error("No hay información para imprimir.");
                }
                if (datosNoDisponiblesText === 'No hay datos disponibles') {
                    throw new Error("No hay información para imprimir.");
                }
                imprimirInformacion(datos, tipo_reporte);
            } catch (error) {
                mensajeError = "No hay un reporte para imprimir.";
                mostrarAlertaHTML(mensajeError);
            }
        });
    }

    if (btnMostrarGrafico) {
        btnMostrarGrafico.addEventListener('click', function (e) {
            const datosNoDisponiblesElement = document.getElementById("datos-no-disponibles");
            const datosNoDisponiblesText = datosNoDisponiblesElement ? datosNoDisponiblesElement.textContent : null;

            try {
                if (!datos || datos.length === 0) {
                    throw new Error("No hay datos para mostrar en el gráfico.");
                }
                if (datosNoDisponiblesText === 'No hay datos disponibles') {
                    throw new Error("No hay datos para mostrar en el gráfico.");
                }
                mostrarGrafico(dataGlobal, tipo_reporte);
            } catch (error) {
                mensajeError = "No hay datos para mostrar en el gráfico.";
                mostrarAlertaHTML(mensajeError);
            }
        });
    }

    const thead = document.querySelector('thead');
    if (thead) {
        // Escucha eventos en el `thead`
        thead.addEventListener('click', (event) => {
            const button = event.target.closest('.btnPin'); // Busca el botón clicado
            if (button) {
                const columna = parseInt(button.dataset.columnIndex, 10); // Obtén el índice de la columna
                const filas = document.querySelectorAll('.table tr');

                // Alterna la clase `pinned` para las celdas de la columna
                filas.forEach(row => {
                    const cell = row.children[columna + 1]; // Ajusta al índice correcto
                    if (cell) {
                        cell.classList.toggle('pinned');
                    }
                });

                // Actualiza los desplazamientos de todas las columnas fijadas
                actualizarColumnasFijadas();

                // Alternar visualmente el botón (opcional)
                const pinIcon = button.querySelector('.pin-column-btn');
                if (pinIcon) {
                    pinIcon.classList.toggle('active');
                }
            }
        });
    }
});

// Función para actualizar las columnas fijadas
function actualizarColumnasFijadas() {
    const filas = document.querySelectorAll('.table tr');

    filas.forEach(row => {
        let acumuladoLeft = 0;
        row.querySelectorAll('.pinned').forEach(cell => {
            cell.style.left = `${acumuladoLeft}px`;
            acumuladoLeft += cell.offsetWidth; // Sumar el ancho de la columna actual
        });
    });
}

// Función para mostrar alerta personalizada en HTML
export function mostrarAlertaHTML(mensaje) {
    const tabla = document.querySelector('.table tbody');
    const loader = document.querySelector('.lds-ellipsis');
    
    if (!tabla) {
        console.error('No hay datos disponibles');
        return;
    }

    // Crear la fila de alerta
    const alertaFila = document.createElement('tr');
    
    // Limpiar el loader si existe
    if (loader) {
        loader.innerHTML = ''; 
    }

    alertaFila.innerHTML = ` 
        <td colspan="50%" class="text-center alert alert-danger" style="background-color: #f8d7da; color: #721c24; padding: 15px; font-weight: bold;">
            ${mensaje}
        </td>
    `;

    // Insertar la alerta en la tabla
    tabla.insertBefore(alertaFila, tabla.firstChild);

    // Remover la alerta automáticamente después de 3 segundos
    setTimeout(() => {
        alertaFila.remove();
        
        // Verifica si no hay más datos en la tabla y muestra un mensaje si es el caso
        if (tabla.rows.length === 1) { // Solo hay la fila de alerta
            tabla.innerHTML = `<tr><td colspan="50%" class="text-center" id="datos-no-disponibles">No hay datos disponibles</td></tr>`;
        }
    }, 3000);
}



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

window.cambiarResultadosPorPagina = cambiarResultadosPorPagina;

function cambiarResultadosPorPagina() {
    const selectElement = document.getElementById('resultadosPorPagina');
    const pageSize = selectElement.value === 'all' 
        ? dataGlobal.datos_completos.length 
        : parseInt(selectElement.value, 10);

    const currentPage = 1;

    // Guardar valores en sessionStorage
    sessionStorage.setItem('pageSize', pageSize);
    sessionStorage.setItem('currentPage', currentPage);

    renderizarDatosEnTabla(dataGlobal, 'dataType', currentPage, pageSize);
}

export function renderizarDatosEnTabla(data, dataType, currentPage = 1, pageSize = 10,
    columnasNoSumar = ['clave_producto', 'descripcion_producto', 'producto', 'sucursal',
        'clave', 'clave_sucursal', 'numero_tipo_documento', 'grupo_movimiento',
        'detalles_tipo_documento', 'almacen_correspondiente', 'moneda', 'zona',
        'orden', 'orden_fecha', 'numero_folio', 'partes_folio', 'partes_fecha',
        'termina_folio', 'nombre', 'zona', 'nombre_producto', 'UPC', 'linea',
        'Promedio_Cliente', 'Promedio_Consignatario', 'fecha', 'dia', 'clave_cliente',
        'consignatario', 'segmentacion', 'clave_grupo_corporativo', 'clave_cliente',
        'clave_consignatario', 'producto', 'No', 'id_vendedor', 'id_almacen',
        'vendedor', 'id_grupo_corporativo', 'grupo_corporativo', 'id_consignatario',
        'consignatario', 'CP', 'colonia', 'folio', 'RFC', 'UUID', 'serie',
        'clave_vendedor', 'nombre_vendedor', 'numero_mes', 'zona_vendedor',
        'nombre_cliente', 'descripcion', 'cliente', 'grupo','folio_facturas','tipo_documento', 'folio_documento', 'clave_vendedor', 'grupo_documento_anexado', 'tipo_documento_anexado', 'folio_documento_anexado', 'genero', 'naturaleza', 'referencia','giro','segmento','nombre_consignatario', 'nombre_grupo'
    ]) {

    const keysToExcludeFromFormatting = ['clave_producto', 'descripcion_producto', 'producto','sucursal', 
        'clave', 'clave_sucursal', 'numero_tipo_documento', 'grupo_movimiento',
        'detalles_tipo_documento', 'almacen_correspondiente', 'moneda','zona',
        'orden', 'orden_fecha', 'numero_folio', 'partes_folio', 'partes_fecha',
        'termina_folio', 'nombre', 'zona', 'nombre_producto','UPC','linea',
        'Promedio_Cliente', 'Promedio_Consignatario', 'fecha', 'dia','clave_cliente', 'consignatario', 'segmentacion', 'clave_grupo_corporativo', 'clave_cliente', 'clave_consignatario', 'producto', 'No', 'id_vendedor', 'id_almacen','vendedor','id_grupo_corporativo','grupo_corporativo',
        'id_consignatario', 'consignatario', 'CP', 'colonia', 'cantidad','folio','RFC', 'UUID', 'serie','clave_vendedor','cliente', 'nombre_vendedor','numero_mes', 'zona_vendedor', 'nombre_cliente', 'descripcion', 'grupo', 'folio_facturas','tipo_documento', 'folio_documento','clave_vendedor', 'grupo_documento_anexado', 'tipo_documento_anexado', 'folio_documento_anexado','naturaleza_documento_anexado', 'genero', 'naturaleza', 'referencia', 'cadena', 'KAM','giro','segmento','nombre_consignatario', 'clave_grupo', 'familia'
    ];
    
    // Almacenar los datos globalmente
    dataGlobal = data;
    window.datos = dataGlobal;

    const separadoresHabilitados = (dataGlobal.campos_reporte.includes("zona"));
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
            ${dataGlobal.campos_reporte.map((campo, index) => {
                const transformedHeader = transformHeader(campo);
                return `
                    <th scope="col" class="datos-tabla" style="justify-content:center; text-align:left; display:table-cell; white-space:nowrap;">
                        ${transformedHeader}
                        <button type="submit" class="btnPin" data-column-index="${index}">
                            <svg class="pin-column-btn" width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd" clip-rule="evenodd" d="M6.5 5C6.5 4.44772 6.94772 4 7.5 4H9H15H16.5C17.0523 4 17.5 4.44772 17.5 5C17.5 5.55228 17.0523 6 16.5 6H16.095L16.9132 15H19C19.5523 15 20 15.4477 20 16C20 16.5523 19.5523 17 19 17H16H13V22C13 22.5523 12.5523 23 12 23C11.4477 23 11 22.5523 11 22V17H8H5C4.44772 17 4 16.5523 4 16C4 15.4477 4.44772 15 5 15H7.08679L7.90497 6H7.5C6.94772 6 6.5 5.55228 6.5 5ZM9.91321 6L9.09503 15H12H14.905L14.0868 6H9.91321Z"/>
                            </svg>
                        </button>
                    </th>
                `;
            }).join('')}
        </tr>
    `;

    thead.innerHTML = theadHTML;

    // Función para eliminar separadores de miles y convertir a número
    function limpiarYConvertir(value) {
        if (typeof value === 'string') {
            value = value.replace(/,/g, ''); // Eliminar comas
        }
        return parseFloat(value) || 0; // Convertir a número o devolver 0 si no es válido
    }

    const paginatedData = paginarDatos(dataGlobal.datos_completos, pageSize, currentPage);

    if (!paginatedData.length) {
        tabla.innerHTML = `<tr><td id="datos-no-disponibles" colspan="${dataGlobal.campos_reporte.length + 1}" class="text-center">No hay datos disponibles</td></tr>`;
        return;
    }

    let zonaActual = "";
    let totalesPorZona = {};
    let totalesPagina = {};
    let totalesGlobales = {};

    // Inicializar los totales solo para las columnas que se deben sumar
    dataGlobal.campos_reporte.forEach(campo => {
        if (!columnasNoSumar.includes(campo)) {
            totalesPagina[campo] = 0;  // Totales de la página actual
            totalesGlobales[campo] = 0;  // Totales globales
            totalesPorZona[campo] = 0;  // Totales por zona
        }
    });

    // Función para generar fila de totales por zona
    function generarTotalesZona(zona) {
        return `
            <tr class="total-zona" style="background-color: rgba(0, 170, 233, 0.5); font-weight:500; justify-content:right;">
                <th class="separador-zona" style="background-color: rgba(0, 170, 233, 0.5); font-weight:500;">Total: ${transformHeader(zona)}</th>
                ${dataGlobal.campos_reporte.map(campo => {
                    const totalValueZona = (!isNaN(totalesPorZona[campo]) && totalesPorZona[campo] !== 0)
                        ? formatNumber(totalesPorZona[campo], false, campo)
                        : '';
                    return `<td class="datos-tabla" style="background-color: rgba(0, 170, 233, 0.5); text-align:right;"><strong>${totalValueZona}</strong></td>`;
                }).join('')}
            </tr>
        `;
    }
    

    const tbodyHTML = paginatedData.map((fila, index) => {
        let separadorZona = "";
        let totalesZonaFila = "";

        // Detectar cambio de zona
        if (separadoresHabilitados && fila.zona !== zonaActual) {
            if (zonaActual) {
                totalesZonaFila = generarTotalesZona(zonaActual);
            }

            separadorZona = `
                <tr class="separador-zona" style="background-color: rgba(112, 224, 0, 1);">
                    <th colspan="${dataGlobal.campos_reporte.length + 1}" style="justify-content:left; font-weight:500; background-color: rgba(112, 224, 0, 0.8);">
                        Zona: ${fila.zona}
                    </th>
                </tr>
            `;
        
            zonaActual = fila.zona;
            dataGlobal.campos_reporte.forEach(campo => {
                if (!columnasNoSumar.includes(campo)) {
                    totalesPorZona[campo] = 0;
                }
            });
        }

        dataGlobal.campos_reporte.forEach(campo => {
            const value = limpiarYConvertir(fila[campo]);
            if (!isNaN(value) && !columnasNoSumar.includes(campo)) {
                totalesPorZona[campo] += value;
                totalesPagina[campo] += value;
            }
        });

        const filaHTML = `
            <tr>
                <th scope="row" class="numero-tabla">${(currentPage - 1) * pageSize + index + 1}</th>
                ${dataGlobal.campos_reporte.map(campo => {
                    let alignmentStyle = ''; // Inicializa la variable para el estilo adicional
                    if (!keysToExcludeFromFormatting.includes(campo)) {
                        alignmentStyle = 'text-align: right;'; // Aplica alineación centrada si no está excluido
                    }

                    const defaultStyle = 'display: table-cell; white-space: nowrap; text-align: left;'; // Estilo predeterminado

                    return `
                        <td class="datos-table" style="${defaultStyle} ${alignmentStyle}">
                            ${formatNumber(fila[campo], false, campo)}
                        </td>`;
                }).join('')}
            </tr>
        `;
        
        return totalesZonaFila + separadorZona + filaHTML;
    }).join('');

    dataGlobal.datos_completos.forEach(fila => {
        dataGlobal.campos_reporte.forEach(campo => {
            const value = limpiarYConvertir(fila[campo]);
            if (!isNaN(value) && !columnasNoSumar.includes(campo)) {
                totalesGlobales[campo] += value;
            }
        });
    });

    const totalesUltimaZona = generarTotalesZona(zonaActual);

    const filaTotalPaginaHTML = `
        <tr id="total-pagina" style="background-color: rgba(0, 170, 233, 0.5); font-weight:500;">
            <th colspan="1" style="background-color: rgba(0, 170, 233, 0.5); font-weight:500;">Total Página</th>
            ${dataGlobal.campos_reporte.map(campo => {
                const totalValuePagina = (!isNaN(totalesPagina[campo]) && totalesPagina[campo] !== 0)
                    ? formatNumber(totalesPagina[campo].toFixed(2), false, campo) : '';
                return `<td class="datos-tabla" style="background-color: rgba(0, 170, 233, 0.5); font-weight:500; text-align:right;"><strong>${totalValuePagina}</strong></td>`;
            }).join('')}
        </tr>
    `;

    const filaTotalGlobalHTML = `
        <tr id="total-global" style="background-color: rgba(0, 170, 233, 0.5); font-weight:500;">
            <th colspan="1" style="background-color: rgba(0, 170, 233, 0.5); font-weight:500; text-align:right;">Total Global</th>
            ${dataGlobal.campos_reporte.map(campo => {
                const totalValueGlobal = (!isNaN(totalesGlobales[campo]) && totalesGlobales[campo] !== 0)
                    ? formatNumber(totalesGlobales[campo].toFixed(2), false, campo) : '';
                return `<td class="datos-tabla" style="background-color: rgba(0, 170, 233, 0.5); font-weight:500; text-align:right;"><strong>${totalValueGlobal}</strong></td>`;
            }).join('')}
        </tr>
    `;

    if (separadoresHabilitados){
        tabla.innerHTML += tbodyHTML + totalesUltimaZona + filaTotalPaginaHTML + filaTotalGlobalHTML;
    } else {
        tabla.innerHTML += tbodyHTML + filaTotalPaginaHTML + filaTotalGlobalHTML;
    }
    tablaFooter.innerHTML = renderPaginadoTabla({
        totalPages: Math.ceil(dataGlobal.datos_completos.length / pageSize),
        currentPage: currentPage
    }, currentPage, dataType);
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
        event.preventDefault();
    }

    // Guardar la página actual en sessionStorage
    sessionStorage.setItem('currentPage', pageNumber);

    const pageSize = parseInt(sessionStorage.getItem('pageSize'), 10) || 10;
    renderizarDatosEnTabla(dataGlobal, dataType, pageNumber, pageSize);
}

window.cambiarPagina = cambiarPagina;

export function resetTabla() {
    const tabla = document.querySelector('.table tbody');
    const thead = document.querySelector('.table thead');
    const tablaFooter = document.getElementById('genericTablaPagination');
    const graphContainer = document.getElementById('tablaGraphContainer');
    
    // Limpiar encabezado y cuerpo de la tabla
    thead.innerHTML = '';
    tabla.innerHTML = '';

    // Establecer la variable de control para cancelar cualquier fetch en proceso
    setCancelFetch(true);

    const theadHTML = `
        <tr>
            <th scope="col">#</th>
        </tr>
    `;

    thead.innerHTML = theadHTML;
    tabla.innerHTML = `<tr class="alert alert-success" role="alert"><td class="text-center">¡Reporte eliminado con éxito!</td></tr>`;
    tablaFooter.innerHTML = '';

    // Limpiar la gráfica
    if (graphContainer) {
        graphContainer.remove(); // Eliminar el contenedor de la gráfica
    }

    // Limpiar los datos globales
    window.datos = []; // Limpiar los datos del reporte
    window.dataGlobal = []; // Limpiar los datos globales para gráficos
}



function debouncedReportes(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

function buscadorResultadosReporte(datosParaBuscador) {
    let input = document.getElementById("inputBusquedaReportes"); 
    let graphContainer = document.getElementById('tablaGraphContainer');
    
    // Limpiar la gráfica
    if (graphContainer) {
        graphContainer.remove(); // Eliminar el contenedor de la gráfica
    }

    if (!input) {
        console.error("No se encontró el elemento de input");
        return;
    }
    
    const currentPage = 1; // Reiniciamos siempre a la primera página
    let filter = input.value.trim().toLowerCase();

    // Manejar la búsqueda vacía
    if (filter === "") {
        renderizarDatosEnTabla(datosParaBuscador, 'dataType', currentPage);
        return;
    }

    // Filtrar los datos si es necesario
    const dataFiltered = datosParaBuscador.datos_completos.filter(fila => 
        datosParaBuscador.campos_reporte.some(campo => {
            const valorCampo = fila[campo];
            // Verificar que valorCampo no sea null o undefined
            return valorCampo && valorCampo.toString().toLowerCase().includes(filter);
        })
    );


    // Renderizar los datos filtrados
    renderizarDatosEnTabla(
        { ...datosParaBuscador, datos_completos: dataFiltered },
        'dataType',
        currentPage
    );
}