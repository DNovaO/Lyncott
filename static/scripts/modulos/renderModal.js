// renderModal.js
import { modalContent, modalFooter, fechaInicialInput, fechaFinalInput } from './config.js';
import { handlers } from './itemHandler.js';
import { parametrosSeleccionados, currentPage, renderPagination} from './main.js';

// Muestra un loader en el modal
export function showLoaderModal() {
    modalContent.innerHTML = `
        <div class="spinner-container">
            <div class="lds-ring">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
            <p>Cargando...</p>
        </div>
    `;
}

// Maneja los datos de la respuesta y muestra el modal
export function handleResponseData(data) {
    const dataType = data.data_type;
    const handler = handlers[dataType];

    if (handler) {
        handler(data, dataType);
    } else {
        console.error('Tipo de dato no reconocido');
    }

    // Mostrar el modal
    $("#genericModal").modal("show");

    // Manejar la selección de un elemento de la lista
    modalContent.querySelectorAll('.selectable-item').forEach(item => {
        item.addEventListener('click', function() {
            handleItemSelected(dataType, this);
        });
    });
}

// Carga los datos en el modal

export function cargarData(data, key, dataType){
    modalContent.innerHTML = renderGeneral(data[key].objList, key, dataType); // Asegúrate de pasar 'key' y 'dataType'
    modalFooter.innerHTML = renderPagination(data[key].pagination_info, currentPage, dataType);
}

// Renderiza la lista de elementos
export function renderGeneral(paginatedItems) {
    let html = '<ul class="list-group mt-3">';
    
    paginatedItems.forEach(item => {
        let line = '';
        for (const key in item) {
            if (Object.hasOwnProperty.call(item, key)) {
                if (line !== '') {
                    line += ' - ';
                }
                line += `${item[key]}`;
            }
        }
        html += `<li type="button" class="list-group-item list-group-item-action selectable-item" data-item='${JSON.stringify(item)}'>${line}</li>`;
    });

    html += '</ul>';
    return html;
}

// Maneja la selección de un ítem
export function handleItemSelected(dataType, selectedItem) {
    // Obtener el texto del elemento seleccionado
    const buttonText = selectedItem.innerText.trim();
    
    // Obtener el objeto JSON del elemento seleccionado
    const parsedItem = JSON.parse(selectedItem.getAttribute('data-item'));
    
    console.log('Elemento seleccionado:', parsedItem);
    
    // Actualizar el texto del botón con el texto del elemento seleccionado
    const button = document.querySelector(`.modal-trigger[data-type="${dataType}"]`);
    if (button) {
        button.textContent = buttonText;
    }
    
    // Si ya hay elementos seleccionados para este dataType, agregarlos, si no, crear una nueva lista
    if (!parametrosSeleccionados[dataType]) {
        parametrosSeleccionados[dataType] = [];
    }

    // Agregar el nuevo elemento seleccionado al arreglo de parámetros
    parametrosSeleccionados[dataType] = [parsedItem];

    // Actualizar las fechas
    parametrosSeleccionados['fecha_inicial'] = fechaInicialInput.value;
    parametrosSeleccionados['fecha_final'] = fechaFinalInput.value;

    // Cerrar el modal
    $("#genericModal").modal("hide");

    // Imprimir para verificar
    console.log('Parámetros seleccionados:', parametrosSeleccionados);
    
    // Retornar los parámetros seleccionados para su uso posterior
    return parametrosSeleccionados;
}
