//main.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script principal que se encarga de manejar la lógica de los modales y la generación de reportes.
    Ademas de mandar la información al servidor y recibir la información de los modulos. (No son los fetch) pero mandan 
    la información a los fetch.
    Haciendo uso de los demas de elementos de la carpeta modulos.

*/ 

export let cache = {};
export let dataType;
export let debouncedBuscador; 
export let parametrosSeleccionados = {};
export let fullItemsArray = [];
export let currentPage = 1;
export let currentPageTable = 1;
export let parametrosInforme = {};

import { tipo_reporte, btnMostrarGrafico, btnReset, btnGenerarInforme, btnBorrarReporte, modalContent, modalFooter, fechaInicialInput, fechaFinalInput} from "./config.js"; 
import { sendDataToServer, sendParametersToServer } from './apiHandler.js';
import { handleItemSelected, renderGeneral } from './renderModal.js';
import { errorParametros} from './utils.js'; // Asegúrate de importar las funciones necesarias
import { resetTabla } from './renderTabla.js';

document.addEventListener("DOMContentLoaded", function(){
    const modalButtons = document.querySelectorAll(".modal-trigger");
    
    modalButtons.forEach(button => {
        
        button.addEventListener("click", function(){
            dataType = this.getAttribute("data-type");
            
            console.log('El tipo de dato que vamos a enviar es:', dataType);

            debouncedBuscador = debounce(() => {
                console.log("dataType recibido:", dataType);
                buscador(dataType);
            }, 300);

            window.debouncedBuscador = debouncedBuscador;
            currentPage = 1;

            $("#genericModal").modal("show");

            sendDataToServer(dataType, currentPage);
        });
    });
    
    if (btnReset) {
        btnReset.addEventListener('click', function(e) {
            e.preventDefault();
            resetFormulario();
        });

    } 
    
    function recolectarValoresPorDefecto() {
        const valoresPorDefecto = {};
    
        // Obtener todos los botones con el atributo 'data-type' y el atributo 'data-estado' igual a 'activo'
        const botonesActivos = document.querySelectorAll('button[data-type][data-estado="activo"]');
    
        botonesActivos.forEach(boton => {
            const dataType = boton.getAttribute('data-type');
            const buttonText = boton.innerText.trim();
    
            try {
                // Intentamos parsear el texto como JSON
                const parsedText = JSON.parse(buttonText);
    
                // Validar si alguno de los valores contiene "Buscar"
                if (Object.values(parsedText).some(value => 
                    typeof value === 'string' && value.startsWith('Buscar'))) {
                    errorParametros(true,'Error, verifica que todos los campos estén seleccionados' )
        
                    throw new Error('Valor no válido');
                }
    
                valoresPorDefecto[dataType] = [parsedText];
            } catch (e) {
                // Si el parsing falla o hay un valor inválido, guardar como texto plano
                if (buttonText.startsWith('Buscar')) {
                    errorParametros(true, 'Error, verifica que todos los campos estén seleccionados');
        
                    throw new Error('Valor no válido');
                }
    
                valoresPorDefecto[dataType] = [{ nombre: buttonText }];
            }
        });
    
        // Añadir las fechas pero antes comparar que la fecha_inicial no sea mayor a la fecha_final
        if (fechaInicialInput.value > fechaFinalInput.value) {
            errorParametros(true, 'Error la fecha inicial no puede ser mayor a la fecha final');

            throw new Error('Fecha inicial mayor a fecha final');
        }else {
            errorParametros(false, 'Parámetros por defecto aplicados');

            valoresPorDefecto['fecha_inicial'] = fechaInicialInput.value;
            valoresPorDefecto['fecha_final'] = fechaFinalInput.value;
        }


    
        console.log('Valores por defecto:', valoresPorDefecto);
        return valoresPorDefecto;
    }
    
    // Evento cuando se presiona el botón de generar informe
    if (btnGenerarInforme) {
        btnGenerarInforme.addEventListener('click', function(e) {
            e.preventDefault();
    
            // Limpiar la gráfica
            const graphContainer = document.getElementById('tablaGraphContainer');
            if (graphContainer) {
                graphContainer.remove(); // Eliminar el contenedor de la gráfica
            }

            let input = document.getElementById("inputBusquedaReportes");
            let filter = input.value.trim().toLowerCase();

            if(filter != ""){ 
                filter = "";
                input.value = "";
            }  

            const tablaFooter = document.getElementById('genericTablaPagination');
            if (tablaFooter) {
                tablaFooter.innerHTML = '';
            }

            // Deshabilitar el botón
            this.disabled = true;
    
            cache = {};
            console.log('boton activado, y cache vacio', cache);
    
            // Actualizar dataType al inicio
            dataType = this.getAttribute("data-type");
    
            // Intentar obtener los parámetros seleccionados
            let parametrosSeleccionados = handleItemSelected(dataType, this);
            
            // Si no se seleccionaron parámetros, usar valores por defecto
            if (parametrosSeleccionados.length === undefined) {
                parametrosSeleccionados = recolectarValoresPorDefecto();
                errorParametros(false, 'Parámetros por defecto aplicados');
    
                currentPageTable = 1;
                console.log('Parametros seleccionados:', parametrosSeleccionados);
                
                // Llamar a sendParametersToServer y manejar la habilitación del botón
                sendParametersToServer(parametrosSeleccionados, currentPageTable, tipo_reporte, this);
    
            } else {
                // Copiar valores seleccionados en parametrosInforme
                for (const parametro in parametrosSeleccionados) {
                    parametrosInforme[parametro] = parametrosSeleccionados[parametro];
                }
                
                // Verificar si el número de parámetros seleccionados es menor que el requerido
                if (Object.keys(parametrosInforme).length - 2 >= numeroParametro - 3) {
                    console.log('boton activado mandando informacion');
                    errorParametros(false, 'Parámetros seleccionados aplicados');
    
                    currentPageTable = 1;
    
                    console.log('dataType en sendParametersToServer:', dataType);
                    
                    // Llamar a sendParametersToServer y manejar la habilitación del botón
                    sendParametersToServer(parametrosInforme, currentPageTable, tipo_reporte, this);
                } else {
                    errorParametros(true, 'Error, verifica que todos los campos estén seleccionados');
                    // Habilitar el botón si hay un error
                    this.disabled = false;
                }
            }
        });
    }
    
    if (btnBorrarReporte){
        btnBorrarReporte.addEventListener('click', function(e) {
            e.preventDefault();
            resetTabla();
            btnGenerarInforme.disabled = false;
        });
    }

    if (btnMostrarGrafico)
        document.getElementById('btnMostrarGrafico').addEventListener('click', function() {
            this.classList.toggle('btn-active-green');
            btnGenerarInforme.disabled = false;
    });

});

