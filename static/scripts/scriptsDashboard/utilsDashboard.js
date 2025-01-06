export function flatpickrdate() {
    // Seleccionar el elemento del input
    const fechaInicialInput = document.getElementById('fecha_inicial');
    const calendarIconInicial = document.getElementById('calendar-icon-inicial');

    if (!fechaInicialInput) {
        console.error('El elemento con id "fecha_inicial" no se encontró.');
        return;
    }

    // Obtener el primer día del mes actual
    const primerDiaDelMes = new Date();
    primerDiaDelMes.setDate(1);

    // Configurar Flatpickr
    flatpickr(fechaInicialInput, {
        locale: {
            firstDayOfWeek: 1,
            weekdays: {
                shorthand: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
                longhand: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],         
            }, 
            months: {
                shorthand: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                longhand: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            },
        },
        dateFormat: 'd-m-Y',
        defaultDate: primerDiaDelMes,
        onReady: function (selectedDates, dateStr, instance) {
            fechaInicialInput.value = instance.formatDate(primerDiaDelMes, 'd-m-Y');
        },
        onChange: function (selectedDates, dateStr) {
            fechaInicialInput.value = dateStr;
        },
    });

    // Agregar funcionalidad al ícono para abrir el selector
    if (calendarIconInicial) {
        calendarIconInicial.addEventListener('click', () => {
            fechaInicialInput._flatpickr.open();
        });
    }
}
