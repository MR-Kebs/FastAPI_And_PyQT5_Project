from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import httpx
import os

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]

@app.get("/convert")
async def convert(from_currency: str, to_currency: str, amount: float):
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if amount < 0:
        raise HTTPException(status_code=400, detail="Сумма не может быть отрицательной")
    
    if from_currency not in currencies or to_currency not in currencies:
        raise HTTPException(status_code=400, detail=f"Неподдерживаемая валюта. Доступны: {currencies}")

    async with httpx.AsyncClient() as client:
        query = await client.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}")
    
    data = query.json()
    rate = data["conversion_rates"][to_currency]
    result = round(amount * rate, 2)

    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "result": result,
        "rate": rate
    }