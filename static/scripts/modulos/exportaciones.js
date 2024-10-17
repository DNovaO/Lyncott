//exportaciones.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script que contiene funciones de utilidad para exportar los datos a CSV, Excel e imprimir el informe.
    Manejo de la logica para que los botones funcionen de la manera correcta
    
*/ 

import { formatNumber, transformHeader } from "./utils.js";
import { tipo_reporte } from "./config.js";


// Función para remover etiquetas HTML de los valores
function removeHTMLTags(str) {
    if (typeof str === 'string') {
        return str.replace(/<\/?[^>]+(>|$)/g, "");  // Remueve las etiquetas HTML
    }
    return str;  // Si no es una cadena, retorna el valor sin modificaciones
}

export function exportToCSV(dataGlobal, tipo_reporte) {
    let filename = tipo_reporte + '.csv';
    const { campos_reporte, datos_completos } = dataGlobal;

    const csvRows = [];
    
    // Agregar encabezados
    csvRows.push(campos_reporte.map(field => transformHeader(field)).join(','));

    // Agregar datos
    datos_completos.forEach(row => {
        const values = campos_reporte.map(field => {
            // Primero formatea el valor
            const formattedValue = formatNumber(row[field], false, field);
            // Luego, remueve cualquier HTML en el valor formateado
            const cleanValue = removeHTMLTags(formattedValue);
            // Escapa el valor para CSV
            const escaped = cleanValue.replace(/"/g, '""');
            return `"${escaped}"`;
        });
        csvRows.push(values.join(','));
    });

    const csvString = csvRows.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.click();
}

// Función para exportar a Excel
export function exportToExcel(dataGlobal, tipo_reporte) {
    const { campos_reporte, datos_completos } = dataGlobal;
    let filename = tipo_reporte + '.xlsx';

    // Filtrar datos y aplicar formato
    const filteredData = datos_completos.map(item => {
        const filteredItem = {};
        campos_reporte.forEach(field => {
            // Primero formatea el valor
            const formattedValue = formatNumber(item[field], false, field);
            // Luego, remueve cualquier HTML en el valor formateado
            const cleanValue = removeHTMLTags(formattedValue);
            // Asigna el valor limpio
            filteredItem[transformHeader(field)] = cleanValue;
        });
        return filteredItem;
    });

    const ws = XLSX.utils.json_to_sheet(filteredData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

    XLSX.writeFile(wb, filename);
}

// Función para imprimir el informe
// Función para imprimir el informe
export async function imprimirInformacion(dataGlobal, tipo_reporte ) {
    const { campos_reporte, datos_completos } = dataGlobal;
    let filename = tipo_reporte;

    // Comprobar que los datos necesarios están disponibles
    if (!campos_reporte || !datos_completos) {
        console.error('Datos incompletos para imprimir el informe.');
        return;
    }

    // Crear el HTML para el reporte
    let printWindow = window.open('', '', 'width=800,height=600');

    // Obtener las filas de totales por ID
    const filaTotalPagina = document.getElementById('total-pagina');
    const filaTotalGlobal = document.getElementById('total-pagina-global');
    const graphCanvas = document.getElementById('chartCanvas'); // Obtener el canvas de la gráfica

    // Convertir las filas de totales a HTML
    const filaTotalPaginaHTML = filaTotalPagina ? filaTotalPagina.outerHTML : '';
    const filaTotalGlobalHTML = filaTotalGlobal ? filaTotalGlobal.outerHTML : '';

    // Verificar que el canvas existe y convertirlo a imagen
    let graphImage = '';
    if (graphCanvas) {
        graphImage = await new Promise((resolve) => {
            graphCanvas.toBlob((blob) => {
                if (blob) {
                    const url = URL.createObjectURL(blob);
                    resolve(url);
                } else {
                    resolve('');
                }
            });
        });
    }

    // Agregar título y estilos básicos para impresión
    printWindow.document.write(`
        <html>
        <head>
            <title>${filename}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                h1 { text-align: center; margin-bottom: 20px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                tr:hover { background-color: #f1f1f1; }
                img { display: block; margin: 0 auto; }
                @media print {
                    body { -webkit-print-color-adjust: exact; }
                }
            </style>
        </head>
        <body>
            <h1>${filename}</h1>
            <table>
                <thead>
                    <tr>
                        <th scope="col" class="numero-tabla">#</th>
                        ${campos_reporte.map(field => `<th>${transformHeader(field)}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
                    ${datos_completos.map((row, index) => `
                        <tr>
                            <th scope="row" class="numero-tabla">${index + 1}</th>  <!-- Número de fila -->
                            ${campos_reporte.map(field => {
                                // Formatear y limpiar los valores para impresión
                                const formattedValue = formatNumber(row[field], false, field);
                                const cleanValue = removeHTMLTags(formattedValue);
                                return `<td>${cleanValue}</td>`;
                            }).join('')}
                        </tr>
                    `).join('')}
                    
                    ${filaTotalPaginaHTML}  <!-- Agregar la fila de Totales de Página -->
                    ${filaTotalGlobalHTML}  <!-- Agregar la fila de Totales Globales -->
                </tbody>
            </table>

            ${graphImage ? `<img src="${graphImage}" alt="Gráfica" style="width: 100%; max-width: 800px;" />` : ''}  <!-- Agregar la gráfica como imagen -->

        </body>
        </html>
    `);

    // Espera un momento para cargar el contenido y luego lanza la impresión
    printWindow.document.close();
    printWindow.focus();

    // Usar un timeout para asegurar que la gráfica esté completamente renderizada antes de imprimir
    setTimeout(() => {
        printWindow.print();
        printWindow.close();
    }, 500); // Espera 500 ms
}
