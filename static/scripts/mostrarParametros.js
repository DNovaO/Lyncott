// Script que ayuda a mostrar/ocultar los parametros segun el tipo de reporte.
document.addEventListener("DOMContentLoaded", function () {
  const REPORTE_FAMILIA = {
    // Familia 1
    "Ventas por Tipo de Cliente (Sin Refacturación)": 1,
    "Por Tipo de Cliente (con Refacturación)": 1,
    "Ventas por Zonas Pesos (Sin Refacturación)": 1,
    "Ventas por Zonas Pesos 2019 vs 20XX (Sin Refacturación)": 1,
    "Ventas por Zonas Kilos (Sin Refacturación)": 1,
    "Ventas por Zonas Kilos 2019 vs 20XX (Sin Refacturación)": 1,
    "Comparativa de Notas de Crédito en Kilogramos": 1,
    "Ventas sin Notas de Crédito en Pesos": 1,

    // Familia 2
    "Cierre de Mes": 2,
    "Conciliación de Ventas": 2,

    // Familia 3
    "Tendencia de las Ventas": 3,
    "Tendencia de las Ventas por Sector (2020)": 3,
    "Ventas por Categoría según la Región": 3,
    "Ventas por Producto según la Familia": 3,
    "Ventas de Producto según el Sector": 3,

    // Familia 4
    "Ventas Sin Cargo por Zona": 4,
    "Ventas Sin Cargo por Zona según el Mes": 4,
    "Devoluciones por Sucursal": 4,
    "Comparativa de Ventas y Presupuesto por Zonas en Pesos": 4,
    "Clientes y Consignatarios Activos": 4,

    // Familia 5
    "Folios de Facturas": 5,
    "Devoluciones por Zona en Pesos": 5,
    "Devoluciones por Zona en Kilogramos": 5,

    // Familia 6
    "Ventas por Familia en Pesos (Sin Refacturación)": 6,
    "Ventas por Familia en Pesos 2019 vs 20XX (Sin Refacturación)": 6,
    "Ventas por Familia en Kilos (Sin Refacturación)": 6,
    "Ventas por Familia en Kilos 2019 vs 20XX (Sin Refacturación)": 6,

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
    "Análisis de Ventas por Vendedor": 9,

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
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
      "vendedor_inicial",
      "vendedor_final",
    ],
    3: ["fecha_inicial", "fecha_final", "region"],
    4: ["fecha_inicial", "fecha_final"],
    5: ["sucursal_inicial", "sucursal_final", "fecha_inicial", "fecha_final"],
    6: [
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
      "linea_inicial",
      "linea_final",
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
      "cliente_inicial",
      "cliente_final",
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
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "producto_inicial",
      "producto_final",
      "familia_inicial",
      "familia_final",
    ],
    17: [
      "sucursal_inicial",
      "sucursal_final",
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
    21: ["producto_inicial", "producto_final", "zona"],
    22: [
      "sucursal_inicial",
      "sucursal_final",
      "fecha_inicial",
      "fecha_final",
      "cliente_inicial",
      "cliente_final",
      "grupoCorporativo",
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
      "sucursal_inicial",
      "sucursal_final",
      "cliente_inicial",
      "cliente_final",
      "producto_inicial",
      "producto_final",
    ],
    25: ["fecha_inicial", "fecha_final", "grupoCorporativo"],
  };

  function actualizarFormato() {
    const tipo_reporte = document.getElementById("tipo_reporte");
    const reporteElegido = tipo_reporte.textContent.trim();
    const familia = REPORTE_FAMILIA[reporteElegido];
    const parametros = FAMILIA[familia] || [];
    
    if (!tipo_reporte) {
      console.error("No se encontró el elemento con ID 'tipo_reporte'");
      return;
    }

    if (familia === undefined) {
      console.error(
        "No se encontró familia para el reporte seleccionado:",
        reporteElegido
      );
      return;
    }


    // Ocultar todos los campos primero
    document.querySelectorAll(".parametro").forEach((field) => {
      field.style.display = "none";
    });

    // Mostrar solo los campos correspondientes a los parámetros disponibles
    parametros.forEach((paramName) => {
      const field = document.querySelector(`.${paramName}`);
      if (field) {
        field.style.display = "block";
      }
    });
  }

  window.onload = function () {
    actualizarFormato(); // Llamar inicialmente para establecer el estado inicial
  };
});
