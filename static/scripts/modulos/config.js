//config.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script que contiene las variables y elementos del DOM que se utilizan en los demás scripts.
    Siempre y cuando el script lo permita.

*/ 


export const parametrosReporte = document.getElementById("parametros-reporte");
export const modal = document.getElementById("genericModal");
export const modalLabel = modal.querySelector(".modal-title");
export const modalContent = modal.querySelector("#genericModalContent");
export const modalFooter = modal.querySelector("#genericModalPagination");
export const categoria_reporte = document.getElementById("categoria_reporte").textContent.trim();
export const tipo_reporte = document.getElementById("tipo_reporte").textContent.trim();
export const btnReset = document.getElementById('btnLimpiar');
export const btnGenerarInforme = document.getElementById('btnGenerarInforme');
export const btnMostrarFiltros = document.getElementById('btnMostrarFiltros');
export const btnBorrarReporte = document.getElementById('btnBorrarReporte');
export const btnExportarExcel = document.getElementById('btnExportarExcel');
export const btnExportarCSV = document.getElementById('btnExportarCSV');
export const btnImprimir = document.getElementById('btnImprimir');
export const btnMostrarGrafico = document.getElementById('btnMostrarGrafico');
export const fechaInicialInput = document.getElementById('fecha_inicial');
export const fechaFinalInput = document.getElementById('fecha_final');

