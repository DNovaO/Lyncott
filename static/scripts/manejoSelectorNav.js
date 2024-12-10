// Manejo de la barra de navegación

/*
    Diego Nova Olguín
    Ultima modificación: 7/11/2024

    Script que se encarga de manejar los cambios de categoría y tipo de reporte en la página de reportes.
    Provocando un redireccionamiento a la página de reportes con los nuevos parámetros del reporte seleccionado.  
*/ 

const categoriasReporte = {
    "Ventas": [
        "Cierre de Mes",
        "Comparativo de Ventas por Producto (Sin Refacturación)",
        "Comparativo Precios, Reales vs Teoricos y Venta Simulada",
        "Lista de Precios por Producto y por Zonas",
        "Por Cliente",
        "Por Producto",
        "Tendencia de las Ventas",
        "Tendencia de las Ventas por Sector (2020)",
        "Trazabilidad por Producto",
        "Ventas de Credito y Contado (Sin Refacturación)",
        "Ventas en Cadenas FoodService",
        "Ventas en General (Pesos Sin Refacturación)",
        "Ventas por Tipo de Cliente (Sin Refacturación)"
    ],
    "Contable": [
        "Credito Contable (con Refacturación)",
        "Folios de Facturas",
        "Por Familia en Kilos (con Refacturación)",
        "Por Producto (con Refacturación)",
        "Por Tipo de Cliente (con Refacturación)"
    ],
    "Indicadores": [
        "Análisis Semanal de los Principales Contribuyentes a través del Principio 80/20",
        "Avance de Ventas por Vendedor",
        "Comparativa de Notas de Crédito en Kilogramos",
        "Comparativa de Ventas y Presupuesto por Zonas en Pesos",
        "Informe de Ventas por Zonas en Kilogramos y por Marca (Sin Refacturación)",
        "Informe de Ventas por Zonas en Pesos",
        "Ventas Contra Devoluciones",
        "Ventas Sin Cargo",
        "Ventas sin Notas de Credito en Pesos",
        "Ventas de Cadenas AutoService KAM",
        "Ventas de Cadenas FoodService KAM",
        "Ventas por Familia en Kilos (Sin Refacturación)",
        "Ventas por Familia en Pesos (Sin Refacturación)",
        "Ventas por Zonas Kilos (Sin Refacturación)",
        "Ventas por Zonas Pesos (Sin Refacturación)"
    ],
    "Clientes / Consignatarios / Segmento": [
        "Análisis de Ventas por Vendedor",
        "Clientes por Grupos",
        "Clientes y Consignatarios Activos",
        "Clientes y Productos por Grupo",
        "Consignatarios por Código Postal",
        "Consignatarios por Familia",
        "Consignatarios por Segmento",
        // "Consignatarios por Sucursal",
        "Ventas a Clientes/Consignatarios por Mes",
        "Ventas de Clientes por Grupo, Consignatario y Producto"
    ],
    "Regional": [
        "Ventas Sin Cargo por Zona",
        "Ventas Sin Cargo por Zona según el Mes",
        "Ventas por Producto por Giro",
        "Ventas por Familia por Producto",
        "Ventas por Familia por Región",
    ],
    "Devoluciones": [
        "Devoluciones a Clientes/Consignatarios por Semana",
        "Devoluciones a Clientes/Consignatarios por Mes",
        "Devoluciones por Fecha",
        "Devoluciones por Sucursal",
        "Devoluciones por Zona en Kilogramos",
        "Devoluciones por Zona en Pesos",
    ],
};

window.addEventListener('pageshow', () => {
    cargarCategorias();
    updateTiposReporte();
});

// Función para generar las categorías en el primer select
function cargarCategorias() {
    const categoriaSelect = document.getElementById('categoriaReporte');
    
    // Limpiar las opciones existentes
    categoriaSelect.innerHTML = '<option value="" class="opacity-50">Seleccione una categoría</option>';
    
    // Agregar las opciones de las categorías
    for (const categoria in categoriasReporte) {
        const option = document.createElement('option');
        option.value = categoria;
        option.textContent = categoria;
        categoriaSelect.appendChild(option);
    }

    // Restaurar selección previa si existe en localStorage
    const categoriaGuardada = localStorage.getItem('categoriaSeleccionada');
    if (categoriaGuardada) {
        categoriaSelect.value = categoriaGuardada;
    }
}

// Función que actualiza los tipos de reporte en el segundo select
function updateTiposReporte() {
    const categoriaSeleccionada = document.getElementById('categoriaReporte').value;
    const tipoReporteSelect = document.getElementById('tipoReporte');
    
    // Limpiar opciones anteriores
    tipoReporteSelect.innerHTML = '<option value="" class="opacity-50">Seleccione un tipo</option>';

    // Verificar si la categoría seleccionada tiene tipos disponibles
    if (categoriaSeleccionada && categoriasReporte[categoriaSeleccionada]) {
        // Obtener los tipos de reporte para la categoría seleccionada
        const tipos = categoriasReporte[categoriaSeleccionada];
        
        // Agregar las opciones correspondientes al segundo select
        tipos.forEach(tipo => {
            const option = document.createElement('option');
            option.value = tipo;
            option.textContent = tipo;
            tipoReporteSelect.appendChild(option);
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const btnBuscarReporte = document.getElementById('btnBuscarReporte');
    const categoriaSelect = document.getElementById('categoriaReporte');
    const tipoSelect = document.getElementById('tipoReporte');
    const alertContainer = document.getElementById("alertContainer");
  
    let currentPage = 0;

    // Guardar la selección del selector en localStorage al cambiar
    categoriaSelect.addEventListener('change', () => {
        localStorage.setItem('categoriaSeleccionada', categoriaSelect.value);
        updateTiposReporte();
    });

    btnBuscarReporte.addEventListener('click', async (e) => {
        e.preventDefault(); 
        
        const categoriaValue = categoriaSelect.value;
        const tipoValue = tipoSelect.value;

        if (categoriaValue === "" || tipoValue === "") {
            mostrarAlerta("Por favor, selecciona una categoría y un tipo de reporte.");
            return;
        }

        const endpointURL = `/report/?categoria_reporte=${encodeURIComponent(categoriaValue)}&tipo_reporte=${encodeURIComponent(tipoValue)}&page=${currentPage}`;

        const body = {
            nuevo_tipo: tipoValue,
            nueva_categoria: categoriaValue,
            page: currentPage,
            cambio: true,
        };

        try {
            const response = await fetch(endpointURL, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify(body),
            });

            if (response.ok) {
                const result = await response.json();
                if (result.redirect_url) {
                    window.location.href = result.redirect_url;
                } else {
                    mostrarAlerta("No se pudo redirigir a la página de reportes.");
                }
            } else {
                throw new Error('Error en la respuesta del servidor');
            }
        } catch (error) {
            console.error('Error en la solicitud fetch:', error);
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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

// Cargar las categorías cuando la página se cargue
document.addEventListener('DOMContentLoaded', cargarCategorias);
