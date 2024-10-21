// graficas.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Se encarga de mostrar el modal con las opciones de selección y de generar el gráfico en la tabla.
    Hace uso de funciones de utilidad para mostrar alertas y transformar encabezados.
        
*/ 

import { showLoaderModal } from './renderModal.js';
import { transformHeader } from "./utils.js";

export function mostrarGrafico(dataGlobal, tipo_reporte) {
    const { campos_reporte, datos_completos } = dataGlobal;

    // Muestra el loader si es necesario
    showLoaderModal();

    // Obtener el contenedor del contenido del modal
    const modalContent = document.getElementById('genericModalContent');
    modalContent.innerHTML = ''; // Limpiar contenido previo

    // Crear HTML para la selección de los ejes X e Y en la misma fila
    const ejesHTML = `
        <div class="form-container">
            <div class="row">
                <div class="form-group col">
                    <div class="form-title">Selecciona la categoria (Eje X):</div>
                    <div class="row">
                        ${campos_reporte.map(campo => `
                            <div class="form-check form-check-inline">
                                <input class="form-check-input ejeX-checkbox" type="checkbox" id="ejeX-${transformHeader(campo)}" value="${transformHeader(campo)}">
                                <label class="form-check-label" for="ejeX-${transformHeader(campo)}">
                                    ${transformHeader(campo)}
                                </label>
                            </div>
                        `).join('')}
                    </div>
                </div>
                <div class="form-group col">
                    <div class="form-title">Selecciona el o los valores a medir (Eje Y):</div>
                    <div class="row">
                        ${campos_reporte.map(campo => `
                            <div class="form-check form-check-inline">
                                <input class="form-check-input ejeY-checkbox" type="checkbox" id="ejeY-${transformHeader(campo)}" value="${transformHeader(campo)}">
                                <label class="form-check-label" for="ejeY-${transformHeader(campo)}">
                                    ${transformHeader(campo)}
                                </label>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;

    // Crear HTML para la selección del tipo de gráfico
    const tipoGraficoHTML = `
        <div class="form-container">
            <div class="form-group">
                <label for="tipoGrafico" class="form-title">Selecciona el tipo de gráfico:</label>
                <select class="custom-select" id="tipoGrafico">
                    <option value="bar">Barras</option>
                    <option value="line">Líneas</option>
                    <option value="scatter">Dispersión</option>
                </select>
            </div>
            <div id="alert-container" style="top: 10px; right: 10px;"></div>
        </div>
    `;

    // Insertar todo en el contenido del modal
    modalContent.innerHTML = ejesHTML + tipoGraficoHTML;

    // Configurar los botones en el footer del modal
    const modalFooter = document.getElementById('genericModalPagination');
    modalFooter.innerHTML = `
        <div class="d-flex justify-content-between">
            <button type="button" class="btn btn-dark w-100" style="font-weight: 500;" id="generateGraph">Generar Gráfico</button>
        </div>
    `;

    // Agregar el listener para el botón 'Generar Gráfico'
    document.getElementById('generateGraph').addEventListener('click', function () {
        // Obtener las selecciones para Eje X
        const selectedXCheckboxes = Array.from(document.querySelectorAll('.ejeX-checkbox:checked'));
        if (selectedXCheckboxes.length === 0) {
            showAlert('Por favor, selecciona al menos una variable para la categoria (Eje X).');
            return;
        }
        const selectedXValues = selectedXCheckboxes.map(cb => cb.value);
        
        // Obtener las selecciones para Eje Y
        const selectedYCheckboxes = Array.from(document.querySelectorAll('.ejeY-checkbox:checked'));
        if (selectedYCheckboxes.length === 0) {
            showAlert('Por favor, selecciona al menos una variable para el valor a medir (Eje Y).');
            return;
        }
        const selectedYValues = selectedYCheckboxes.map(cb => cb.value);
        
        const tipoGrafico = document.getElementById('tipoGrafico').value;
        
        // Validar que Eje X y Eje Y no sean la misma variable
        const duplicates = selectedXValues.filter(value => selectedYValues.includes(value));
        if (duplicates.length > 0) {
            showAlert(
                `Por favor, selecciona variables diferentes para los ejes X e Y. Los siguientes valores son duplicados: ${duplicates.join(', ')}`,
                'warning'
            );
            return;
        }
        
        // Llamar a la función para generar el gráfico con los valores seleccionados
        agregarGraficoATabla(selectedXValues, selectedYValues, tipoGrafico, datos_completos);

        // Cerrar el modal
        $("#genericModal").modal("hide");
    });

    // Mostrar el modal
    $("#genericModal").modal("show");

    console.log(tipo_reporte);
}

