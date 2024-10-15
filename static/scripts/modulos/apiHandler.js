// apiHandler.js
import { showLoaderModal, handleResponseData } from './renderModal.js';
import { showLoaderTabla, renderizarDatosEnTabla } from './renderTabla.js';
import { categoria_reporte, tipo_reporte } from './config.js';
import { cache } from './main.js';
import { getCookie } from './utils.js';

// Función para manejar llamadas a la API con cacheo
export async function fetchData(endpoint, body, cacheKey, prefetch = false) {

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

        return data;
    } catch (error) {
        console.error("Error:", error);
        if (!prefetch) throw error;
    }
}

// Función para enviar datos al servidor y manejar la respuesta
export function sendDataToServer(dataType, currentPage) {
    const endpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipo_reporte)}&page=${currentPage}`;
    const body = { data_type: dataType, page: currentPage };
    const cacheKey = `${dataType}_${currentPage}`;

    showLoaderModal();

    fetchData(endpointURL, body, cacheKey)
        .then(data => {
            handleResponseData(data);
            console.log('Los datos recibidos son:', data);
        })
        .catch(error => console.error("Error:", error));
}

// Función para enviar parámetros al servidor y manejar la respuesta
export function sendParametersToServer(parametrosInforme, currentPageTable, tipoReporte, btnGenerarInforme) {
    console.log('Parametros que fueron seleccionados y seran manipulados', parametrosInforme);

    const dataType = 'resultado';
    const endpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoria_reporte)}&tipo_reporte=${encodeURIComponent(tipoReporte)}&page=${currentPageTable}`;
    const body = { parametros_seleccionados: parametrosInforme, page: currentPageTable, tipo_reporte: tipoReporte, data_type: dataType };
    const cacheKey = `${tipoReporte}_${currentPageTable}`;

    showLoaderTabla();

    fetchData(endpointURL, body, cacheKey)
        .then(data => {
            renderizarDatosEnTabla(data, tipoReporte);
            console.log('Los datos recibidos son:', data);
        })
        .catch(error => console.error("Error:", error))
        .finally(() => {
            // Habilitar el botón después de completar la petición
            if (btnGenerarInforme) {
                btnGenerarInforme.disabled = false;
            }
        });
}
