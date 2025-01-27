import { tendenciaVentas, showLoaderContainer, hideLoaderContainer } from './dashboardApis.js';
import { errorParametrosTendencia, inicializarFlatpickr } from './utilsDashboard.js';

let isReloading = false; 
let fecha_inicial_actual = null;
let fecha_final_actual = null;

export function manejarTendenciaVentas(data) {
    if (!data || !Array.isArray(data.tendencia_ventas)) {
        console.error('El formato de los datos no es válido o no contiene "tendencia_ventas":', data);
        return;
    }

    const tendenciaVentas = data.tendencia_ventas;

    console.log('Datos procesados desde el manejo del API de Tendencia de Ventas:', tendenciaVentas);

    // Preparar datos para la gráfica
    const etiquetas = tendenciaVentas.map(d => d.fecha_dia); // Usar la columna combinada fecha_dia
    const ventaAutoService = tendenciaVentas.map(d => d.venta_autoservice); // Ventas autoservice
    const ventaFoodService = tendenciaVentas.map(d => d.venta_foodservice); // Ventas foodservice

    // Crear el elemento del canvas dinámicamente si no existe
    let canvas = document.getElementById('tendenciaChart');
    if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'tendenciaChart';
        document.body.appendChild(canvas);
    }

    // Verificar si ya existe un gráfico en el canvas, y destruirlo si es necesario
    const existingChart = Chart.getChart(canvas);
    if (existingChart) {
        existingChart.destroy();
    }

    // Configurar gráfico
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line', // Tipo de gráfico
        data: {
            labels: etiquetas,
            datasets: [
                {
                    label: 'Ventas AutoService',
                    data: ventaAutoService,
                    borderColor: 'blue',
                    backgroundColor: 'rgba(0, 0, 255, 0.1)',
                    fill: true,
                },
                {
                    label: 'Ventas FoodService',
                    data: ventaFoodService,
                    borderColor: 'green',
                    backgroundColor: 'rgba(0, 255, 0, 0.1)',
                    fill: true,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function (tooltipItem) {
                            return `$${tooltipItem.raw.toLocaleString()}`; // Formato moneda
                        },
                    },
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Ventas ($)',
                    },
                },
                x: {
                    title: {
                        display: true,
                        text: 'Fecha (Día)',
                    },
                },
            },
        },
    });

    if (canvas) {
        actualizarContenedorTendencia(data);
    }
}