function agregarGraficoATabla(ejeX, ejeY, tipoGrafico, datos) {
    const tabla = document.querySelector('.table');

    console.log("Eje X:", ejeX);
    console.log("Eje Y:", ejeY);
    console.log("Datos completos:", datos);

    let existingGraphContainer = document.getElementById('tablaGraphContainer');
    if (existingGraphContainer) {
        existingGraphContainer.remove();
    }

    const graphContainer = document.createElement('div');
    graphContainer.id = 'tablaGraphContainer';
    graphContainer.style.display = 'flex'; // Usar flexbox para centrar
    graphContainer.style.justifyContent = 'center'; // Centrar horizontalmente
    graphContainer.style.width = '100%'; // Ajustar al 100% del contenedor padre
    graphContainer.style.height = '100vh';
    graphContainer.style.overflow = 'auto'; // Permitir desbordamiento
    graphContainer.innerHTML = '<canvas id="chartCanvas" style="display: flex; justify-content:center;"></canvas>';

    tabla.insertAdjacentElement('afterend', graphContainer);

    const ctx = document.getElementById('chartCanvas').getContext('2d');

    // Crear etiquetas para el Eje X tomando valores de las ventas
    const etiquetas = datos.map(fila => {
        return ejeX.map(eje => convertirValor(fila[transformHeaderReverse(eje)])).join(', ') || 'Sin Datos';
    });

    console.log("Etiquetas del Eje X:", etiquetas);

    // Obtener datasets para el eje Y
    const datasets = ejeY.map((campoY, index) => {
        const data = datos.map(fila => {
            const valor = convertirValor(fila[transformHeaderReverse(campoY)]);
            return (typeof valor === 'number') ? valor : 0; // Solo incluir números
        });
        console.log(`Datos para ${campoY}:`, data);

        return {
            label: campoY,
            data: data,
            backgroundColor: obtenerColor(index),
            borderColor: obtenerColor(index, 0.8),
            borderWidth: 1,
        };
    });

    // Crear el gráfico
    new Chart(ctx, {
        type: tipoGrafico,
        data: { labels: etiquetas, datasets: datasets },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                title: { display: true, text: `Gráfico generado` },
                subtitle: {display:true, text: 'Nota: Los valores pueden ser activados o desactivados dando click en el color o en la leyenda'}
            },
            scales: { x: { beginAtZero: true }, y: { beginAtZero: true } },
        }
    });

    setTimeout(() => {
        $("#genericModal").modal("hide");
    }, 300);
}

// Transformar encabezados de manera que se ajusten a los nombres en los datos
function transformHeaderReverse(header) {
    return header.toLowerCase().replace(/\s+/g, '_');
}

function convertirValor(valor) {
    if (typeof valor === 'string') {
        valor = valor.replace(/,/g, '');
        const numero = parseFloat(valor);
        if (!isNaN(numero)) {
            return numero;
        }
        const fecha = new Date(valor);
        if (!isNaN(fecha.getTime())) {
            return fecha;
        }
        return valor;
    }
    return valor;
}

function obtenerColor(index, opacity = 0.8) {
    const colores = [
        'rgba(255, 82, 127, OP)', 
        'rgba(0, 153, 255, OP)',  
        'rgba(255, 136, 0, OP)',   
        'rgba(0, 230, 230, OP)',  
        'rgba(178, 102, 255, OP)' 
    ];
    return colores[index % colores.length].replace('OP', opacity);
}

export function showAlert(message, type = 'danger') {
    const alertContainer = document.getElementById('alert-container');
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.style = `
        margin-bottom: 10px;
        padding: 15px;
        border-radius: 5px;
        background-color: ${type === 'danger' ? '#f8d7da' : '#d1e7dd'};
        color: ${type === 'danger' ? '#842029' : '#0f5132'};
        border: 1px solid ${type === 'danger' ? '#f5c2c7' : '#badbcc'};
    `;
    alert.innerHTML = `
        <strong>${type === 'danger' ? 'Error:' : 'Info:'}</strong> ${message}
    `;

    alertContainer.appendChild(alert);

    // Remover la alerta después de 3 segundos
    setTimeout(() => alert.remove(), 3000);
}
