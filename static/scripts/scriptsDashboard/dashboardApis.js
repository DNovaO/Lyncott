// dashboardApis.js

/*
Diego Nova Olguín
    Ultima modificación: 26/12/2024
    
    Script que contiene funciones de utilidad para el manejo de las llamadas a las multiples API para el dashboard.
    Permite una reutilización de código en otros scripts.
    Donde se enviaran los datos al servidor y se manejaran las respuestas para los contenedores del dashboard.
    
    Usando get para asi obtener los multiples datos.
    
*/

export async function apiVentasYDevoluciones() {
    // console.log('apiVentasYDevoluciones');
    const endpointURL = '/dashboard/';

    showLoaderContainer('loader-wrapper-ventas'); // Mostrar el loader antes de la solicitud

    try {
        const response = await fetch(endpointURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body:JSON.stringify( {
                "Titulo": "Ventas y Devoluciones",
            }),
        }).then(response => {
            hideLoaderContainer('loader-wrapper-ventas'); // Ocultar el loader una vez que la petición se complete
            
            return response;
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error("Error en la solicitud:", error);
    } 
}

export async function estadisticasRapidas() {
    // console.log('estadisticasRapidas');
    const endpointURL = '/dashboard/';

    showLoaderContainer('loader-wrapper-estadisticas-rapidas'); // Mostrar el loader antes de la solicitud

    try {
        const response = await fetch(endpointURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body:JSON.stringify( { 
                "Titulo": "Estadisticas Rapidas",
            }),
        }).then(response => {
            hideLoaderContainer('loader-wrapper-estadisticas-rapidas'); // Ocultar el loader una vez que la petición se complete
            
            return response;
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
}

export async function distribucionVentas() {
    // console.log('distribucionVentas');
    const endpointURL = '/dashboard/';

    showLoaderContainer('loader-wrapper-productos'); // Mostrar el loader antes de la solicitud

    try {
        const response = await fetch(endpointURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body:JSON.stringify( {
                "Titulo": "Distribucion de Ventas",
            }),
        }).then(response => {
            hideLoaderContainer('loader-wrapper-productos'); // Ocultar el loader una vez que la petición se complete
            
            return response;
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error en la solicitud:", error);
    }
}

export async function autorizacionesGasto() {
    // console.log('autorizacionesGasto');
    const endpointURL = '/dashboard/';

    showLoaderContainer('loader-wrapper-autorizaciones-gastos'); // Mostrar el loader antes de la solicitud

    try {
        const response = await fetch(endpointURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body:JSON.stringify( {
                "Titulo": "Autorizaciones de Gasto",
            }),
        }).then(response => {
            hideLoaderContainer('loader-wrapper-autorizaciones-gastos'); // Ocultar el loader una vez que la petición se complete
            
            return response;
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error en la solicitud:", error);
    } finally {
        hideLoaderContainer('loader-wrapper-autorizaciones-gastos'); // Ocultar el loader una vez que la petición se complete
    }
}

function showLoaderContainer(containerID) {
    const loaderWrapper = document.getElementById(containerID);  // Selecciona un solo elemento

    if (loaderWrapper) {  // Asegúrate de que el elemento existe
        loaderWrapper.innerHTML = `
            <p class="loading-text">Cargando</p>
            <span class="loader-container"></span>
        `;
    }
}

function hideLoaderContainer(containerID) {
    const loaderWrapper = document.getElementById(containerID);  // Selecciona un solo elemento
    if (loaderWrapper) {  // Asegúrate de que el elemento existe
        loaderWrapper.innerHTML = '';  // Elimina el contenido del loader
        //Eliminar el loader del DOM
        loaderWrapper.remove();
    }
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
