document.addEventListener('DOMContentLoaded', function () {
  const fechaInicialInput = document.getElementById('fecha_inicial');
  const fechaFinalInput = document.getElementById('fecha_final');
  const calendarIconInicial = document.getElementById('calendar-icon-inicial');
  const calendarIconFinal = document.getElementById('calendar-icon-final');

  // Obtener la fecha del primer día del mes actual
  const primerDiaDelMes = new Date();
  primerDiaDelMes.setDate(1); // Establecer el día como 1

  // Formatear la fecha inicial en el formato "d-m-Y"
  const fechaInicial = `${primerDiaDelMes.getDate()}-${primerDiaDelMes.getMonth() + 1}-${primerDiaDelMes.getFullYear()}`;

  // Obtener la fecha actual
  const diaActual = new Date();

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
  configureFlatpickr(fechaInicialInput, fechaInicial);
  configureFlatpickr(fechaFinalInput, diaActual);

  // Abrir el calendario al hacer clic en el icono correspondiente
  calendarIconInicial.addEventListener('click', function () {
    fechaInicialInput._flatpickr.open();
  });

  calendarIconFinal.addEventListener('click', function () {
    fechaFinalInput._flatpickr.open();
  });
});
