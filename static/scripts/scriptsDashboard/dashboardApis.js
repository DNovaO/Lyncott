// dashboardApis.js

/*
Diego Nova Olguín
    Ultima modificación: 26/12/2024
    
    Script que contiene funciones de utilidad para el manejo de las llamadas a las multiples API para el dashboard.
    Permite una reutilización de código en otros scripts.
    Donde se enviaran los datos al servidor y se manejaran las respuestas para los contenedores del dashboard.
    
    Usando get para asi obtener los multiples datos.
    
*/

export async function apiVentasYDevoluciones(fecha, fecha_final) {
    // console.log('apiVentasYDevoluciones');
    const endpointURL = '/dashboard/';

    showLoaderContainer('loader-wrapper-ventas','body-venta-devoluciones'); // Mostrar el loader antes de la solicitud

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
                "Fecha_inicial": fecha,
                "Fecha_final": fecha_final,
            }),
        }).then(response => {
            hideLoaderContainer('loader-wrapper-ventas','body-venta-devoluciones'); // Ocultar el loader una vez que la petición se complete
            
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

    showLoaderContainer('loader-wrapper-estadisticas-rapidas','body-estadisticas-rapidas'); // Mostrar el loader antes de la solicitud

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
            hideLoaderContainer('loader-wrapper-estadisticas-rapidas', 'body-estadisticas-rapidas'); // Ocultar el loader una vez que la petición se complete
            
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

    showLoaderContainer('loader-wrapper-productos','body-distribucion-productos'); // Mostrar el loader antes de la solicitud

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
            hideLoaderContainer('loader-wrapper-productos','body-distribucion-productos'); // Ocultar el loader una vez que la petición se complete
            
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

    showLoaderContainer('loader-wrapper-autorizaciones-gastos','body-autorizaciones-gastos'); // Mostrar el loader antes de la solicitud

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
            hideLoaderContainer('loader-wrapper-autorizaciones-gastos','body-autorizaciones-gastos'); // Ocultar el loader una vez que la petición se complete
            
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

export function showLoaderContainer(containerID, bodyID) {
    const loaderWrapper = document.getElementById(containerID);  // Selecciona un solo elemento
    const cardBody = document.getElementById(bodyID);  // Selecciona un solo elemento
    
    if (cardBody){
        cardBody.style.opacity = 0.5;  // Reducir la opacidad del contenido mientras se carga el loader
        loaderWrapper.style.opacity = 1; 
    }

    if (loaderWrapper) {  // Asegúrate de que el elemento loaderWrapper existe
        loaderWrapper.innerHTML = `
            <p class="loading-text">Cargando...</p>
            <span class="loader-container"></span>
        `;
    }
}

export function hideLoaderContainer(containerID, bodyID) {
    const loaderWrapper = document.getElementById(containerID);  // Selecciona un solo elemento
    const cardBody = document.getElementById(bodyID);  // Selecciona un solo elemento

    if (cardBody){
        cardBody.style.opacity = 1;  // Restaurar la opacidad del contenido
    }
    
    if (loaderWrapper) {  // Asegúrate de que el elemento existe
        loaderWrapper.innerHTML = '';  // Elimina el contenido del loader
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
