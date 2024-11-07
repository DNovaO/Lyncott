// validarReportes.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script que se encarga de validar los reportes antes de ser ir a la siguiente página,
    para evitar errores en el backend e incongurencias en el frontend.    
*/ 


function validarFormulario() {
    const categoriaSelect = document.getElementById("categoriaReporte");
    const tipoSelect = document.getElementById("tipoReporte");
    const alertContainer = document.getElementById("alertContainer");
  
    // Limpiar cualquier alerta previa
    alertContainer.style.display = "none";
    alertContainer.innerHTML = "";

    if (categoriaSelect.value === "" && tipoSelect.value === "") {
        mostrarAlerta("Por favor, selecciona una categoría de reporte y un tipo de reporte.");
        return false;
    }
    
    if (categoriaSelect.value === "") {
        mostrarAlerta("Por favor, selecciona una categoría de reporte.");
        return false;
    }

    if (tipoSelect.value === "") {
      mostrarAlerta("Por favor, selecciona un tipo de reporte.");
      return false;
    }
  
    return true; // Permitir el envío del formulario si todo está bien
}
  
function mostrarAlerta(mensaje) {
    const alertContainer = document.getElementById("alertContainer");
    alertContainer.style.display = "block";
    alertContainer.innerHTML = `<strong>Error:</strong> ${mensaje}`;

    setTimeout(() => {
        alertContainer.style.display = "none";
        alertContainer.innerHTML = "";
    }, 3000);
}
  