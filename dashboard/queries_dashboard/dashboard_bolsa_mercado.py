import requests

FINNHUB_API_KEY = "cu8gvs1r01qt63vgvnj0cu8gvs1r01qt63vgvnjg"

def get_stock_data(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "c" in data and "pc" in data:  # Verifica que existan los campos necesarios
            latest_close = data["c"]
            prev_close = data["pc"]

            # Evita división por cero
            if prev_close != 0:
                difference = ((latest_close - prev_close) / prev_close) * 100
            else:
                difference = None  # Indica que no se puede calcular la diferencia

            return {
                "symbol": symbol,
                "latest_close": latest_close,
                "prev_close": prev_close,
                "difference": difference
            }
        else:
            return {"error": f"No se encontraron datos válidos para {symbol}"}
    except requests.RequestException as e:
        return {"error": f"Error al conectar con la API: {str(e)}"}
