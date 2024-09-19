from datetime import date
import calendar

def obtener_rango_fechas():
    # Lista para almacenar los primeros y últimos días de cada mes
    resultado = {}

    # Iterar sobre todos los meses del año actual
    actual_year = date.today().year
    for mes in range(1, 13):
        # Obtener el primer día del mes
        primer_dia = date(actual_year, mes, 1)

        # Obtener el último día del mes
        ultimo_dia = date(actual_year, mes, calendar.monthrange(actual_year, mes)[1])

        # Formato del mes
        nombre_mes = calendar.month_name[mes].lower()

        # Agregar al diccionario con fechas como objetos datetime.date
        resultado[f'{nombre_mes}_inicial'] = primer_dia
        resultado[f'{nombre_mes}_final'] = ultimo_dia

    return resultado
