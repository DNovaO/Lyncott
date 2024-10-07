// Script que ayuda a mostrar/ocultar los parametros segun el tipo de reporte.
let numeroParametro = 0;

document.addEventListener("DOMContentLoaded", function () {
  const REPORTE_FAMILIA = {
    // Familia 1
    "Ventas por Tipo de Cliente (Sin Refacturación)": 1,
    "Por Tipo de Cliente (con Refacturación)": 1,
    "Ventas por Zonas Pesos (Sin Refacturación)": 1,
    "Ventas por Zonas Kilos (Sin Refacturación)": 1,
    "Comparativa de Notas de Crédito en Kilogramos": 1,
    "Ventas sin Notas de Crédito en Pesos": 1,

    // Familia 2
    "Cierre de Mes": 2,
    "Conciliación de Ventas": 2,

    // Familia 3

    "Ventas por Categoría según la Región": 3,
    "Ventas por Producto según la Familia": 3,
    "Ventas de Producto según el Sector": 3,

    // Familia 4
    
    "Ventas Sin Cargo por Zona según el Mes": 4,
    "Consignatarios por Sucursal": 4,

    // Familia 5
    "Folios de Facturas": 5,
    "Devoluciones por Zona en Pesos": 5,
    "Devoluciones por Zona en Kilogramos": 5,

    // Familia 6
    "Ventas por Familia en Pesos (Sin Refacturación)": 6,
    "Ventas por Familia en Kilos (Sin Refacturación)": 6,

    // Familia 7
    "Informe de Ventas por Zonas en Pesos": 7,
    "Informe de Ventas por Zonas en Kilogramos y por Marca (Sin Refacturación)": 7,

    // Familia 8
    "Ventas de Cadenas FoodService KAM": 8,
    "Ventas de Cadenas AutoService KAM": 8,

    // Familia 9
    "Avance de Ventas por Vendedor": 9,
    "Análisis Semanal de los Principales Contribuyentes a través del Principio 80/20": 9,
    "Consignatarios por Código Postal": 9,
    
    // Familia 10
    "Por Cliente": 10,
    "Comparativo de Ventas por (Producto Sin Refacturación)": 10,
    "Por Producto (con Refacturación)": 10,
    "Ventas Sin Cargo": 10,
    "Ventas a Clientes/Consignatarios por Mes": 10,

    // Familia 11
    "Por Producto": 11,

    // Familia 12
    "Ventas de Credito y Contado (Sin Refacturación)": 12,
    "Credito Contable (con Refacturación)": 12,

    // Familia 13
    "Ventas en Cadenas FoodService": 13,

    // Familia 14
    "Ventas Contra Devoluciones": 14,
    "Ventas de Clientes por Grupo, Consignatario y Producto": 14,

    // Familia 15
    "Devoluciones por Fecha": 15,

    // Familia 16
    "Por Familia en Kilos (con Refacturación)": 16,

    // Familia 17
    "Consignatarios por Familia": 17,

    // Familia 18
    "Consignatarios por Producto": 18,

    // Familia 19
    "Consignatarios por Segmento": 19,

    // Familia 20
    "Clientes por Grupos": 20,

    // Familia 21
    "Lista de Precios por Producto y por Zonas": 21,

    // Familia 22
    "Comparativo Precios, Reales vs Teoricos y Venta Simulada": 22,

    // Familia 23
    "Trazabilidad por Producto": 23,

    // Familia 24
    "Ventas en General (Pesos Sin Refacturación)": 24,

    // Familia 25
    "Clientes y Productos por Grupo": 25,

    "Comparativa de Ventas y Presupuesto por Zonas en Pesos": 26,

    "Clientes y Consignatarios Activos": 27,

    "Tendencia de las Ventas": 28,
    "Tendencia de las Ventas por Sector (2020)": 28,
    "Devoluciones por Sucursal": 28,
    "Ventas Sin Cargo por Zona": 28,

    "Análisis de Ventas por Vendedor": 29,
  };

  const FAMILIA = {
    1: [
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
      "producto_inicial",
      "producto_final",
    ],
    2: [
      "fecha_inicial",
      "fecha_final",
      "sucursal",
    ],
    3: ["fecha_inicial", "fecha_final", "region"],
    4: ["fecha_inicial", "fecha_final", "sucursal"],
    5: ["sucursal_inicial", "sucursal_final", "fecha_inicial", "fecha_final"],
    6: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "producto_inicial",
      "producto_final",
      "familia_inicial",
      "familia_final",
    ],
    7: [
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
      "producto_inicial",
      "producto_final",
      "marca_inicial",
      "marca_final",
    ],
    8: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "producto_inicial",
      "producto_final",
    ],
    9: ["sucursal", "fecha_inicial", "fecha_final"],
    10: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
      "producto_inicial",
      "producto_final",
    ],
    11: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
      "producto_inicial",
      "producto_final",
      "familia_inicial",
      "familia_final",
    ],

    12: ["fecha_inicial", "fecha_final", "cliente_inicial", "cliente_final"],

    13: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "producto_inicial",
      "producto_final",
    ],
    14: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "grupoCorporativo_inicial",
      "grupoCorporativo_final",
    ],
    15: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "grupoCorporativo",
    ],
    16: [
      "sucursal",
      "fecha_inicial",
      "fecha_final",
      "producto_inicial",
      "producto_final",
      "familia_inicial",
      "familia_final",
    ],
    17: [
      "sucursal",
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
      "familia_inicial",
      "familia_final",
    ],
    18: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
      "producto_inicial",
      "producto_final",
      "segmento_inicial",
      "segmento_final",
    ],
    19: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
    ],
    20: ["grupoCorporativo_inicial", "grupoCorporativo_final"],
    21: ["producto_inicial", "producto_final"],
    
    22: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
      "grupoCorporativo_inicial", 
      "grupoCorporativo_final"
    ],

    23: [
      "sucursal",
      "fecha_inicial",
      "fecha_final",
      "producto_inicial",
      "producto_final",
      "status",
    ],
    24: [
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
      "producto_inicial",
      "producto_final",
    ],
    25: ["fecha_inicial", "fecha_final", "grupoCorporativo"],

    26:['sucursal', 'year'],

    27:["fecha_inicial", "fecha_final"],

    28: ["fecha_inicial", "fecha_final"],

    29: ["fecha_inicial", "fecha_final", "producto_inicial", "producto_final", "cliente_inicial", "cliente_final", "vendedor_inicial", "vendedor_final", "sucursal"],

  };


  function actualizarFormato() {
    numeroParametro = 0;

    const tipo_reporte = document.getElementById("tipo_reporte");
    if (!tipo_reporte) {
        console.error("No se encontró el elemento con ID 'tipo_reporte'");
        return;
    }

    const reporteElegido = tipo_reporte.textContent.trim();
    const familia = REPORTE_FAMILIA[reporteElegido];
    if (familia === undefined) {
        console.error("No se encontró familia para el reporte seleccionado:", reporteElegido);
        return;
    }

    const parametros = FAMILIA[familia] || [];
    const camposParaMostrar = new Set(parametros);

    // Obtener todos los contenedores relevantes
    const todosLosContenedores = document.querySelectorAll(".contenedor-div");

    // Eliminar los contenedores que no contienen parámetros a mostrar
    todosLosContenedores.forEach((contenedor) => {
        // Buscar dentro del contenedor si hay un parámetro que debe ser mostrado
        const parametroEncontrado = Array.from(contenedor.querySelectorAll(".parametro"))
            .some(param => camposParaMostrar.has(param.classList[0]));

        if (!parametroEncontrado) {
            contenedor.style.display = "none";
            // Añadir data-estado="inactivo" a los botones en el contenedor eliminado
            const botones = contenedor.querySelectorAll('button[data-type]');
            botones.forEach(boton => {
                boton.setAttribute('data-estado', 'inactivo');
            });
        } else {
            numeroParametro++;
            contenedor.style.display = "flow-root";
            // Añadir data-estado="activo" a los botones en el contenedor visible
            const botones = contenedor.querySelectorAll('button[data-type]');
            botones.forEach(boton => {
                boton.setAttribute('data-estado', 'activo');
            });
        }
    });

    // Mostrar solo los campos correspondientes a los parámetros disponibles
    parametros.forEach((paramName) => {
        const field = document.querySelector(`.${paramName}`);
        if (field) {
            field.style.display = "inline";
        }
    });

    return numeroParametro;
}

window.onload = function () {
    actualizarFormato();
};

});
