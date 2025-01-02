import { apiVentasYDevoluciones, estadisticasRapidas, distribucionVentas, autorizacionesGasto } from './dashboardApis.js';

import { manejarVentasYDevoluciones } from './manejoVentasDevoluciones.js';
import { manejarEstadisticasRapidas } from './manejoEstadisticasRapidas.js';
import { manejarDistribucionVentas } from './manejoDistribucionVentas.js';
import { manejarAutorizacionesGasto } from './manejoAutorizacionesGastos.js';


document.addEventListener('DOMContentLoaded', function () {
    showLoader();  // Mostrar el loader al iniciar

    // Variables para contar las respuestas
    let respuestasCompletadas = 0;
    const umbralMinimo = 2;  // Número mínimo de respuestas exitosas para ocultar el loader

    // Función para manejar el contador de respuestas y ocultar el loader
    function manejarRespuesta() {
        respuestasCompletadas++;
        if (respuestasCompletadas >= umbralMinimo) {
            hideLoader(); // Ocultar el loader si el umbral mínimo se alcanza
        }
    }

    // Array de promesas
    const promesas = [
        apiVentasYDevoluciones(),
        estadisticasRapidas(),
        distribucionVentas(),
        autorizacionesGasto()
    ];

    // Ejecutar cada promesa individualmente
    promesas.forEach(promesa => {
        promesa
            .then(response => {
                if (response) {
                    manejarRespuesta(); // Incrementar el contador si la respuesta es válida
                    manejoDatosDashboard(response);  // Manejar los datos del dashboard
                }
            })
            .catch(error => {
                console.error('Error en una solicitud:', error);
                // Si decides manejar errores de otro modo, puedes hacerlo aquí
            });
    });
});

function manejoDatosDashboard(data) {
    const { titulo } = data;

    // Diccionario de títulos y sus funciones correspondientes
    const manejadores = {
        'Ventas y Devoluciones': manejarVentasYDevoluciones,
        'Estadisticas Rapidas': manejarEstadisticasRapidas,
        'Distribucion de Ventas': manejarDistribucionVentas,
        'Autorizaciones de Gasto': manejarAutorizacionesGasto,
    };

    // Verifica si existe un manejador para el título y lo ejecuta
    const manejarFuncion = manejadores[titulo];
    if (manejarFuncion) {
        manejarFuncion(data);
    } else {
        console.error('Título no reconocido:', titulo);
    }
}

function showLoader() {
    const loaderDiv = document.getElementById('loader');
    loaderDiv.innerHTML = `
        <div class="lds-ellipsis-container">
            <h1 class="loading-text">Cargando datos del dashboard</h1>
            <div class="lds-ellipsis" style="margin: 0 auto;">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
    `;
    document.body.appendChild(loaderDiv);  // Aseguramos que el loader esté visible en el body
}

function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.remove();  // Eliminamos el loader del DOM
    }
}
