import { errorParametrosProductos, flatpickrdateParaProductos } from './utilsDashboard.js';
import { parseDate } from './manejoVentasDevoluciones.js';

let fecha_inicial_actual = null;
let fecha_final_actual = null;
let productoMasVendido;
let productoMenosVendido; 

export function manejarDistribucionVentas(data) {
    console.log('Datos desde el manejo del API de distribución de ventas:', data);

    if (!data || !data.distribucion_ventas) {
        console.error('Dastos de ventas no válidos.');
        return;
    }

    // Extraer productos y ventas de los datos
    const productos = data.distribucion_ventas.map(item => item.producto?.trim() || 'Desconocido');
    const ventas = data.distribucion_ventas.map(item => item.venta || 0);

    // Crear el contexto del canvas para Chart.js
    const canvas = document.getElementById('lineChart');
    if (!canvas) {
        console.error('El elemento canvas con id "lineChart" no se encontró.');
        return;
    }

    // Verificar si ya existe un gráfico en el canvas, y destruirlo si es necesario
    const existingChart = Chart.getChart(canvas);
    if (existingChart) {
        existingChart.destroy();
    }

    // Crear la gráfica de líneas
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: productos,
            datasets: [{
                label: 'Ventas por Producto',
                data: ventas,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                pointBackgroundColor: 'rgba(255, 99, 132, 1)', // Color de los puntos
                pointBorderColor: 'rgb(255, 29, 78)', // Borde de los puntos para mayor contraste
                pointBorderWidth: 1, // Grosor del borde de los puntos
                fill: true,
                tension: 0.1
            }]            
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: {
                        maxRotation: 90,
                        minRotation: 90,
                        font: {
                            size: 8 // Ajusta el tamaño de las etiquetas del eje X
                        }
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 10 // Ajusta el tamaño de las etiquetas del eje Y
                        }
                    },
                    beginAtZero: true
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            return `${label}: $${value.toLocaleString('es-MX')}`; // Muestra valores y porcentaje
                        },
                    }
                },
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'x'
                    },
                    zoom: {
                        wheel: {
                            enabled: true
                        },
                        mode: 'x',
                        onZoomComplete: ({ chart }) => {
                            chart.update('none');
                        }
                    }
                }
            }
        }
    });

    if (canvas) {
        actualizarContenedor(productos, ventas);
    }
}

// Función para actualizar el contenedor de resumen de productos
function actualizarContenedor(productos, ventas) {
    const resumenProductos = document.getElementById('resumen-graficaProductos');
    const resumenVentasProductos = document.getElementById('resumen-graficaProductos-numeros');

    // Encontrar los índices del producto más y menos vendido
    let indexMasVendido = ventas.indexOf(Math.max(...ventas));
    let indexMenosVendido = ventas.indexOf(Math.min(...ventas));

    // Obtener el producto más y menos vendido
    productoMasVendido = productos[indexMasVendido];
    productoMenosVendido = productos[indexMenosVendido];

    if (!resumenProductos) {
        console.error('El contenedor con id "resumen-graficaProductos" no se encontró.');
        return;
    }

    // Limpiar y renderizar el contenedor
    resumenProductos.innerHTML = `
        <h4 class="mb-1 text-center">Resumen de periodo</h4>

        <div class="container mb-2">
            <!-- Fila para las fechas -->
            <div class="row g-3 align-items-center justify-content-center">
                <div class="col-md-6">
                    <div class="date-container">
                        <label for="fecha_inicial" class="date-label">Fecha inicial:</label>
                        <div class="date-input-wrapper">
                            <input type="text" id="fecha_inicial_productos" name="fecha_inicial" class="form-control" />
                            <i class="fas fa-calendar-alt calendar-icon" id="calendar-icon-inicial-producto"></i>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="date-container">
                        <label for="fecha_final" class="date-label">Fecha final:</label>
                        <div class="date-input-wrapper">
                            <input type="text" id="fecha_final_productos" name="fecha_final" class="form-control" />
                            <i class="fas fa-calendar-alt calendar-icon" id="calendar-icon-final-producto"></i>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Botón de actualizar -->
            <div class="row justify-content-center mt-3">
                <div class="col-md-12 text-center">
                    <button id="btnActualizar_producto" class="btn btn-custom w-100">
                        <i class="fas fa-sync-alt me-2"></i><span style="font-weight:500;">Actualizar</span>
                    </button>
                </div>
            </div>
        </div>
    `;

    resumenVentasProductos.innerHTML = `
        <div class="resumen-numerosProducto">
            <p class="text-center mt-2">
            <strong>Producto más vendido:</strong> <span id="productoMasVendido">${productoMasVendido}: $${ventas[indexMasVendido].toLocaleString('es-MX')}</span>
            </p>
            <p class="text-center mt-2">
            <strong>Producto menos vendido:</strong> <span id="productoMenosVendido">${productoMenosVendido}:$${ventas[indexMenosVendido].toLocaleString('es-MX')}</span>
            </p>
        </div>
    `;

    // Inicializar los eventos para los íconos del calendario
    const calendarIconInicial = document.getElementById('calendar-icon-inicial-producto');
    if(calendarIconInicial){
        calendarIconInicial.addEventListener('click', () => {
            document.getElementById('fecha_inicial_productos').focus();
        });
    }

    const calendarIconFinal = document.getElementById('calendar-icon-final-producto');
    if(calendarIconFinal){
        calendarIconFinal.addEventListener('click', () => {
            document.getElementById('fecha_final_productos').focus();
        });
    }

    const fechaInput = document.getElementById('fecha_inicial_productos');
    const fechaInputFinal = document.getElementById('fecha_final_productos');

    // Establecer las fechas en los inputs solo si no están definidas
    if (fecha_inicial_actual && fecha_final_actual) {
        fechaInput.value = fecha_inicial_actual;
        fechaInputFinal.value = fecha_final_actual;
    }

    // Configurar flatpickr si aún no está configurado
    flatpickrdateParaProductos(fecha_inicial_actual, fecha_final_actual);


    // Inicializar el botón de actualizar
    const btnActualizar = document.getElementById('btnActualizar_producto');
    if(btnActualizar){
        btnActualizar.addEventListener('click', () => {
            const fechaSeleccionada = fechaInput.value || fecha_inicial_actual;
            const fechaFinalSeleccionada = fechaInputFinal.value || fecha_final_actual;

            const fechaInicial = parseDate(fechaSeleccionada);
            const fechaFinal = parseDate(fechaFinalSeleccionada);


            // Validar si las fechas son válidas
            if (isNaN(fechaInicial) || isNaN(fechaFinal)) {
                errorParametrosProductos(true, 'Las fechas ingresadas no son válidas.');
                console.error('Fecha inválida:', fechaSeleccionada, fechaFinalSeleccionada);
                return;
            }
        
            // Validar si la fecha inicial es mayor que la fecha final
            if (fechaInicial.getTime() > fechaFinal.getTime()) {
                errorParametrosProductos(true, 'La fecha inicial no puede ser mayor a la fecha final.');
                console.log('Fechas incorrectas: la fecha inicial es mayor que la fecha final');
                return;
            }

            // Realizar la petición a la API
            errorParametrosProductos(false);
            recargarDatosProductosAPI(fechaInicial, fechaFinal);
        });
    }
}

// Función de resumen de productos (por implementar)
function recargarDatosProductosAPI(fecha, fechaFinal) {
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
