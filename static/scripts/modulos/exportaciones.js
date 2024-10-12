//exportaciones.js
import { formatNumber, transformHeader } from "./utils.js";
// Función para remover etiquetas HTML de los valores
function removeHTMLTags(str) {
    if (typeof str === 'string') {
        return str.replace(/<\/?[^>]+(>|$)/g, "");  // Remueve las etiquetas HTML
    }
    return str;  // Si no es una cadena, retorna el valor sin modificaciones
}

export function exportToCSV(dataGlobal, filename) {
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
export function exportToExcel(dataGlobal, filename) {
    const { campos_reporte, datos_completos } = dataGlobal;

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

// Funcion para imprimir
export function imprimirInformacion(dataGlobal, filename) {
    const { campos_reporte, datos_completos } = dataGlobal;

    // Crear el HTML para el reporte
    let printWindow = window.open('', '', 'width=800,height=600');
    
    // Agregar título y estilos básicos para impresión
    printWindow.document.write(`
        <html>
        <head>
            <title>${filename}</title>
            <style>
                body { font-family: Arial, sans-serif; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                h1 { text-align: center; }
            </style>
        </head>
        <body>
            <h1>${filename}</h1>
            <table>
                <thead>
                    <tr>
                        ${campos_reporte.map(field => `<th>${transformHeader(field)}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
                    ${datos_completos.map(row => `
                        <tr>
                            ${campos_reporte.map(field => {
                                // Formatear y limpiar los valores para impresión
                                const formattedValue = formatNumber(row[field], false, field);
                                const cleanValue = removeHTMLTags(formattedValue);
                                return `<td>${cleanValue}</td>`;
                            }).join('')}
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </body>
        </html>
    `);

    // Espera un momento para cargar el contenido y luego lanza la impresión
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();

    // Cierra la ventana de impresión después de imprimir
    printWindow.close();
}