export function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

export function buscador(dataType) {
    console.log(dataType);
    let input = document.getElementById("inputBusqueda");
    if (!input) {
        console.error("No se encontró el elemento de input");
        return;
    }

    let filter = input.value.trim().toLowerCase();
    
    if (filter === "") {
        sendDataToServer(dataType); // Vuelve a cargar los datos originales si el filtro está vacío
        return;
    }

    let filteredItems = fullItemsArray.filter(item => {
        for (const key in item) {
            if (Object.hasOwnProperty.call(item, key)) {
                if (typeof item[key] === 'string' && item[key].toLowerCase().includes(filter)) {
                    return true;
                }
            }
        }
        return false;
    });

    let resultList = document.getElementById("genericModalContent");
    if (resultList) {
        resultList.innerHTML = renderGeneral(filteredItems);

        // Reemplazar eventos después de actualizar la lista
        resultList.querySelectorAll('.selectable-item').forEach(item => {
            item.addEventListener('click', function() {
                handleItemSelected(dataType, this);
                input.value = ""; // Resetear el input después de seleccionar
            });
        });

    } else {
        console.error("No se encontró el elemento de lista de resultados");
    }   
}

export function resetFormulario() {

    // Tomar valor del footer por id
    const footer = document.getElementById('genericTablaPagination');

    // Restablecer texto de botones que activan los modales
    const modalButtons = document.querySelectorAll('.modal-trigger');
    modalButtons.forEach(button => {
        button.textContent = `Buscar ${button.getAttribute('data-type').replace('_', ' ')}`; // Restablecer el texto del botón
    });
    
    // Limpiar contenido y pie del modal
    modalContent.innerHTML = '';
    modalFooter.innerHTML = '';
    footer.innerHTML = '';
    parametrosSeleccionados = {};
    parametrosInforme = {};

}
