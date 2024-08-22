// // paginado.js
// import { changePage } from './utils.js';

// export function renderPagination(paginationInfo, currentPage, dataType, isTable = false) {
//     let html = '<nav aria-label="Page navigation"><ul class="pagination justify-content-center">';

//     html += '<li class="page-item">';
//     if (paginationInfo && paginationInfo.has_previous) {
//         html += `<a class="page-link" onclick="changePage(1, '${dataType}', ${isTable})">&laquo;</a>`;
//     } else {
//         html += '<span class="page-link disabled" aria-disabled="true">&laquo;</span>';
//     }
//     html += '</li>';

//     html += '<li class="page-item">';
//     if (paginationInfo && paginationInfo.has_previous) {
//         html += `<a class="page-link" onclick="changePage(${paginationInfo.previous_page_number}, '${dataType}', ${isTable})">&lt;</a>`;
//     } else {
//         html += '<span class="page-link disabled" aria-disabled="true">&lt;</span>';
//     }
//     html += '</li>';

//     html += `<li class="page-item disabled"><span class="page-link">Page ${currentPage} of ${paginationInfo.num_pages}</span></li>`;

//     html += '<li class="page-item">';
//     if (paginationInfo && paginationInfo.has_next) {
//         html += `<a class="page-link" onclick="changePage(${paginationInfo.next_page_number}, '${dataType}', ${isTable})">&gt;</a>`;
//     } else {
//         html += '<span class="page-link disabled" aria-disabled="true">&gt;</span>';
//     }
//     html += '</li>';

//     html += '<li class="page-item">';
//     if (paginationInfo && paginationInfo.has_next) {
//         html += `<a class="page-link" onclick="changePage(${paginationInfo.num_pages}, '${dataType}', ${isTable})">&raquo;</a>`;
//     } else {
//         html += '<span class="page-link disabled" aria-disabled="true">&raquo;</span>';
//     }
//     html += '</li>';

//     html += '</ul></nav>';

//     return html;
// }


// // Exponer changePage globalmente
// window.changePage = changePage;

// // // Función para cambiar de página
// // export function changePageTabla(pageNumber) {
// //     const tipo_reporte = document.getElementById("tipo_reporte").textContent.trim();
// //     currentPageTable = pageNumber;
    
// //     sendParametersToServer(parametrosSeleccionados, currentPageTable, tipo_reporte);
// // } 

// export function renderPaginationTabla(paginationInfo, currentPageTable, dataType) {
//     return renderPagination(paginationInfo, currentPageTable, dataType, true);
// }