function actualizarContenedorTendencia(data) {
    if (!data || !Array.isArray(data.tendencia_ventas)) {
        console.error("El formato de los datos no es válido o no contiene 'tendencia_ventas'.");
        return;
    }

    const tendenciaVentas = data.tendencia_ventas;

    // Encontrar los días con mayores y menores ventas para AutoService y FoodService
    const diaMayorVentaAutoService = tendenciaVentas.reduce((max, item) =>
        item.venta_autoservice > max.venta_autoservice ? item : max, tendenciaVentas[0]);

    const diaMenorVentaAutoService = tendenciaVentas.reduce((min, item) =>
        item.venta_autoservice < min.venta_autoservice ? item : min, tendenciaVentas[0]);

    const diaMayorVentaFoodService = tendenciaVentas.reduce((max, item) =>
        item.venta_foodservice > max.venta_foodservice ? item : max, tendenciaVentas[0]);

    const diaMenorVentaFoodService = tendenciaVentas.reduce((min, item) =>
        item.venta_foodservice < min.venta_foodservice ? item : min, tendenciaVentas[0]);

    // Referencia al contenedor de resumen
    const resumenContenedor = document.getElementById('resumen-graficaTendencia');
    const resumenContenedorNumeros = document.getElementById('resumen-graficaTendencia-numeros');
    
    if(resumenContenedor) {
        resumenContenedor.innerHTML = `
            <h4 class="mb-1 text-center">Resumen de periodo</h4>

            <div class="container mb-2">
                <!-- Fila para las fechas -->
                <div class="row g-3 align-items-center justify-content-center">
                    <div class="col-md-6">
                        <div class="date-container">
                            <label for="fecha_inicial_tendencia" class="date-label">Fecha inicial:</label>
                            <div class="date-input-wrapper">
                                <input type="text" id="fecha_inicial_tendencia" name="fecha_inicial_tendencia" class="form-control" />
                                <i class="fas fa-calendar-alt calendar-icon" id="calendar-icon-inicial-tendencia"></i>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="date-container">
                            <label for="fecha_final_tendencia" class="date-label">Fecha final:</label>
                            <div class="date-input-wrapper">
                                <input type="text" id="fecha_final_tendencia" name="fecha_final_tendencia" class="form-control" />
                                <i class="fas fa-calendar-alt calendar-icon" id="calendar-icon-final-tendencia"></i>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Botón de actualizar -->
                <div class="row justify-content-center mt-3">
                    <div class="col-md-12 text-center">
                        <button id="btnActualizar_tendencia" class="btn btn-custom w-100">
                            <i class="fas fa-sync-alt me-2"></i><span style="font-weight:500;">Actualizar</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // Renderizar las tarjetas
    if (resumenContenedorNumeros) {
        resumenContenedorNumeros.innerHTML = `
            <div class="resumen-numeros">
                <div class="row justify-content-center w-100">
                    <!-- Tarjeta de Mayor Venta AutoService -->
                    <div class="col-12 col-md-6 text-center mb-4">
                        <div class="card shadow-sm border-success d-flex flex-column h-100">
                            <div class="card-body d-flex flex-column justify-content-center">
                                <h6 class="card-title">Mayor Venta AutoService</h6>
                                <p class="card-text text-center text-success mt-auto fs-5">
                                    ${diaMayorVentaAutoService.fecha_dia}: 
                                    $${diaMayorVentaAutoService.venta_autoservice.toLocaleString('es-MX')}
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Tarjeta de Menor Venta AutoService -->
                    <div class="col-12 col-md-6 text-center mb-4">
                        <div class="card shadow-sm border-danger d-flex flex-column h-100">
                            <div class="card-body d-flex flex-column justify-content-center">
                                <h6 class="card-title">Menor Venta AutoService</h6>
                                <p class="card-text text-center text-danger mt-auto fs-5">
                                    ${diaMenorVentaAutoService.fecha_dia}: 
                                    $${diaMenorVentaAutoService.venta_autoservice.toLocaleString('es-MX')}
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Tarjeta de Mayor Venta FoodService -->
                    <div class="col-12 col-md-6 text-center mb-4">
                        <div class="card shadow-sm border-success d-flex flex-column h-100">
                            <div class="card-body d-flex flex-column justify-content-center">
                                <h6 class="card-title">Mayor Venta FoodService</h6>
                                <p class="card-text text-center text-success mt-auto fs-5">
                                    ${diaMayorVentaFoodService.fecha_dia}: 
                                    $${diaMayorVentaFoodService.venta_foodservice.toLocaleString('es-MX')}
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Tarjeta de Menor Venta FoodService -->
                    <div class="col-12 col-md-6 text-center mb-4">
                        <div class="card shadow-sm border-danger d-flex flex-column h-100">
                            <div class="card-body d-flex flex-column justify-content-center">
                                <h6 class="card-title">Menor Venta FoodService</h6>
                                <p class="card-text text-center text-danger mt-auto fs-5">
                                    ${diaMenorVentaFoodService.fecha_dia}: 
                                    $${diaMenorVentaFoodService.venta_foodservice.toLocaleString('es-MX')}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Agregar funcionalidad al ícono para abrir el selector
    const calendarIconInicial = document.getElementById('calendar-icon-inicial-tendencia');
    if (calendarIconInicial) {
        calendarIconInicial.addEventListener('click', () => {
            document.getElementById('fecha_inicial_tendencia').focus();
        });
    }

    const calendarIconFinal = document.getElementById('calendar-icon-final-tendencia');
    if (calendarIconFinal) {
        calendarIconFinal.addEventListener('click', () => {
            document.getElementById('fecha_final_tendencia').focus();
        });
    }

    setTimeout(() => {
        const fechaInput = document.getElementById('fecha_inicial_tendencia');
        const fechaInputFinal = document.getElementById('fecha_final_tendencia');
        const btnActualizar = document.getElementById('btnActualizar_tendencia');

        if (fecha_inicial_actual && fecha_final_actual) {
            fechaInput.value = fecha_inicial_actual;
            fechaInputFinal.value = fecha_final_actual;
        }

        inicializarFlatpickr(fecha_inicial_actual, fecha_final_actual, 'tendencia');

        if (btnActualizar) {
            btnActualizar.addEventListener('click', function () {
                const fechaSeleccionada = fechaInput.value || fecha_inicial_actual;
                const fechaFinalSeleccionada = fechaInputFinal.value || fecha_final_actual;
                
                // Función para convertir una fecha en formato d-m-Y a un objeto Date
                function convertirAFecha(fechaStr) {
                    const partes = fechaStr.split('-'); // Divide la fecha en día, mes y año
                    const dia = parseInt(partes[0], 10); // Día
                    const mes = parseInt(partes[1], 10) - 1; // Mes (0-indexado)
                    const anio = parseInt(partes[2], 10); // Año
                    return new Date(anio, mes, dia); // Devuelve el objeto Date
                }
                
                // Convertir las fechas seleccionadas a objetos Date
                const fechaInicialDate = convertirAFecha(fechaSeleccionada);
                const fechaFinalDate = convertirAFecha(fechaFinalSeleccionada);
                
                // Validar si la fecha inicial es mayor que la fecha final
                if (fechaInicialDate > fechaFinalDate) {
                    console.log('Fecha inicial mayor a la final:', fechaSeleccionada, fechaFinalSeleccionada);
                    errorParametrosTendencia(true, 'La fecha inicial no puede ser mayor a la fecha final.');
                    return;
                }
                
                errorParametrosTendencia(false);
                recargarDatostendenciaAPI(fechaSeleccionada, fechaFinalSeleccionada);
            });
        }
    }, 50);
}


// Función de resumen de productos (por implementar)
function recargarDatostendenciaAPI(fecha, fechaFinal) {
    if (isReloading) {
        console.log('Reload already in progress. Skipping this request.');
        return;
    }

    isReloading = true; // Indica que una recarga está en curso

    const fechaInput = document.getElementById('fecha_inicial_tendencia');
    const fechaInputFinal = document.getElementById('fecha_final_tendencia');
    const btnActualizar = document.getElementById('btnActualizar_tendencia');

    console.log('Fechas enviadas para recarga tendencia:', fecha, fechaFinal);

    showLoaderContainer('loader-wrapper-tendencia_ventas', 'body-tendencia_ventas');
    fechaInput.disabled = true;
    fechaInputFinal.disabled = true;
    btnActualizar.disabled = true;

    tendenciaVentas(fecha, fechaFinal)
        .then(response => {
            if (response && response.status === "ok") {
                manejarTendenciaVentas(response);

                // Verifica si el API contiene fechas y actualiza los inputs solo si son diferentes
                if (response.fecha && response.fecha_final) {
                    if (response.fecha !== fecha_inicial_actual) {
                        fechaInput.value = response.fecha;
                        fecha_inicial_actual = response.fecha;
                        console.log('Fechas actualizadas desde el API con:', response.fecha, response.fecha_final);
                    }
                    if (response.fecha_final !== fecha_final_actual) {
                        fechaInputFinal.value = response.fecha_final;
                        fecha_final_actual = response.fecha_final;
                        console.log('Fechas actualizadas desde el API con:', response.fecha, response.fecha_final);
                    }
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
            hideLoaderContainer('loader-wrapper-tendencia_ventas', 'body-tendencia_ventas');
            fechaInput.disabled = false;
            fechaInputFinal.disabled = false;
            btnActualizar.disabled = false;
            isReloading = false; // Restablece el indicador de recarga
        });
}
