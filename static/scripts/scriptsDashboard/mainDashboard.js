import { apiVentasYDevoluciones, estadisticasRapidas, distribucionVentas, autorizacionesGasto } from './dashboardApis.js';

document.addEventListener('DOMContentLoaded', function () {
    showLoader();  // Mostrar el loader al iniciar

    // Usamos Promise.all para manejar las solicitudes de API simultáneamente
    Promise.all([apiVentasYDevoluciones(), estadisticasRapidas(), distribucionVentas(), autorizacionesGasto()])
        .then(([ventasYDevoluciones, estadisticas, distribucion, autorizaciones]) => {
            console.log(ventasYDevoluciones);
            console.log(estadisticas);
            console.log(distribucion);
            console.log(autorizaciones);

            hideLoader();  // Ocultar el loader cuando todas las promesas se resuelvan
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
        });
});

function showLoader() {
    const loaderDiv = document.getElementById('loader');
    console.log('Loader cargando');
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
    console.log('loader oculto');
    if (loader) {
        loader.remove();  // Eliminamos el loader del DOM
    }
}
