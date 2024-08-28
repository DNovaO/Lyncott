//exportaciones.js
import { formatNumber, transformHeader } from "./utils.js";

// Función para exportar a CSV
export function exportToCSV(dataGlobal, filename) {
    const { campos_reporte, datos_completos } = dataGlobal;

    const csvRows = [];
    
    // Agregar encabezados
    csvRows.push(campos_reporte.map(field => transformHeader(field)).join(','));

    // Agregar datos
    datos_completos.forEach(row => {
        const values = campos_reporte.map(field => {
            const value = row[field];
            const escaped = ('' + formatNumber(value, false, field)).replace(/"/g, '""');
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
            filteredItem[transformHeader(field)] = formatNumber(item[field], false, field);
        });
        return filteredItem;
    });

    const ws = XLSX.utils.json_to_sheet(filteredData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

    XLSX.writeFile(wb, filename);
}