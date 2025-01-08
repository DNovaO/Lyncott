export function flatpickrdate(fechaInicial, fechaFinal) {
    const fechaInicialInput = document.getElementById('fecha_inicial');
    const fechaFinalInput = document.getElementById('fecha_final');
    const calendarIconInicial = document.getElementById('calendar-icon-inicial');
    const calendarIconFinal = document.getElementById('calendar-icon-final');

    console.log('desde flatpickrdate', fechaInicial, fechaFinal);

    // Obtener el primer día del mes actual
    const primerDiaDelMes = new Date();
    primerDiaDelMes.setDate(1);

    // Formatear la fecha "d-m-Y"
    function obtenerFechaFormateada(fecha) {
        return `${('0' + fecha.getDate()).slice(-2)}-${('0' + (fecha.getMonth() + 1)).slice(-2)}-${fecha.getFullYear()}`;
    }

    // Validar y convertir la fecha a un objeto Date
    function convertirAFecha(fechaStr) {
        const partes = fechaStr.split('-');
        if (partes.length === 3) {
            const dia = parseInt(partes[0], 10);
            const mes = parseInt(partes[1], 10) - 1; // Los meses en JavaScript son 0-indexados
            const anio = parseInt(partes[2], 10);
            return new Date(anio, mes, dia);
        }
        return null;
    }

    // Configurar Flatpickr
    function configurarFlatpickr(input, fechaPorDefecto) {
        flatpickr(input, {
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
            defaultDate: fechaPorDefecto,
            onReady: function (selectedDates, dateStr, instance) {
                input.value = instance.formatDate(fechaPorDefecto, 'd-m-Y');
            },
            onChange: function (selectedDates, dateStr) {
                input.value = dateStr;
            }
        });
    }

    // Si se proporcionan fechas inicial y final, usarlas. Si no, usar las predeterminadas.
    const fechaInicialDef = fechaInicial ? convertirAFecha(fechaInicial) : primerDiaDelMes;
    const fechaFinalDef = fechaFinal ? convertirAFecha(fechaFinal) : new Date();

    // Verificar si las fechas convertidas son válidas
    if (isNaN(fechaInicialDef) || isNaN(fechaFinalDef)) {
        console.error('Fechas no válidas proporcionadas:', fechaInicial, fechaFinal);
        return;
    }

    // Inicializar Flatpickr con las fechas proporcionadas o por defecto
    configurarFlatpickr(fechaInicialInput, fechaInicialDef);
    configurarFlatpickr(fechaFinalInput, fechaFinalDef);

    // Abrir calendario al hacer clic en el ícono
    calendarIconInicial.addEventListener('click', function () {
        fechaInicialInput._flatpickr.open();
    });

    calendarIconFinal.addEventListener('click', function () {
        fechaFinalInput._flatpickr.open();
    });
}