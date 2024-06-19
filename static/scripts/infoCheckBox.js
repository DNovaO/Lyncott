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
    <div class = "info-section" style="text-align: left;">Información de Ventas</div>
    <ul class = "info-list" style="text-align: left;">
        <li><strong>Por Producto:</strong> Muestra el volumen y valor de ventas segmentado por producto.<br>
            <strong>Uso:</strong> Identificar productos más vendidos y ajustar estrategias de marketing y producción.</li>
        <li><strong>Por Cliente:</strong> Presenta las ventas totales desglosadas por cliente.<br>
            <strong>Uso:</strong> Evaluar la contribución de cada cliente a las ventas totales y personalizar el servicio.</li>
        <li><strong>Ventas en Cadenas FoodService:</strong> Informe específico de ventas realizadas a través de cadenas de servicios alimentarios.<br>
            <strong>Uso:</strong> Analizar la participación en el mercado de foodservice y optimizar la oferta.</li>
        <li><strong>Ventas por Tipo de Cliente (Sin Refacturación):</strong> Detalla las ventas según el tipo de cliente, sin incluir refacturaciones.<br>
            <strong>Uso:</strong> Entender las necesidades y comportamientos de diferentes segmentos de clientes.</li>
        <li><strong>Ventas de Crédito y Contado (Sin Refacturación):</strong> Comparación entre ventas a crédito y ventas al contado, excluyendo refacturaciones.<br>
            <strong>Uso:</strong> Gestionar el flujo de caja y las políticas de crédito.</li>
        <li><strong>Cierre de Mes:</strong> Resumen de todas las ventas realizadas al final de un mes.<br>
            <strong>Uso:</strong> Evaluar el rendimiento mensual y planificar el siguiente periodo.</li>
        <li><strong>Conciliación de Ventas:</strong> Revisión y reconciliación de todas las transacciones de ventas.<br>
            <strong>Uso:</strong> Asegurar la precisión y coherencia en los registros de ventas.</li>
        <li><strong>Lista de Precios por Producto y por Zonas:</strong> Muestra los precios de los productos desglosados por zonas geográficas.<br>
            <strong>Uso:</strong> Ajustar precios según las condiciones del mercado local.</li>
        <li><strong>Comparativo Precios, Reales vs Teóricos y Venta Simulada:</strong> Comparación entre precios reales, teóricos y simulados de ventas.<br>
            <strong>Uso:</strong> Identificar desviaciones y ajustar la estrategia de precios.</li>
        <li><strong>Comparativo de Ventas por Producto (Sin Refacturación):</strong> Compara ventas de diferentes productos excluyendo refacturaciones.<br>
            <strong>Uso:</strong> Determinar el rendimiento relativo de cada producto.</li>
        <li><strong>Ventas en General (Pesos Sin Refacturación):</strong> Informe general de ventas en términos monetarios, sin refacturaciones.<br>
            <strong>Uso:</strong> Obtener una visión global de las ventas.</li>
        <li><strong>Tendencia de las Ventas:</strong> Análisis de la evolución de las ventas a lo largo del tiempo.<br>
            <strong>Uso:</strong> Identificar patrones y tendencias de mercado.</li>
        <li><strong>Tendencia de las Ventas por Sector (2020):</strong> Análisis de la tendencia de ventas por sector durante el año 2020.<br>
            <strong>Uso:</strong> Evaluar el impacto de factores específicos del año 2020.</li>
        <li><strong>Trazabilidad por Producto:</strong> Seguimiento detallado del recorrido de un producto desde la producción hasta la venta.<br>
            <strong>Uso:</strong> Garantizar la calidad y seguridad del producto, así como cumplir con regulaciones.</li>
    </ul>
    `,
  contable: `
    <div class = "info-section" style="text-align: left;">Información Contable</div>
    <ul class = "info-list" style="text-align: left;">
        <li><strong>Por Producto (con Refacturación):</strong> Ventas desglosadas por producto, incluyendo refacturaciones.<br>
            <strong>Uso:</strong> Comprender el impacto completo de las ventas incluyendo ajustes.</li>
        <li><strong>Por Tipo de Cliente (con Refacturación):</strong> Ventas por tipo de cliente, considerando refacturaciones.<br>
            <strong>Uso:</strong> Evaluar la relación completa con cada tipo de cliente.</li>
        <li><strong>Crédito Contable (con Refacturación):</strong> Informe de ventas a crédito, incluyendo refacturaciones.<br>
            <strong>Uso:</strong> Gestionar y analizar la deuda de clientes.</li>
        <li><strong>Por Familia en Kilos (con Refacturación):</strong> Ventas desglosadas por familia de productos en kilos, con refacturaciones.<br>
            <strong>Uso:</strong> Analizar la venta en términos de peso y ajustar la producción.</li>
        <li><strong>Folios de Facturas:</strong> Registro de todos los folios de facturas emitidas.<br>
            <strong>Uso:</strong> Control y seguimiento de la facturación.</li>
    </ul>
    `,
  indicadores: `
    <div class = "info-section" style="text-align: left;">Indicadores</div>
    <ul class = "info-list" style="text-align: left;">
        <li><strong>Ventas por Zonas Pesos (Sin Refacturación):</strong> Ventas en términos monetarios por zona, sin refacturaciones.<br>
            <strong>Uso:</strong> Evaluar el desempeño regional sin ajustes posteriores.</li>
        <li><strong>Ventas por Zonas Pesos 2019 vs 20XX (Sin Refacturación):</strong> Comparativa de ventas por zonas en pesos entre 2019 y un año específico, sin refacturaciones.<br>
            <strong>Uso:</strong> Analizar tendencias y cambios interanuales.</li>
        <li><strong>Ventas por Zonas Kilos (Sin Refacturación):</strong> Ventas por zonas en kilos, excluyendo refacturaciones.<br>
            <strong>Uso:</strong> Evaluar el volumen físico de ventas regionales.</li>
        <li><strong>Ventas por Zonas Kilos 2019 vs 20XX (Sin Refacturación):</strong> Comparativa de ventas por zonas en kilos entre 2019 y un año específico, sin refacturaciones.<br>
            <strong>Uso:</strong> Analizar el crecimiento o decrecimiento del volumen de ventas.</li>
        <li><strong>Ventas por Familia en Pesos (Sin Refacturación):</strong> Ventas en términos monetarios por familia de productos, sin refacturaciones.<br>
            <strong>Uso:</strong> Identificar las familias de productos más rentables.</li>
        <li><strong>Ventas por Familia en Pesos 2019 vs 20XX (Sin Refacturación):</strong> Comparativa de ventas en pesos por familia de productos entre 2019 y un año específico, sin refacturaciones.<br>
            <strong>Uso:</strong> Evaluar el desempeño y cambios en diferentes familias de productos.</li>
        <li><strong>Ventas por Familia en Kilos (Sin Refacturación):</strong> Ventas en kilos por familia de productos, sin refacturaciones.<br>
            <strong>Uso:</strong> Analizar el volumen de ventas por familias de productos.</li>
        <li><strong>Ventas por Familia en Kilos 2019 vs 20XX (Sin Refacturación):</strong> Comparativa de ventas en kilos por familia de productos entre 2019 y un año específico, sin refacturaciones.<br>
            <strong>Uso:</strong> Evaluar las variaciones en la demanda de productos.</li>
        <li><strong>Informe de Ventas por Zonas en Pesos:</strong> Reporte detallado de ventas en pesos desglosado por zonas.<br>
            <strong>Uso:</strong> Entender el rendimiento financiero en diferentes áreas geográficas.</li>
        <li><strong>Informe de Ventas por Zonas en Kilogramos y por Marca (Sin Refacturación):</strong> Detalle de ventas en kilogramos desglosado por zonas y marcas, sin refacturaciones.<br>
            <strong>Uso:</strong> Evaluar el volumen de ventas y el rendimiento de marcas específicas en cada zona.</li>
        <li><strong>Ventas Sin Cargo:</strong> Informe de ventas que no han generado costo.<br>
            <strong>Uso:</strong> Identificar oportunidades y estrategias de promoción.</li>
        <li><strong>Ventas de Cadenas FoodService KAM:</strong> Ventas realizadas a través de cadenas de foodservice gestionadas por Key Account Managers.<br>
            <strong>Uso:</strong> Medir el desempeño de KAM en el segmento de foodservice.</li>
        <li><strong>Ventas de Cadenas AutoService KAM:</strong> Ventas realizadas a través de cadenas de autoservicio gestionadas por Key Account Managers.<br>
            <strong>Uso:</strong> Evaluar la efectividad de las estrategias de autoservicio.</li>
        <li><strong>Comparativa de Notas de Crédito en Kilogramos:</strong> Comparación de notas de crédito emitidas en términos de kilos.<br>
            <strong>Uso:</strong> Analizar devoluciones y ajustes de ventas.</li>
        <li><strong>Ventas sin Notas de Crédito en Pesos:</strong> Ventas netas después de restar las notas de crédito, en pesos.<br>
            <strong>Uso:</strong> Evaluar el impacto de las devoluciones en las ventas totales.</li>
        <li><strong>Avance de Ventas por Vendedor:</strong> Progreso de ventas logrado por cada vendedor.<br>
            <strong>Uso:</strong> Monitorear el desempeño individual de los vendedores.</li>
        <li><strong>Análisis Semanal de los Principales Contribuyentes a través del Principio 80/20:</strong> Informe semanal que identifica los principales contribuyentes a las ventas siguiendo el principio de Pareto.<br>
            <strong>Uso:</strong> Focalizar esfuerzos en los clientes y productos más rentables.</li>
        <li><strong>Ventas Contra Devoluciones:</strong> Comparación entre las ventas realizadas y las devoluciones recibidas.<br>
            <strong>Uso:</strong> Evaluar la satisfacción del cliente y la calidad del producto.</li>
        <li><strong>Comparativa de Ventas y Presupuesto por Zonas en Pesos (Sin Refacturación):</strong> Comparación entre las ventas reales y el presupuesto asignado por zonas, sin refacturaciones.<br>
            <strong>Uso:</strong> Medir la efectividad de las estrategias de ventas y planificación financiera.</li>
    </ul>
    `,

  clientes: `
    <div class = "info-section" style="text-align: left;">Clientes</div>
    <ul class = "info-list" style="text-align: left;">
        <li><strong>Clientes por Grupos:</strong> Listado de clientes organizados por grupos.<br>
            <strong>Uso:</strong> Segmentar clientes para estrategias de marketing y ventas específicas.</li>
        <li><strong>Consignatarios por Código Postal:</strong> Registro de consignatarios según su ubicación postal.<br>
            <strong>Uso:</strong> Analizar la distribución geográfica y optimizar la logística.</li>
        <li><strong>Consignatarios por Segmento:</strong> Clasificación de consignatarios por segmento de mercado.<br>
            <strong>Uso:</strong> Desarrollar estrategias de ventas adaptadas a cada segmento.</li>
        <li><strong>Consignatarios por Producto:</strong> Listado de consignatarios en relación a los productos que manejan.<br>
            <strong>Uso:</strong> Identificar la demanda de productos específicos por consignatarios.</li>
        <li><strong>Consignatarios por Familia:</strong> Registro de consignatarios según la familia de productos.<br>
            <strong>Uso:</strong> Evaluar la distribución de productos por consignatarios.</li>
        <li><strong>Ventas a Clientes/Consignatarios por Mes:</strong> Detalle mensual de ventas a clientes y consignatarios.<br>
            <strong>Uso:</strong> Monitorear el comportamiento de compras y ventas en diferentes periodos.</li>
        <li><strong>Ventas de Clientes por Grupo, Consignatario y Producto:</strong> Ventas desglosadas por grupo de clientes, consignatario y producto.<br>
            <strong>Uso:</strong> Análisis detallado para mejorar la segmentación y estrategias de ventas.</li>
        <li><strong>Clientes y Productos por Grupo:</strong> Listado de clientes y los productos que adquieren, organizados por grupos.<br>
            <strong>Uso:</strong> Mejorar la personalización del servicio y la oferta de productos.</li>
        <li><strong>Consignatarios por Sucursal:</strong> Registro de consignatarios distribuidos por sucursal.<br>
            <strong>Uso:</strong> Evaluar la efectividad de las sucursales en la gestión de consignatarios.</li>
        <li><strong>Análisis de Ventas por Vendedor:</strong> Desglose de ventas realizadas por cada vendedor.<br>
            <strong>Uso:</strong> Identificar fortalezas y áreas de mejora para cada miembro del equipo de ventas.</li>
        <li><strong>Clientes y Consignatarios Activos:</strong> Listado de clientes y consignatarios que han realizado transacciones recientemente.<br>
            <strong>Uso:</strong> Mantener un registro actualizado para estrategias de fidelización y servicio al cliente.</li>
    </ul>
    `,

  regional: `
    <div class = "info-section" style="text-align: left;">Regional</div>
    <ul class = "info-list" style="text-align: left;">
        <li><strong>Ventas por Categoría según la Región:</strong> Desglose de ventas por categoría de producto en diferentes regiones.<br>
            <strong>Uso:</strong> Adaptar estrategias de ventas y marketing a las características regionales.</li>
        <li><strong>Ventas por Producto según la Familia:</strong> Ventas de productos organizadas por familias en diferentes regiones.<br>
            <strong>Uso:</strong> Analizar la demanda y ajustar la producción y distribución.</li>
        <li><strong>Ventas de Producto según el Sector:</strong> Ventas desglosadas por sector económico y tipo de producto.<br>
            <strong>Uso:</strong> Evaluar el rendimiento de productos en diversos sectores del mercado.</li>
        <li><strong>Ventas Sin Cargo por Zona:</strong> Registro de ventas realizadas sin cargo en diferentes zonas.<br>
            <strong>Uso:</strong> Analizar promociones y estrategias de marketing gratuitas.</li>
        <li><strong>Ventas Sin Cargo por Zona según el Mes:</strong> Ventas sin cargo desglosadas por zona y mes.<br>
            <strong>Uso:</strong> Evaluar el impacto temporal y regional de promociones gratuitas.</li>
    </ul>
  `,

  devoluciones:`
    <div class="info-section" style="text-align: left;">Devoluciones</div>
    <ul class="info-list" style="text-align: left;">
        <li><strong>Devoluciones por Fecha:</strong> Registro de devoluciones de productos organizadas por fecha.<br>
            <strong>Uso:</strong> Identificar patrones y causas de devoluciones en periodos específicos.</li>
        <li><strong>Devoluciones por Sucursal:</strong> Detalle de devoluciones recibidas en cada sucursal.<br>
            <strong>Uso:</strong> Evaluar el desempeño y la calidad del servicio en cada sucursal.</li>
        <li><strong>Devoluciones por Zona en Pesos:</strong> Análisis de devoluciones en términos monetarios desglosadas por zona.<br>
            <strong>Uso:</strong> Medir el impacto financiero de las devoluciones en diferentes áreas.</li>
        <li><strong>Devoluciones por Zona en Kilogramos:</strong> Registro de devoluciones en kilos, desglosado por zona.<br>
            <strong>Uso:</strong> Evaluar el volumen de productos devueltos y las razones por zona.</li>
    </ul>

  `, 

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

  //Cuando se añade la informacion
  if (anyChecked) {
    infoContent.innerHTML = content;
    setTimeout(() => {
      infoCard.style.width = "110vh";
      infoCard.style.opacity = "1";
      infoCard.style.transform = "translateX(0)";
      infoCard.style.transition = "all 0.3s ease-in-out";
      infoContent.style.overflowY = "auto";
      infoContent.style.maxHeight = "40vh";
    }, 200);
  
  //Cuando se retrae toda la información
  } else {
    infoCard.style.opacity = 0;
    infoCard.style.width = "0px";
    infoCard.style.transform = "translateX(100%)";
    infoCard.style.transition = "all 0.3s ease-in-out";
    setTimeout(() => {
      infoContent.innerHTML = ""; // Resetea el contenido al tamaño original
      infoCard.style.width = "0px";
    }, 200);
  }
}

Object.values(checkboxes).forEach((checkbox) => {
  checkbox.addEventListener("change", updateInfoCard);
});
