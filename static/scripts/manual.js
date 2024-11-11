// Manual.js

/*
    Diego Nova Olguín
    Ultima modificación: 7/11/2024

    Script que se encarga de guiar al usuario a través de los pasos necesarios para generar un reporte.
    Se mostrarán los elementos necesarios para generar un reporte y se explicará su funcionamiento.  
*/ 

const driver = window.driver.js.driver;

const driverObj = driver();

function iniciarGuia() {
    setTimeout(() => {
        const driverObj = driver({
            disableActiveInteraction: true,
            showProgress: true,
            doneBtnText: 'Hecho',        
            closeBtnText: 'Cerrar',       
            nextBtnText: 'Siguiente', 
            prevBtnText: 'Anterior',
            steps: [
            { element: '#parametros-reporte', popover: { title: 'Guía de reportes', description: 'En esta sección se configuran los parámetros necesarios para generar los reportes. La cantidad de parámetros puede variar según el tipo de reporte seleccionado. ' } },
            
            { element: '#parametros-individuales', popover: { title: 'Guía de reportes', description: 'Al hacer click para cambiar los parámetros, se abrirá una ventana que mostrará más detalles sobre los parámetros de esa categoría. Además, tendrás la opción de buscar un cliente específico para facilitar la personalización de tu reporte.' } },
            
            { element: '#btnLimpiar', popover: { title: 'Guía de reportes', description: 'Para restablecer todos los filtros, haz click en el botón de limpiar filtros. Esto te permitirá empezar de nuevo con la configuración de los parámetros.' } },
            
            { element: '#btnGenerarInforme', popover: { title: 'Guía de reportes', description: 'Una vez completado el llenado de todos los parámetros haz click en el botón de generar reporte. Esto te permitirá generar el reporte deseado.' } },
            
            { element: '#navbar-reportes', popover: { title: 'Guía de reportes', description: 'En la barra de navegación, se puede cambiar el reporte dentro de la misma página sin necesidad de volver al inicio. Asi como cerrar sesión y volver al menú inicial.' } },

            { element: '#resultado-reporte', popover: { title: 'Guía de reportes', description: 'En esta sección se generan los reportes. Ten en cuenta que, aunque los botones relacionados con el reporte estarán visibles, no podrás utilizarlos hasta haber generado uno.' } },
            
            { element: '#resultadosPorPagina', popover: { title: 'Guía de reportes', description: 'Después de generar un reporte, puedes modificar la cantidad de datos que se van a mostrar en una página del reporte.' } },

            { element: '#search-reportes', popover: { title: 'Guía de reportes', description: 'Después de generar un reporte, puedes localizar un elemento específico utilizando la barra de búsqueda. Simplemente ingresa el término que deseas encontrar y la búsqueda resaltará los resultados correspondientes en el reporte.' } },

            { element: '#btnExportarExcel', popover: { title: 'Guía de reportes', description: 'Una vez que hayas generado un reporte, tienes la opción de exportarlo en formato Excel. Ten en cuenta que el reporte en Excel no incluirá el total de los resultados ni las gráficas' } },

            { element: '#btnExportarCSV', popover: { title: 'Guía de reportes', description: 'Después de generar un reporte, puedes exportarlo en formato CSV. Ten en cuenta que el reporte en CSV no incluirá el total de los resultados ni las gráficas.' } },

            { element: '#btnBorrarReporte', popover: { title: 'Guía de reportes', description: 'Una vez que hayas generado un reporte, tienes la opción de eliminar toda la información generada si así lo deseas. Esta acción eliminará todos los datos asociados al reporte.' } },
            
            { element: '#btnImprimir', popover: { title: 'Guía de reportes', description: 'Después de generar un reporte, puedes imprimirlo fácilmente haciendo clic en el botón de imprimir. Esta opción te permitirá obtener una copia física del reporte incluyendo totales y la gráfica generada.' } },

            { element: '#btnMostrarGrafico', popover: { title: 'Guía de reportes', description: 'Una vez que hayas generado un reporte, puedes crear un reporte completamente personalizado. Tendrás la flexibilidad de seleccionar los datos que deseas visualizar y elegir el tipo de gráfico que mejor se adapte a tus necesidades.' } },

            { element: '#boton-ayuda', popover: { title: 'Guía de reportes', description: 'Si necesitas ver el tutorial nuevamente, haz clic en el botón de ayuda.' } },
            ],

            onHighlighted: (element, step, options) => {
                // Bloquear la interacción con el elemento resaltado y sus hijos
                if (element) {
                    element.style.pointerEvents = 'none'; // Desactiva interacciones del elemento
                    const children = element.querySelectorAll('*'); // Selecciona todos los hijos
                    children.forEach(child => {
                        child.style.pointerEvents = 'none'; // Desactiva interacciones de cada hijo
                    });
                }
            },
            onDeselected: (element, step, options) => {
                // Reactivar la interacción cuando se deja de resaltar el elemento y sus hijos
                if (element) {
                    element.style.pointerEvents = 'auto'; // Reactiva interacciones del elemento
                    const children = element.querySelectorAll('*'); // Selecciona todos los hijos
                    children.forEach(child => {
                        child.style.pointerEvents = 'auto'; // Reactiva interacciones de cada hijo
                    });
                }
            },
        });
        driverObj.drive();
        
    }, 1000);
}

document.addEventListener("DOMContentLoaded", function() {
    // localStorage.removeItem('hasSeenGuide'); // Descomentar para mostrar la guía nuevamente cada vez que se recargue la página

    // Verificar si el usuario ya ha visto la guía
    if (!localStorage.getItem('hasSeenGuide')) {
        iniciarGuia();
        localStorage.setItem('hasSeenGuide', 'true');
    }
});