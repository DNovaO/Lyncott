// formatoFecha.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script que contiene multiples funciones para el manejo de las fechas, obtener las fechas, formatearlas y modificarlas.    
*/ 

document.addEventListener('DOMContentLoaded', function () {
  const fechaInicialInput = document.getElementById('fecha_inicial');
  const fechaFinalInput = document.getElementById('fecha_final');
  const calendarIconInicial = document.getElementById('calendar-icon-inicial');
  const calendarIconFinal = document.getElementById('calendar-icon-final');

  // Obtener el primer día del mes actual
  const primerDiaDelMes = new Date();
  primerDiaDelMes.setDate(1);

  // Formatear la fecha "d-m-Y"
  function obtenerFechaFormateada(fecha) {
    return `${('0' + fecha.getDate()).slice(-2)}-${('0' + (fecha.getMonth() + 1)).slice(-2)}-${fecha.getFullYear()}`;
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
          shorthand: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Оct', 'Nov', 'Dic'],
          longhand: ['Enero', 'Febrero', 'Мarzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
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

  // Inicializar Flatpickr
  configurarFlatpickr(fechaInicialInput, primerDiaDelMes);
  configurarFlatpickr(fechaFinalInput, new Date());

  // Abrir calendario al hacer clic en el ícono
  calendarIconInicial.addEventListener('click', function () {
    fechaInicialInput._flatpickr.open();
  });

  calendarIconFinal.addEventListener('click', function () {
    fechaFinalInput._flatpickr.open();
  });
});
