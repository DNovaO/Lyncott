const driver = window.driver.js.driver; 
const driverObj = driver();

function iniciarGuiaDashboard() {
    setTimeout(() => {
        const driverObj = driver({
            disableActiveInteraction: true,
            showProgress: true,
            doneBtnText: 'Hecho',        
            closeBtnText: 'Cerrar',       
            nextBtnText: 'Siguiente', 
            prevBtnText: 'Anterior',
            steps: [
                { element: '#body-acciones-bolsa', popover: { title: 'Acciones en la Bolsa', description: 'Visualiza los movimientos más relevantes de determinadas acciones bursátiles.' } },
                { element: '#body', popover: { title: 'Información Importante', description: 'Las gráficas muestran datos mensuales por defecto, desde el primer día del mes actual hasta la fecha actual. Puedes ajustar las fechas en algunos gráficos para visualizar otros periodos.' } },
                { element: '#body-venta-devoluciones', popover: { title: 'Ventas vs Devoluciones', description: 'Compara las ventas y devoluciones mediante una gráfica interactiva. Puedes ajustar las fechas según tus necesidades.' } },
                { element: '#body-estadisticas-rapidas', popover: { title: 'Estadísticas Rápidas', description: 'Consulta un resumen claro y conciso de datos clave, como la venta total por sucursal y el total en kilos vendidos.' } },
                { element: '#body-distribucion-productos', popover: { title: 'Distribución de Productos', description: 'Analiza las ventas de productos en un periodo determinado. Identifica cuáles han tenido mayor o menor demanda, NOTA: Se puede hacer zoom en la gráfica con la rueda del mouse.' } },
                { element: '#tendenciaChart-container', popover: { title: 'Tendencia de Ventas', description: 'Observa la evolución de las ventas a lo largo del tiempo, comparando los segmentos de foodservice y autoservice.' } },
                { element: '#boton-ayuda', popover: { title: 'Guía del Dashboard', description: 'Haz clic aquí si deseas ver nuevamente el tutorial del dashboard.' } }, 
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
