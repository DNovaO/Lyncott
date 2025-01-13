import { formatNumber, transformHeader } from './utilsDashboard.js';

export function manejarEstadisticasRapidas(datos) {
    console.log('Datos desde el manejo del API de estadísticas rápidas', datos);

    const contenedor = document.getElementById('body-estadisticas-rapidas');
    if (!contenedor) {
        console.error('El contenedor con id "body-estadisticas-rapidas" no se encontró.');
        return;
    }

    // Limpiar el contenedor antes de renderizar nuevos datos
    contenedor.innerHTML = '<ul class="list-group list-group-flush"></ul>';

    // Validar datos básicos
    if (datos.status !== "ok" || !Array.isArray(datos.estadisticas)) {
        console.error('Datos no válidos recibidos desde el API:', datos);
        return;
    }

    const lista = contenedor.querySelector('.list-group-flush');

    // Iterar sobre las estadísticas y procesarlas
    datos.estadisticas.forEach((grupo, index) => {
        const titulo = transformHeader(`Grupo ${index + 1}`); // Título del grupo basado en el índice (si es necesario)

        // Verificar que el grupo no sea nulo y que sea un arreglo
        if (grupo && Array.isArray(grupo) && grupo.length > 0) {
            grupo.forEach(estadistica => {
                // Procesar cada objeto dentro del grupo
                if (estadistica && typeof estadistica === 'object') {
                    const key = Object.keys(estadistica)[0]; // Extraer la primera clave del objeto
                    const value = estadistica[key];

                    // Aplicar transformHeader a la clave para formatearla
                    const keyTransformada = transformHeader(key);

                    // Formatear el valor si corresponde
                    const formattedValue = (!isNaN(value) && value !== 0)
                        ? formatNumber(value, false, key)
                        : value; // Si no es un número, mostrar el valor tal cual

                    // Crear un elemento de lista para cada estadística
                    const item = document.createElement('li');
                    item.className = 'list-group-item d-flex justify-content-between align-items-center estadistica-item';

                    item.innerHTML = `
                        <span class="key" style="font-weight:500;">${keyTransformada}</span>
                        <span class="value">${formattedValue}</span>
                    `;

                    lista.appendChild(item);

                    // Agregar la clase para animación
                    setTimeout(() => {
                        item.classList.add('visible');
                    }, 50); // Tiempo mínimo para aplicar la clase (para iniciar la animación)
                }
            });
        } else if (!grupo) {
            console.warn(`Elemento nulo o vacío en la posición ${index} de las estadísticas.`);
        }
    });
}
