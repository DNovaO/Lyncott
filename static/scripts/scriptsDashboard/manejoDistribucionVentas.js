export function manejarDistribucionVentas(data) {
    console.log('Datos desde el manejo del API de distribucion de ventas', data);

    // Extraer los productos y las ventas de los datos
    const productos = data.distribucion_ventas.map(item => item.producto.trim());
    const ventas = data.distribucion_ventas.map(item => item.venta);

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
            labels: productos, // Productos en el eje X
            datasets: [{
                label: 'Ventas por Producto',
                data: ventas, // Ventas en el eje Y
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
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
                            size: 8// Ajusta el tamaño de las etiquetas del eje X
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
                zoom: {
                    pan: {
                        enabled: true, // Habilita el paneo
                        mode: 'x' // Permite pan en ambos ejes
                    },
                    zoom: {
                        wheel: {
                            enabled: true, // Habilita el zoom con el scroll del mouse
                        },
                        mode: 'x', // Permite el zoom en ambos ejes
                        onZoomComplete: ({ chart }) => {
                            chart.update('none'); // Actualiza la gráfica para mantener calidad
                        }
                    }
                }
            }
        }
    });
}
