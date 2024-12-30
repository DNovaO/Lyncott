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
    console.log('apiVentasYDevoluciones');
    const endpointURL = '/dashboard/';

    showLoader(); // Mostrar el loader antes de la solicitud

    try {
        const response = await fetch(endpointURL, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error("Error en la solicitud:", error);
    } finally {
        hideLoader(); // Ocultar el loader una vez que la petición se complete
    }
}

export async function estadisticasRapidas() {
    console.log('estadisticasRapidas');
    const endpointURL = '/dashboard/';

    showLoader(); // Mostrar el loader antes de la solicitud

    try {
        const response = await fetch(endpointURL, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error("Error en la solicitud:", error);
    } finally {
        hideLoader(); // Ocultar el loader una vez que la petición se complete
    }
}

export async function distribucionVentas() {
    console.log('distribucionVentas');
    const endpointURL = '/dashboard/';

    showLoader(); // Mostrar el loader antes de la solicitud

    try {
        const response = await fetch(endpointURL, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error("Error en la solicitud:", error);
    } finally {
        hideLoader(); // Ocultar el loader una vez que la petición se complete
    }
}

export async function autorizacionesGasto() {
    console.log('autorizacionesGasto');
    const endpointURL = '/dashboard/';

    showLoader(); // Mostrar el loader antes de la solicitud

    try {
        const response = await fetch(endpointURL, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error("Error en la solicitud:", error);
    } finally {
        hideLoader(); // Ocultar el loader una vez que la petición se complete
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

function showLoader() {
    const loaderWrapper = document.getElementsByClassName('loader-wrapper');

    loaderWrapper.innerHTML = `
        <p class="loading-text">Cargando</p>
        <span class="loader-container"></span>
    `;

}

function hideLoader() {
    const loaderWrapper = document.getElementsByClassName('loader-wrapper');
    loaderWrapper.innerHTML = '';  
}

