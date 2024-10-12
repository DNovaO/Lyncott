/*  
    Sección para graficar los reportes, donde el usuario puede elegir los ejes de la gráfica.
    Se manejarán condicionales para manejar reportes prioritarios con una gráfica preestablecida y no modificable.
*/

import { showLoaderModal } from './renderModal.js';
import { formatNumber, transformHeader } from "./utils.js";
// import { generarGrafico } from './grafico.js'; // Ajusta la ruta según tu estructura de archivos

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
                    <div class="form-title">Selecciona la variable para el Eje X:</div>
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
                    <div class="form-title">Selecciona la variable para el Eje Y:</div>
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
                    <option value="pie">Pastel</option>
                    <option value="scatter">Dispersión</option>
                </select>
            </div>
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
            alert('Por favor, selecciona al menos una variable para el Eje X.');
            return;
        }
        const selectedXValues = selectedXCheckboxes.map(cb => cb.value);

        // Obtener las selecciones para Eje Y
        const selectedYCheckboxes = Array.from(document.querySelectorAll('.ejeY-checkbox:checked'));
        if (selectedYCheckboxes.length === 0) {
            alert('Por favor, selecciona al menos una variable para el Eje Y.');
            return;
        }
        const selectedYValues = selectedYCheckboxes.map(cb => cb.value);

        const tipoGrafico = document.getElementById('tipoGrafico').value;

        // Validar que Eje X y Eje Y no sean la misma variable
        const duplicates = selectedXValues.filter(value => selectedYValues.includes(value));
        if (duplicates.length > 0) {
            alert(`Por favor, selecciona variables diferentes para los ejes X e Y. Los siguientes valores son duplicados: ${duplicates.join(', ')}`);
            return;
        }

        // Llamar a la función para generar el gráfico con los valores seleccionados
        generarGrafico(selectedXValues, selectedYValues, tipoGrafico, datos_completos, tipo_reporte);

        // Cerrar el modal
        $("#genericModal").modal("hide");
    });

    // Mostrar el modal
    $("#genericModal").modal("show");

    // Imprimir el tipo de reporte para verificar
    console.log(tipo_reporte);
}
