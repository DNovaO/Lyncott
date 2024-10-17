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

  // Obtener la fecha del primer día del mes actual
  const primerDiaDelMes = new Date();
  primerDiaDelMes.setDate(1); // Establecer el día como 1

  // Función para obtener la fecha en formato "d-m-Y"
  function obtenerFechaFormateada(fecha) {
    return `${('0' + fecha.getDate()).slice(-2)}-${('0' + (fecha.getMonth() + 1)).slice(-2)}-${fecha.getFullYear()}`;
  }

  // Formatear la fecha inicial en el formato "d-m-Y"
  const fechaInicial = obtenerFechaFormateada(primerDiaDelMes);

  // Función para configurar Flatpickr
  function configureFlatpickr(input, defaultDate) {
    flatpickr(input, {
      dateFormat: "d-m-Y",
      defaultDate: defaultDate,
      onReady: function(selectedDates, dateStr, instance) {
        // Actualizar el input con la fecha seleccionada al cargar
        input.value = instance.formatDate(defaultDate, "d-m-Y");
      },
      onChange: function(selectedDates, dateStr, instance) {
        // Actualizar el input con la fecha seleccionada
        input.value = dateStr;
      }
    });
  }

  // Configurar Flatpickr para ambos inputs
  configureFlatpickr(fechaInicialInput, primerDiaDelMes); // Usar primer día del mes actual como predeterminado
  configureFlatpickr(fechaFinalInput, new Date()); // Usar fecha actual como predeterminada

  // Abrir el calendario al hacer clic en el icono correspondiente
  calendarIconInicial.addEventListener('click', function () {
    fechaInicialInput._flatpickr.open();
  });

  calendarIconFinal.addEventListener('click', function () {
    fechaFinalInput._flatpickr.open();
  });
});
