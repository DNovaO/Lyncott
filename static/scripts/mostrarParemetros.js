function mostrarCampos() {
    var tipoReporte = document.getElementById("tipo_reporte").dataset.tipo;
    var campoFechaInicio = document.getElementById("campo_fecha_inicio");
    var campoFechaFin = document.getElementById("campo_fecha_fin");
    var campoIdProducto = document.getElementById("campo_id_producto");
    var campoClientes = document.getElementById("campo_clientes");
    var campoSucursal = document.getElementById("campo_sucursal");

    // Definir los campos asociados a cada tipo de reporte
    const camposPorTipoReporte = {
        'reportes_Familia1': [campoFechaInicio, campoFechaFin],
        'reportes_Familia2': [campoFechaInicio, campoFechaFin, campoIdProducto],
        'reportes_Familia3': [campoClientes, campoIdProducto, campoSucursal]
    };

    // Definir los tipos de reporte que requieren la presencia de campos específicos
    const tiposConCamposEspeciales = {
        'Por Cliente': 'reportes_Familia3' // Ejemplo: Si el tipo de reporte es "Por Cliente", se mostrarán los campos asociados a 'reportes_Familia3'
    };

    // Ocultar todos los campos primero
    for (const campo of [campoFechaInicio, campoFechaFin, campoIdProducto, campoClientes, campoSucursal]) {
        campo.style.display = "none";
    }

    // Mostrar los campos asociados al tipo de reporte seleccionado
    const camposAsociados = camposPorTipoReporte[tipoReporte];
    if (camposAsociados) {
        for (const campo of camposAsociados) {
            campo.style.display = "block";
        }
    }

    // Mostrar campos especiales si es necesario
    const tipoReporteEspecial = tiposConCamposEspeciales[tipoReporte];
    if (tipoReporteEspecial) {
        const camposEspeciales = camposPorTipoReporte[tipoReporteEspecial];
        if (camposEspeciales) {
            for (const campo of camposEspeciales) {
                campo.style.display = "block";
            }
        }
    }
}
