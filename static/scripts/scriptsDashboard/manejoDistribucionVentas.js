    import { distribucionVentas, showLoaderContainer, hideLoaderContainer } from './dashboardApis.js';
    import { errorParametrosProductos, inicializarFlatpickr } from './utilsDashboard.js';

    let isReloading = false; 
    let fecha_inicial_actual = null;
    let fecha_final_actual = null;

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

function actualizarContenedor(productos, ventas) {
    const resumenProductos = document.getElementById('resumen-graficaProductos');
    const resumenVentasProductos = document.getElementById('resumen-graficaProductos-numeros');

    // Asociar productos con ventas
    const productosYVentas = productos.map((producto, i) => ({
        producto: producto,
        venta: ventas[i]
    }));

    // Ordenar por ventas (descendente para más vendidos)
    const ordenadosPorVenta = [...productosYVentas].sort((a, b) => b.venta - a.venta);
    const top4MasVendidos = ordenadosPorVenta.slice(0, 4);

    // Filtrar productos a ignorar y ordenar por ventas (ascendente para menos vendidos)
    const productosFiltrados = productosYVentas.filter(({ producto }) =>
        producto !== "REJA QUESOS PICADOS" && producto !== "REJA FUERA DE ESPECIFICACION"
    );
    const ordenadosPorMenosVenta = [...productosFiltrados].sort((a, b) => a.venta - b.venta);
    const top4MenosVendidos = ordenadosPorMenosVenta.slice(0, 4);

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
                        <label for="fecha_inicial_productos" class="date-label">Fecha inicial:</label>
                        <div class="date-input-wrapper">
                            <input type="text" id="fecha_inicial_productos" name="fecha_inicial_productos" class="form-control" />
                            <i class="fas fa-calendar-alt calendar-icon" id="calendar-icon-inicial-producto"></i>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="date-container">
                        <label for="fecha_final_productos" class="date-label">Fecha final:</label>
                        <div class="date-input-wrapper">
                            <input type="text" id="fecha_final_productos" name="fecha_final_productos" class="form-control" />
                            <i class="fas fa-calendar-alt calendar-icon" id="calendar-icon-final-producto"></i>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Botón de actualizar -->
            <div class="row justify-content-center mt-3">
                <div class="col-md-12 text-center">
                    <button id="btnActualizar_productos" class="btn btn-custom w-100">
                        <i class="fas fa-sync-alt me-2"></i><span style="font-weight:500;">Actualizar</span>
                    </button>
                </div>
            </div>
        </div>
    `;

    resumenVentasProductos.innerHTML = `
        <div class="resumen-numerosProducto">
            <div class="top-sold">
                <p class="text-center mt-4 mb-3">
                    <strong>Top 4 Más Vendidos</strong>
                </p>
                <div class="row justify-content-center">
                    ${top4MasVendidos.map(({ producto, venta }, i) => `
                        <div class="col-6 col-md-3 text-center mb-4">
                            <div class="card shadow-sm border-success d-flex flex-column h-100">
                                <div class="card-body d-flex flex-column justify-content-between">
                                    <h5 class="card-title">${i + 1}. ${producto}</h5>
                                    <p class="card-text text-success mt-auto">$${venta.toLocaleString('es-MX')}</p>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>

            <div class="top-unsold mt-5">
                <p class="text-center mt-4 mb-3">
                    <strong>Top 4 Menos Vendidos</strong>
                </p>
                <div class="row justify-content-center">
                    ${top4MenosVendidos.map(({ producto, venta }, i) => `
                        <div class="col-6 col-md-3 text-center mb-4">
                            <div class="card shadow-sm border-danger d-flex flex-column h-100">
                                <div class="card-body d-flex flex-column justify-content-between">
                                    <h5 class="card-title">${i + 1}. ${producto}</h5>
                                    <p class="card-text text-danger mt-auto">$${venta.toLocaleString('es-MX')}</p>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>

    `;

    // Agregar funcionalidad al ícono para abrir el selector
    const calendarIconInicial = document.getElementById('calendar-icon-inicial-producto');
    if (calendarIconInicial) {
        calendarIconInicial.addEventListener('click', () => {
            document.getElementById('fecha_inicial_productos').focus();
        });
    }

    const calendarIconFinal = document.getElementById('calendar-icon-final-producto');
    if (calendarIconFinal) {
        calendarIconFinal.addEventListener('click', () => {
            document.getElementById('fecha_final_productos').focus();
        });
    }

    setTimeout(() => {
        const fechaInput = document.getElementById('fecha_inicial_productos');
        const fechaInputFinal = document.getElementById('fecha_final_productos');
        const btnActualizar = document.getElementById('btnActualizar_productos');

        if (fecha_inicial_actual && fecha_final_actual) {
            fechaInput.value = fecha_inicial_actual;
            fechaInputFinal.value = fecha_final_actual;
        }

        inicializarFlatpickr(fecha_inicial_actual, fecha_final_actual, 'productos');

        if (btnActualizar) {
            btnActualizar.addEventListener('click', function () {
                const fechaSeleccionada = fechaInput.value || fecha_inicial_actual;
                const fechaFinalSeleccionada = fechaInputFinal.value || fecha_final_actual;

                if (new Date(fechaSeleccionada) > new Date(fechaFinalSeleccionada)) {
                    errorParametrosProductos(true, 'La fecha inicial no puede ser mayor a la fecha final.');
                    return;
                }

                errorParametrosProductos(false);
                recargarDatosProductosAPI(fechaSeleccionada, fechaFinalSeleccionada);
            });
        }
    }, 100);
}
    
// Función de resumen de productos (por implementar)
function recargarDatosProductosAPI(fecha, fechaFinal) {
    if (isReloading) {
        console.log('Reload already in progress. Skipping this request.');
        return;
    }

    isReloading = true; // Indica que una recarga está en curso

    const fechaInput = document.getElementById('fecha_inicial_productos');
    const fechaInputFinal = document.getElementById('fecha_final_productos');
    const btnActualizar = document.getElementById('btnActualizar_productos');

    console.log('Fechas enviadas para recarga productos:', fecha, fechaFinal);

    showLoaderContainer('loader-wrapper-productos', 'body-distribucion-productos');
    fechaInput.disabled = true;
    fechaInputFinal.disabled = true;
    btnActualizar.disabled = true;

    distribucionVentas(fecha, fechaFinal)
        .then(response => {
            if (response && response.status === "ok") {
                manejarDistribucionVentas(response);

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
            hideLoaderContainer('loader-wrapper-productos', 'body-distribucion-productos');
            fechaInput.disabled = false;
            fechaInputFinal.disabled = false;
            btnActualizar.disabled = false;
            isReloading = false; // Restablece el indicador de recarga
        });
}
