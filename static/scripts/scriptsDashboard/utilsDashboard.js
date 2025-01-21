export function inicializarFlatpickr(fechaInicial, fechaFinal, tipo = 'general') {
    // Identificadores dinámicos basados en el tipo
    const fechaInicialId = tipo === 'productos' ? 'fecha_inicial_productos' : 'fecha_inicial';
    const fechaFinalId = tipo === 'productos' ? 'fecha_final_productos' : 'fecha_final';
    const iconoInicialId = tipo === 'productos' ? 'calendar-icon-inicial-producto' : 'calendar-icon-inicial';
    const iconoFinalId = tipo === 'productos' ? 'calendar-icon-final-producto' : 'calendar-icon-final';

    const fechaInicialInput = document.getElementById(fechaInicialId);
    const fechaFinalInput = document.getElementById(fechaFinalId);
    const calendarIconInicial = document.getElementById(iconoInicialId);
    const calendarIconFinal = document.getElementById(iconoFinalId);

    console.log(`Desde inicializarFlatpickr (${tipo})`, fechaInicial, fechaFinal);

    // Obtener el primer día del mes actual
    const primerDiaDelMes = new Date();
    primerDiaDelMes.setDate(1);

    // Validar y convertir la fecha a un objeto Date
    function convertirAFecha(fechaStr) {
        const partes = fechaStr.split('-');
        if (partes.length === 3) {
            const dia = parseInt(partes[2], 10);  // Cambiar el índice para asegurar que día y mes se asignen correctamente
            const mes = parseInt(partes[1], 10) - 1; // Los meses son 0-indexados
            const anio = parseInt(partes[0], 10);
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


export function transformHeader(header) {
    // Validar que el header sea un string
    if (typeof header !== 'string') {
        return 'Sin título'; // Valor por defecto
    }
    // Reemplazar guiones bajos por espacios y capitalizar cada palabra
    return header.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
}

export function formatNumber(value, isCurrency = false, key = '') {
    // Lista de claves que no deben ser formateadas
    const keysToExcludeFromFormatting = [];


    // Si la clave está en la lista de exclusión, devolver el valor sin cambios
    if (keysToExcludeFromFormatting.includes(key)) {
        return value;
    }

    if (value == null || value === '') {
        return ' - ';
    }

    // Convertir el valor a una cadena si no lo es
    let valueStr = value.toString().trim();

    // Si el valor es una cadena y comienza con $, limpiarlo
    if (valueStr.startsWith('$')) {
        isCurrency = true;
        valueStr = valueStr.replace(/^\$/, ''); // Elimina el símbolo $
    }
    valueStr = valueStr.replace(/,/g, ''); // Elimina comas si las hay

    // Convierte el valor a número
    const numericValue = parseFloat(valueStr);

    if (isNaN(numericValue)) {
        return value; // Devuelve el valor original si no es un número válido
    }

    // Si el valor es 0 , devolverlo en rojo y negrita
    if (numericValue === 0) {
        return '<span style="color: red; font-weight: bold; text-align: right;" > 0 </span>';
    }

    if(numericValue < 0){
        return '<span style="color: red; font-weight: bold; text-align: right;">' + numericValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '</span>';
    }

    // Formatear el número con o sin símbolo de moneda
    const formattedValue = numericValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

    return isCurrency ? `$${formattedValue}` : formattedValue;
}

export function errorParametros(estado, mensaje = 'Ocurrió un error al procesar los parámetros.') {
    
    // Obtener el contenedor principal
    const bodyVentaDevoluciones = document.getElementById('body-venta-devoluciones');
    if (!bodyVentaDevoluciones) {
        console.error('No se encontró el contenedor con id "body-venta-devoluciones".');
        return;
    }

    // Limpiar alertas existentes
    const alertas = document.querySelectorAll('.alertContainer-ventas-devoluciones .alert');
    alertas.forEach(alert => alert.remove());
    
    // Si el estado es true, agregar la alerta
    if (estado) {
        bodyVentaDevoluciones.insertAdjacentHTML('afterbegin', `
            <div class="alert alert-danger fade show text-center" role="alert">
                <strong>¡Oops!</strong> ${mensaje}
            </div> 
        `);

        setTimeout(() => {
            bodyVentaDevoluciones.querySelector('.alert').remove();
        }, 1000);
    }
}

export function errorParametrosProductos(estado, mensaje = 'Ocurrió un error al procesar los parámetros.') {
    
    // Obtener el contenedor principal
    const bodyVentaDevoluciones = document.getElementById('body-distribucion-productos');
    if (!bodyVentaDevoluciones) {
        console.error('No se encontró el contenedor con id "body-distribucion-productos".');
        return;
    }

    // Limpiar alertas existentes
    const alertas = document.querySelectorAll('.alertContainer-productos');
    alertas.forEach(alert => alert.remove());
    
    // Si el estado es true, agregar la alerta
    if (estado) {
        bodyVentaDevoluciones.insertAdjacentHTML('afterbegin', `
            <div class="alert alert-danger fade show text-center" role="alert">
                <strong>¡Oops!</strong> ${mensaje}
            </div> 
        `);

        setTimeout(() => {
            bodyVentaDevoluciones.querySelector('.alert').remove();
        }, 1000);
    }
}
