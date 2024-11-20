# f_DifDiasTotales.py

# Diego Nova Olguín
# Ultima modificación: 17/10/2024

# Funcion que tambien se encuentra en la base de datos para la obtencion de los 
# dias totales dentro de un rango de fechas establecido.

from datetime import datetime, date, timedelta
from .f_DifDias import *


def f_DifDiasTotales(start_date: date, end_date: date, festivos: list) -> int:
    total_business_days = 0
    start_date = start_date.replace(day=1)  # Primer día del mes
    last_day_of_month = start_date + timedelta(days=31)  # Último día del mes
    
    if start_date.month == 2:
        last_day_of_month = start_date + timedelta(days=28)
    elif start_date.month in [4, 6, 9, 11]:
        last_day_of_month = start_date + timedelta(days=30)
        
    while start_date <= last_day_of_month:
        last_day_of_month = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        if last_day_of_month > last_day_of_month:
            last_day_of_month = end_date

        # Llamar a la función f_DifDias para contar días hábiles hasta el último día del mes
        total_business_days += f_DifDias(start_date, last_day_of_month, festivos)

        # Avanzar al primer día del mes siguiente
        start_date = (start_date + timedelta(days=31)).replace(day=1)
        
    return total_business_days
        
    
        
        
        
    
    
    
