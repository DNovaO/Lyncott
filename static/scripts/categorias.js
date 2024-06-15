function updateTiposReporte() {
  const categoriaSelect = document.getElementById("categoriaReporte");
  const tipoSelect = document.getElementById("tipoReporte");
  const selectedCategoria = categoriaSelect.value;

  // Limpiar tipos de reporte
  tipoSelect.innerHTML = '<option value="">Seleccione un tipo</option>';

  // Agregar los tipos de reporte correspondientes
  if (categoriasReporte[selectedCategoria]) {
    categoriasReporte[selectedCategoria].forEach((tipo) => {
      const option = document.createElement("option");
      option.value = tipo;
      option.textContent = tipo;
      tipoSelect.appendChild(option);
    });
  }
}

