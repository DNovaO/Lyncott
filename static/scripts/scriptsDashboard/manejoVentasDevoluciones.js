import { apiVentasYDevoluciones, hideLoaderContainer,  showLoaderContainer } from './dashboardApis.js';
import { flatpickrdate } from './utilsDashboard.js';

export function manejarVentasYDevoluciones(datos) {
    console.log('Datos desde el manejo del API de ventas y devoluciones', datos);

    // Verifica si el gráfico ya existe y destrúyelo (para evitar superposiciones)
    const canvas = document.getElementById('barChart');
    if (!canvas) {
        console.error('El elemento canvas con id "barChart" no se encontró.');
        return;
    }

    const existingChart = Chart.getChart(canvas);
    if (existingChart) {
        existingChart.destroy();
    }

    // Extraer los datos para la gráfica
    if (datos.status !== "ok" || !datos.ventas || !Array.isArray(datos.ventas)) {
        console.error('Datos no válidos recibidos desde el API:', datos);
        return;
    }

    const ventasData = datos.ventas[0]; // Extraer el primer objeto del array de ventas
    const labels = ['Ventas', 'Devoluciones']; // Etiquetas para las barras
    const ventas = ventasData.ventas || 0; // Valor de ventas
    const devoluciones = ventasData.devoluciones || 0; // Valor de devoluciones
    const valores = [ventas, devoluciones]; // Agrupar los datos para la gráfica

    // Renderizar la gráfica
    new Chart(canvas, {
        type: 'pie',  // Tipo de gráfico 'pie'
        data: {
            labels: labels, // Etiquetas de las categorías
            datasets: [
                {
                    label: 'Monto en Pesos (MXN)',
                    data: valores, // Los valores que quieres graficar
                    backgroundColor: [
                        'rgba(53, 163, 236, 0.7)', // Color para 'Ventas'
                        'rgba(255, 61, 103, 0.7)', // Color para 'Devoluciones'
                    ],
                    borderColor: [
                        'rgb(0, 153, 255)',  // Borde para 'Ventas'
                        'rgb(255, 0, 55)',  // Borde para 'Devoluciones'
                    ],
                    borderWidth: 1,
                    hoverBackgroundColor: [
                        'rgba(53, 163, 236, 1)',  // Color de hover para 'Ventas'
                        'rgba(255, 61, 103, 1)',  // Color de hover para 'Devoluciones'
                    ],
                    hoverBorderColor: [
                        'rgb(53, 163, 236)',  // Borde de hover para 'Ventas'
                        'rgb(255, 61, 103)',  // Borde de hover para 'Devoluciones'
                    ],
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',  // Coloca la leyenda en la parte superior del gráfico
                    labels: {
                        font: {
                            size: 14,  // Tamaño de la fuente de la leyenda
                        },
                        color: '#333',  // Color del texto de la leyenda
                    },
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const percentage = context.raw / valores.reduce((acc, val) => acc + val, 0) * 100;
                            return `${label}: $${value.toLocaleString('es-MX')} (${percentage.toFixed(2)}%)`; // Muestra valores y porcentaje
                        },
                    },
                    backgroundColor: 'rgba(0, 0, 0, 0.7)', // Fondo del tooltip
                    titleFont: {
                        size: 16,  // Tamaño de la fuente del título del tooltip
                    },
                    bodyFont: {
                        size: 14,  // Tamaño de la fuente del contenido del tooltip
                    },
                    displayColors: false,  // Desactiva los cuadros de colores en el tooltip
                },
            },
        },
    });

    // Después de que el gráfico se haya generado, agregar el resumen
    setTimeout(() => {
        const resumenHtml = document.getElementById('resumen-grafica');  // Obtener el contenedor del resumen
        const resumenHtmlnumeros = document.getElementById('resumen-grafica-numeros');  // Obtener el contenedor del resumen

        if (resumenHtml) {
            resumenHtml.innerHTML = `
                <h5 class="mb-1 text-center">Resumen de periodo</h5>

                <div class="container text-center">    
                    <div class="date-container">
                        <label for="fecha_inicial" class="date-label">Fecha inicial:</label>
                        <div class="date-input-wrapper">
                            <input type="text" id="fecha_inicial" name="fecha_inicial" class="form-control" />
                            <i class="fas fa-calendar-alt calendar-icon" id="calendar-icon-inicial"></i>
                        </div>
                    </div>
                </div>

            `;

            resumenHtmlnumeros.innerHTML = `
                <div class="resumen-numeros">
                    <p class="text-center mt-2">
                    <strong>Total ventas:</strong> <span id="ventasData">$${ventas.toLocaleString('es-MX')}</span>
                    </p>
                    <p class="text-center mt-2">
                    <strong>Total devoluciones:</strong> <span id="devolucionesData">$${devoluciones.toLocaleString('es-MX')}</span>
                    </p>
                </div>
            `;

            // Agregar funcionalidad al ícono para abrir el selector
            const calendarIconInicial = document.getElementById('calendar-icon-inicial');
            if (calendarIconInicial) {
                calendarIconInicial.addEventListener('click', () => {
                    document.getElementById('fecha_inicial').focus();
                });
            }

            // Esperar un poco antes de activar la transición
            setTimeout(() => {
                const fechaInput = document.getElementById('fecha_inicial');
                if (fechaInput) {
                    fechaInput.addEventListener('change', function () {
                        const fecha = fechaInput.value;  // Obtener el valor actualizado del input
                        console.log('Fecha seleccionada:', fecha);  // Mostrar la fecha actualizada
                        recargarDatos(fecha);
                    });
                }

                flatpickrdate();
                resumenHtml.classList.add('visible'); 
                resumenHtmlnumeros.classList.add('visible');  
            }, 100);  // Retraso corto para permitir que el contenido se cargue antes de la animación
        } else {
            console.error('No se encontró el contenedor con id "resumen-grafica"');
        }
    }, 50);  // Tiempo de espera para asegurarse de que la gráfica se haya renderizado
}

function recargarDatos(fecha) {
    showLoaderContainer('loader-wrapper-ventas', 'body-venta-devoluciones');
    apiVentasYDevoluciones(fecha)
        .then(response => {
            if (response) {
                manejarVentasYDevoluciones(response);
            }
        })
        .catch(error => {
            console.error('Error al recargar los datos:', error);
        }).finally(() => {
            hideLoaderContainer('loader-wrapper-ventas','body-venta-devoluciones');
        });
}
