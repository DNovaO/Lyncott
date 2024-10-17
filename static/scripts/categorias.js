//categorias.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script que contiene las categorias y tipos de reporte que se utilizan en el sistema.
    Dependiendo la categoria seleccionada se mostrarán los tipos de reporte correspondientes.
    
*/ 


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


