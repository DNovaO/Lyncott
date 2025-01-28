import { formatNumber, transformHeader } from './utilsDashboard.js';

let paginaActual = 1; // Página actual
const elementosPorPagina = 15; // Máximo de elementos por página

export function manejarEstadisticasRapidas(datos) {

    const contenedor = document.getElementById('body-estadisticas-rapidas');
    if (!contenedor) {
        console.error('El contenedor con id "body-estadisticas-rapidas" no se encontró.');
        return;
    }

    if (!datos || datos.status !== "ok" || !Array.isArray(datos.estadisticas)) {
        console.error('Datos no válidos recibidos:', datos);
        contenedor.innerHTML = '<p class="text-center text-danger">Error al cargar las estadísticas.</p>';
        return;
    }

    // Filtrar datos no válidos
    const estadisticasValidas = datos.estadisticas.filter((grupo) => Array.isArray(grupo) && grupo.length > 0);
    const totalElementos = estadisticasValidas.flat().length;
    const totalPaginas = Math.ceil(totalElementos / elementosPorPagina);

    // Función para renderizar los datos de la página actual
    const renderizarPagina = () => {
        // Limpiar el contenedor antes de renderizar nuevos datos
        contenedor.innerHTML = `
            <h4 class="mb-1 text-center">Resumen de periodo mensual</h4>

            <ul id="resumen-estadisticas-rapidas" class="list-group list-group-flush"></ul>
            
            <nav class="pagination-wrapper" aria-label="Controles de paginación">
                <div class="pagination-controls d-flex justify-content-center align-items-center" style="margin-top:50px;">
                    <button id="prevPage" class="btn btn-secondary mx-1" aria-label="Página anterior" disabled>
                        &lt;
                    </button>
                    <div id="paginationNumbers" class="d-flex flex-wrap justify-content-center mx-2" role="navigation" aria-live="polite"></div>
                    <button id="nextPage" class="btn btn-secondary mx-1" aria-label="Página siguiente" disabled>
                        &gt;
                    </button>
                </div>
            </nav>
        `;

        const lista = document.getElementById('resumen-estadisticas-rapidas');
        const inicio = (paginaActual - 1) * elementosPorPagina;
        const fin = inicio + elementosPorPagina;
        const datosPaginados = estadisticasValidas.flat().slice(inicio, fin);

        if (datosPaginados.length === 0) {
            lista.innerHTML = '<li class="list-group-item text-center">No hay datos para mostrar.</li>';
            return;
        }

        datosPaginados.forEach((estadistica) => {
            const item = document.createElement('li');
            item.className = 'list-group-item d-flex justify-content-between align-items-center estadistica-item';

            if (estadistica.sucursal && estadistica.venta_pesos) {
                const sucursalTransformada = transformHeader(estadistica.sucursal);
                const ventaFormateada = formatNumber(estadistica.venta_pesos, true, 'pesos');

                item.innerHTML = `
                    <span class="sucursal" style="font-weight:500;">${sucursalTransformada}</span>
                    <span class="venta">${ventaFormateada}</span>
                `;
            } else {
                const key = Object.keys(estadistica)[0];
                const value = estadistica[key];
                const keyTransformada = transformHeader(key);
                const formattedValue = (!isNaN(value) && value !== 0)
                    ? formatNumber(value, false, key)
                    : value;

                item.innerHTML = `
                    <span class="key" style="font-weight:500;">${keyTransformada}</span>
                    <span class="value">$${formattedValue}</span>
                `;
            }

            lista.appendChild(item);
        });

        // Renderizar los números de paginación
        const paginationNumbers = document.getElementById('paginationNumbers');
        paginationNumbers.innerHTML = '';
        for (let i = 1; i <= totalPaginas; i++) {
            const pageButton = document.createElement('button');
            pageButton.className = `btn mx-1 ${i === paginaActual ? 'btn-primary' : 'btn-outline-primary'}`;
            pageButton.innerText = i;
            pageButton.addEventListener('click', () => {
                if (paginaActual !== i) {
                    paginaActual = i;
                    renderizarPagina();
                }
            });
            paginationNumbers.appendChild(pageButton);
        }

        // Manejar la visibilidad de los botones
        const btnPrev = document.getElementById('prevPage');
        const btnNext = document.getElementById('nextPage');

        btnPrev.disabled = paginaActual === 1;
        btnNext.disabled = paginaActual === totalPaginas;

        btnPrev.addEventListener('click', () => {
            if (paginaActual > 1) {
                paginaActual--;
                renderizarPagina();
            }
        });

        btnNext.addEventListener('click', () => {
            if (paginaActual < totalPaginas) {
                paginaActual++;
                renderizarPagina();
            }
        });
    };

    // Renderizar la primera página
    renderizarPagina();
}
