import { apiVentasYDevoluciones, hideLoaderContainer, showLoaderContainer } from './dashboardApis.js';
import { errorParametros, flatpickrdate } from './utilsDashboard.js';

let isReloading = false;  // Flag to track if a reload is in progress
let fecha_inicial_actual = null;
let fecha_final_actual = null;

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

    const ventasData = datos.ventas && datos.ventas[0] ? datos.ventas[0] : { ventas: 0, devoluciones: 0 };
    const labels = ['Ventas', 'Devoluciones']; // Etiquetas para las barras
    const ventas = typeof ventasData.ventas === 'number' && !isNaN(ventasData.ventas) ? ventasData.ventas : 0;
    const devoluciones = typeof ventasData.devoluciones === 'number' && !isNaN(ventasData.devoluciones) ? ventasData.devoluciones : 0;
    const valores = [ventas, devoluciones]; // Agrupar los datos para la gráfica

    // Renderizar la gráfica
    new Chart(canvas, {
        type: 'bar', // Tipo de gráfico 'bar' (barras)
        data: {
            labels: labels, // Etiquetas de las categorías
            datasets: [
                {

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
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'x', // Eje horizontal
            plugins: {
                legend: {
                    display: false, // Ocultar la leyenda
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
                        size: 16, // Tamaño de la fuente del título del tooltip
                    },
                    bodyFont: {
                        size: 14, // Tamaño de la fuente del contenido del tooltip
                    },
                    displayColors: false, // Desactiva los cuadros de colores en el tooltip
                },
            },
        },
        plugins: [
            {
                id: 'customLabels', // Identificador del plugin
                afterDatasetsDraw: (chart) => {
                    const { ctx, chartArea: { top }, scales: { x, y } } = chart;

                    chart.data.datasets[0].data.forEach((value, index) => {
                        const barX = x.getPixelForValue(index); // Posición en el eje X
                        const barY = y.getPixelForValue(value); // Posición en el eje Y
                        const label = `$${value.toLocaleString('es-MX')}`; // Valor formateado en MXN

                        ctx.save();
                        ctx.fillStyle = chart.data.datasets[0].backgroundColor[index]; // Color según la barra
                        ctx.font = 'bold 12px Arial'; // Fuente del texto
                        ctx.textAlign = 'center';
                        ctx.fillText(label, barX, barY - 10); // Dibuja el texto encima de la barra
                        ctx.restore();
                    });
                },
            },
        ],
    });

        

    // Después de que el gráfico se haya generado, agregar el resumen
    setTimeout(() => {
        const resumenHtml = document.getElementById('resumen-grafica');  // Obtener el contenedor del resumen
        const resumenHtmlnumeros = document.getElementById('resumen-grafica-numeros');  // Obtener el contenedor del resumen

        if (resumenHtml) {
            resumenHtml.innerHTML = `
                <h4 class="mb-1 text-center">Resumen de periodo</h4>

                <div class="container mb-2">
                    <!-- Fila para las fechas -->
                    <div class="row g-3 align-items-center justify-content-center">
                        <div class="col-md-6">
                            <div class="date-container">
                                <label for="fecha_inicial" class="date-label">Fecha inicial:</label>
                                <div class="date-input-wrapper">
                                    <input type="text" id="fecha_inicial" name="fecha_inicial" class="form-control" />
                                    <i class="fas fa-calendar-alt calendar-icon" id="calendar-icon-inicial"></i>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="date-container">
                                <label for="fecha_final" class="date-label">Fecha final:</label>
                                <div class="date-input-wrapper">
                                    <input type="text" id="fecha_final" name="fecha_final" class="form-control" />
                                    <i class="fas fa-calendar-alt calendar-icon" id="calendar-icon-final"></i>
                                </div>
                        </div>
                    </div>

                    <!-- Botón de actualizar -->
                    <div class="row justify-content-center mt-3">
                        <div class="col-md-6 text-center">
                            <button id="btnActualizar" class="btn btn-custom w-100">
                                <i class="fas fa-sync-alt me-2"></i><span style="font-weight:500;">Actualizar</span>
                            </button>
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

            const calendarIconFinal = document.getElementById('calendar-icon-final');
            if (calendarIconFinal) {
                calendarIconFinal.addEventListener('click', () => {
                    document.getElementById('fecha_final').focus();
                });
            }

            // Esperar un poco antes de activar la transición
            setTimeout(() => {
                const fechaInput = document.getElementById('fecha_inicial');
                const fechaInputFinal = document.getElementById('fecha_final');
                const btnActualizar = document.getElementById('btnActualizar');

                // Establecer las fechas en los inputs solo si no están definidas
                if (fecha_inicial_actual && fecha_final_actual) {
                    fechaInput.value = fecha_inicial_actual;
                    fechaInputFinal.value = fecha_final_actual;
                }

                // Configurar flatpickr si aún no está configurado
                flatpickrdate(fecha_inicial_actual, fecha_final_actual);

                // Configurar el evento de actualización de las fechas
                if (btnActualizar) {
                    btnActualizar.addEventListener('click', function () {
                        const fechaSeleccionada = fechaInput.value || fecha_inicial_actual;
                        const fechaFinalSeleccionada = fechaInputFinal.value || fecha_final_actual;
                    
                        console.log('Fecha seleccionada por el usuario:', fechaSeleccionada, fechaFinalSeleccionada);
                    
                        // Convertir fechas a objetos Date
                        const fechaInicial = parseDate(fechaSeleccionada);
                        const fechaFinal = parseDate(fechaFinalSeleccionada);
                    
                        // Validar si las fechas son válidas
                        if (isNaN(fechaInicial) || isNaN(fechaFinal)) {
                            errorParametros(true, 'Las fechas ingresadas no son válidas.');
                            console.error('Fecha inválida:', fechaSeleccionada, fechaFinalSeleccionada);
                            return;
                        }
                    
                        // Validar si la fecha inicial es mayor que la fecha final
                        if (fechaInicial.getTime() > fechaFinal.getTime()) {
                            errorParametros(true, 'La fecha inicial no puede ser mayor a la fecha final.');
                            console.log('Fechas incorrectas: la fecha inicial es mayor que la fecha final');
                            return;
                        }
                    
                        // Limpiar cualquier error anterior y recargar datos
                        errorParametros(false);
                        recargarDatosAPI(fechaSeleccionada, fechaFinalSeleccionada);
                    });                    
                }
                

                // Activar la visibilidad del resumen
                if (resumenHtml && resumenHtmlnumeros) {
                    resumenHtml.classList.add('visible');
                    resumenHtmlnumeros.classList.add('visible');
                }
            }, 100); // Retraso corto para permitir que el contenido se cargue antes de la animación

        } else {
            console.error('No se encontró el contenedor con id "resumen-grafica"');
        }
    }, 50);  // Tiempo de espera para asegurarse de que la gráfica se haya renderizado
}

function recargarDatosAPI(fecha, fechaFinal) {
    if (isReloading) {
        console.log('Reload already in progress. Skipping this request.');
        return;
    }

    isReloading = true; // Indica que una recarga está en curso

    const fechaInput = document.getElementById('fecha_inicial');
    const fechaInputFinal = document.getElementById('fecha_final');
    const btnActualizar = document.getElementById('btnActualizar');

    console.log('Fechas enviadas para recarga:', fecha, fechaFinal);

    showLoaderContainer('loader-wrapper-ventas', 'body-venta-devoluciones');
    fechaInput.disabled = true;
    fechaInputFinal.disabled = true;
    btnActualizar.disabled = true;

    apiVentasYDevoluciones(fecha, fechaFinal)
        .then(response => {
            if (response && response.status === "ok") {
                manejarVentasYDevoluciones(response);

                // Verifica si el API contiene fechas y actualiza los inputs solo si son diferentes
                if (response.fecha && response.fecha_final) {
                    if (response.fecha !== fecha_inicial_actual) {
                        fechaInput.value = response.fecha;
                        fecha_inicial_actual = response.fecha;
                    }
                    if (response.fecha_final !== fecha_final_actual) {
                        fechaInputFinal.value = response.fecha_final;
                        fecha_final_actual = response.fecha_final;
                    }
                    console.log('Fechas actualizadas desde el API:', response.fecha, response.fecha_final);
                } else {
                    console.log('El API no devolvió fechas. Se mantienen las actuales.');
                }
            } else {
                console.error('Datos inválidos recibidos del API:', response);
            }
        })
        .catch(error => {
            console.error('Error al recargar los datos:', error);
        })
        .finally(() => {
            hideLoaderContainer('loader-wrapper-ventas', 'body-venta-devoluciones');
            fechaInput.disabled = false;
            fechaInputFinal.disabled = false;
            btnActualizar.disabled = false;
            isReloading = false; // Restablece el indicador de recarga
        });
}

export function parseDate(fechaStr) {
    const [day, month, year] = fechaStr.split('-').map(Number);
    return new Date(year, month - 1, day); // Mes es 0-based
}