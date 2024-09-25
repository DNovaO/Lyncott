from datetime import date, timedelta

def f_DifDias(start_date: date, end_date: date, festivos: list) -> int:
    business_days = 0

    # Si las fechas son iguales, retornar 0
    if start_date == end_date:
        return business_days

    current_date = start_date
    while current_date < end_date:  # Verifica hasta el día anterior a end_date
        if current_date.weekday() < 6:  # 0: lunes, 6: domingo
            business_days += 1
        current_date += timedelta(days=1)

    # Filtrar los días festivos que caen dentro del rango
    festivos_datetime = [f for f in festivos if isinstance(f, date)]
    business_days -= sum(1 for f in festivos_datetime if start_date <= f <= end_date)

    return business_days
