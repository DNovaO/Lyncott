//exportaciones.js

/*
    Diego Nova Olguín
    Ultima modificación: 17/10/2024

    Script que contiene funciones de utilidad para exportar los datos a CSV, Excel e imprimir el informe.
    Manejo de la logica para que los botones funcionen de la manera correcta
    
*/ 

import { formatNumber, transformHeader } from "./utils.js";

const columnasNoSumar = ['clave_producto', 'descripcion_producto', 'producto', 'sucursal',
    'clave', 'clave_sucursal', 'numero_tipo_documento', 'grupo_movimiento',
    'detalles_tipo_documento', 'almacen_correspondiente', 'moneda', 'zona',
    'orden', 'orden_fecha', 'numero_folio', 'partes_folio', 'partes_fecha',
    'termina_folio', 'nombre', 'zona', 'nombre_producto', 'UPC', 'linea',
    'Promedio_Cliente', 'Promedio_Consignatario', 'fecha', 'dia', 'clave_cliente',
    'consignatario', 'segmentacion', 'clave_grupo_corporativo', 'clave_cliente',
    'clave_consignatario', 'producto', 'No', 'id_vendedor', 'id_almacen',
    'vendedor', 'id_grupo_corporativo', 'grupo_corporativo', 'id_consignatario',
    'consignatario', 'CP', 'colonia', 'folio', 'RFC', 'UUID', 'serie',
    'clave_vendedor', 'nombre_vendedor', 'numero_mes', 'zona_vendedor',
    'nombre_cliente', 'descripcion', 'cliente', 'grupo'
]

// Función para remover etiquetas HTML de los valores
function removeHTMLTags(str) {
    if (typeof str === 'string') {
        return str.replace(/<\/?[^>]+(>|$)/g, "");  // Remueve las etiquetas HTML
    }
    return str;  // Si no es una cadena, retorna el valor sin modificaciones
}

export function exportToCSV(dataGlobal, tipo_reporte) {
    // Validación de la estructura de dataGlobal
    if (!dataGlobal || !dataGlobal.campos_reporte || !dataGlobal.datos_completos) {
        throw new Error("Datos no válidos para la exportación a CSV.");
    }

    let filename = tipo_reporte + '.csv';
    const { campos_reporte, datos_completos } = dataGlobal;

    const csvRows = [];
    
    // Agregar encabezados
    csvRows.push(campos_reporte.map(field => transformHeader(field)).join(','));

    // Agregar datos
    datos_completos.forEach(row => {
        try {
            const values = campos_reporte.map(field => {
                // Manejo de valores no definidos
                const cellValue = row[field] !== undefined ? row[field] : ''; // Valor por defecto

                // Primero formatea el valor y elimina espacios
                const formattedValue = formatNumber(cellValue, false, field).toString().trim();
                // Asegurarse de que el valor formateado sea una cadena
                const cleanValue = removeHTMLTags(formattedValue).trim(); // Convertir a cadena y eliminar espacios
                // Escapa el valor para CSV
                const escaped = cleanValue.replace(/"/g, '""');
                return `"${escaped}"`;
            });
            csvRows.push(values.join(','));
        } catch (error) {
            console.error(`Error procesando la fila: ${JSON.stringify(row)}`, error);
        }
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

export async function imprimirInformacion(dataGlobal, tipo_reporte) {
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
    const filaTotalGlobal = document.getElementById('total-global');
    const graphCanvas = document.getElementById('chartCanvas'); // Obtener el canvas de la gráfica
    const separadoresHabilitados = (dataGlobal.campos_reporte.includes("zona"));
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

    // Agrupar los datos por zona
    const datosPorZona = datos_completos.reduce((acc, row) => {
        if (!acc[row.zona]) {
            acc[row.zona] = [];
        }
        acc[row.zona].push(row);
        return acc;
    }, {});

    // Agregar título y estilos básicos para impresión
    printWindow.document.write(`
        <html>
        <head>
            <title>${filename}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
                h1 { text-align: center; margin-bottom: 20px; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { border: 1px solid #ddd; padding: 5px; text-align: left; }
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
                    ${Object.keys(datosPorZona).map(zona => {
                        const rows = datosPorZona[zona];
                        let zonaTotal = campos_reporte.reduce((totals, field) => {
                            // Comprobar si el campo está en la lista de columnas a no sumar
                            if (columnasNoSumar.includes(field)) {
                                // Si está en la lista, no sumarlo
                                totals[field] = '';
                            } else {
                                // Si no está en la lista, sumar los valores
                                totals[field] = rows.reduce((sum, row) => sum + (parseFloat(row[field]) || 0), 0);
                            }
                            return totals;
                        }, {});
                        

                        let zonaHTML = rows.map((row, index) => {
                            let separadorZona = "";
                            let zonaActual = row.zona;

                            // Aquí se detecta y agrega el separador por zona
                            if (index === 0 || row.zona !== rows[index - 1].zona) {
                                separadorZona = `
                                    <tr class="separador-zona" style="background-color: rgba(112, 224, 0, 1);">
                                        <th colspan="${campos_reporte.length + 1}" style="justify-content:left; font-weight:500; background-color: rgba(112, 224, 0, 0.8);">
                                            Zona: ${zonaActual}
                                        </th>
                                    </tr>
                                `;
                            }

                            return `
                                ${separadorZona}
                                <tr>
                                    <th scope="row" class="numero-tabla">${index + 1}</th>
                                    ${campos_reporte.map(field => {
                                        // Formatear y limpiar los valores para impresión
                                        const formattedValue = formatNumber(row[field], false, field);
                                        const cleanValue = removeHTMLTags(formattedValue);
                                        return `<td>${cleanValue}</td>`;
                                    }).join('')}
                                </tr>
                            `;
                        }).join('');

                        // Agregar la fila de totales por zona
                        let totalesZonaFila = `
                            <tr class="total-zona" style="background-color: rgba(0, 170, 233, 0.5); font-weight:500; justify-content:right;">
                                <th class="separador-zona" style="background-color: rgba(0, 170, 233, 0.5); font-weight:500;">Total: ${transformHeader(zona)}</th>
                                ${campos_reporte.map(field => {
                                    const totalValue = formatNumber(zonaTotal[field], false, field);
                                    return `<td class="datos-tabla" style="background-color: rgba(0, 170, 233, 0.5); text-align:right;"><strong>${totalValue}</strong></td>`;
                                }).join('')}
                            </tr>
                        `;

                        return zonaHTML + totalesZonaFila;
                    }).join('')}
                    
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

