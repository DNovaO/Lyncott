export function manejarAccionesBolsa(data) {
    console.log("Datos desde el manejo de API acciones bolsa:", data);
  
    // Referencia al contenedor donde se cargarán las acciones
    const accionesContainer = document.querySelector("#body-acciones-bolsa ul.list-group");
    const loader = document.querySelector("#loader-wrapper-acciones-bolsa");
    const alertContainer = document.querySelector("#alertContainer");
  
    // Limpia el contenido anterior
    accionesContainer.innerHTML = '';
    alertContainer.style.display = 'none';
  
    // Muestra un loader mientras se procesan los datos
    loader.style.display = 'block';
  
    // Simula una pequeña espera (opcional, para UX) y luego renderiza
    setTimeout(() => {
      loader.style.display = 'none';
  
      // Verifica si hay datos
      if (data && data.acciones) {
        const acciones = data.acciones;
  
        // Si hay acciones, renderízalas en la lista
        for (const [symbol, detalles] of Object.entries(acciones)) {
          const listItem = document.createElement('li');
          listItem.className = 'list-group-item d-flex justify-content-between align-items-center p-3';

          // Aseguramos que todo el contenido se muestre con el mismo formato
          if (detalles.error) {
            // Si hubo error con alguna acción, muestra el mensaje
            listItem.classList.add('text-danger');
            listItem.innerHTML = `
              <div class="d-flex flex-column">
                <strong>${symbol}</strong>
                <small>Error: ${detalles.error}</small>
              </div>
            `;
          } else {
            // Renderiza los datos de la acción con formato consistente
            const { latest_close, prev_close, difference } = detalles;
            const differenceClass = difference >= 0 ? 'text-success' : 'text-danger';

            listItem.innerHTML = `
              <div class="d-flex flex-column">
                <strong>${symbol}</strong>
                <span class="text-muted">$${latest_close.toFixed(2)}</span>
                <span class="small text-muted">Previo: $${prev_close.toFixed(2)}</span>
                <span class="${differenceClass} small">
                  (${difference >= 0 ? '+' : ''}${difference.toFixed(2)}%)
                </span>
              </div>
              <div class="badge ${differenceClass}">${difference >= 0 ? 'Sube' : 'Baja'}</div>
            `;
          }

          // Agrega el elemento a la lista
          accionesContainer.appendChild(listItem);
        }
      } else {
        // Si no hay datos, muestra un mensaje de error
        alertContainer.textContent = 'No se encontraron acciones para mostrar.';
        alertContainer.style.display = 'block';
      }
    }, 500); // Simulación del tiempo de espera (opcional)
}
