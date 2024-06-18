const infoCard = document.getElementById("infoCard");
const infoContent = document.getElementById("infoContent");

const checkboxes = {
  ventas: document.getElementById("checkVentas"),
  contable: document.getElementById("checkContable"),
  indicadores: document.getElementById("checkIndicadores"),
  clientes: document.getElementById("checkClientes"),
  regional: document.getElementById("checkRegional"),
  devoluciones: document.getElementById("checkDevoluciones"),
};

const contentMap = {
  ventas: `
        <div style="text-align: left;">Información de Ventas</div>
        <ul style="text-align: left;">
            <li><strong>Por Producto:</strong> Muestra el volumen y valor de ventas segmentado por producto.<br>
                <strong>Uso:</strong> Identificar productos más vendidos y ajustar estrategias de marketing y producción.</li>
            <li><strong>Por Cliente:</strong> Presenta las ventas totales desglosadas por cliente.<br>
                <strong>Uso:</strong> Evaluar la contribución de cada cliente a las ventas totales y personalizar el servicio.</li>
            <li><strong>Ventas en Cadenas FoodService:</strong> Informe específico de ventas realizadas a través de cadenas de servicios alimentarios.<br>
                <strong>Uso:</strong> Analizar la participación en el mercado de foodservice y optimizar la oferta.</li>
            <!-- Añade más según sea necesario -->
        </ul>
    `,
  contable: `
        <div style="text-align: left;">Información Contable</div>
        <ul style="text-align: left;">
            <li><strong>Por Producto (con Refacturación):</strong> Ventas desglosadas por producto, incluyendo refacturaciones.<br>
                <strong>Uso:</strong> Comprender el impacto completo de las ventas incluyendo ajustes.</li>
            <li><strong>Por Tipo de Cliente (con Refacturación):</strong> Ventas por tipo de cliente, considerando refacturaciones.<br>
                <strong>Uso:</strong> Evaluar la relación completa con cada tipo de cliente.</li>
            <!-- Añade más según sea necesario -->
        </ul>
    `,
  indicadores: `
        <div style="text-align: left;">Información de Indicadores</div>
        <ul style="text-align: left;">
            <li><strong>Ventas por Zonas Pesos (Sin Refacturación):</strong> Ventas en términos monetarios por zona, sin refacturaciones.<br>
                <strong>Uso:</strong> Evaluar el desempeño regional sin ajustes posteriores.</li>
            <li><strong>Ventas por Zonas Pesos 2019 vs 20XX (Sin Refacturación):</strong> Comparativa de ventas por zonas en pesos entre 2019 y un año específico, sin refacturaciones.<br>
                <strong>Uso:</strong> Analizar tendencias y cambios interanuales.</li>
            <!-- Añade más según sea necesario -->
        </ul>
    `,
  // Agrega más categorías según lo necesario
};

function updateInfoCard() {
  let content = "";
  let anyChecked = false;

  Object.keys(checkboxes).forEach((key) => {
    if (checkboxes[key].checked) {
      anyChecked = true;
      content += contentMap[key];
    }
  });

  if (anyChecked) {
    infoContent.innerHTML = content;
    setTimeout(() => {
      infoCard.style.width = "125vh";
      infoCard.style.opacity = "1";
      infoCard.style.transform = "translateX(0)";
      infoCard.style.transition = "all 0.3s ease-in-out";
    }, 200);
  } else {
    infoCard.style.opacity = 0;
    infoCard.style.transform = "translateX(100%)";
    infoCard.style.transition = "all 0.3s ease-in-out";
    setTimeout(() => {
      infoCard.style.width = "0px";
    }, 200);
  }
}

Object.values(checkboxes).forEach((checkbox) => {
  checkbox.addEventListener("change", updateInfoCard);
});
