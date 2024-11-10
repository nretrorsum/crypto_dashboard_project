from datetime import datetime
from decimal import Decimal
from typing import Dict, Any

from fastapi import HTTPException

from database.database_models import UserPortfolio
from routers.schemas import ReadPortfolio


class Investment:
    def __init__(self, repository, data_request):
        self.repository = repository
        self.foreign_api_data = data_request

    async def get_portfolio_data(self, user_id, portfolio_id):
        # Отримуємо портфель для користувача, де кожен елемент це словник
        portfolio_data = await self.repository.get_portfolio_by_user(user_id, portfolio_id, UserPortfolio)
        return portfolio_data

    @staticmethod
    def calculate_roi(ticker: str, value: Decimal, purchase_price: Decimal, current_price: Decimal):
        # Розрахунок ROI
        roi = ((current_price - purchase_price) / purchase_price) * 100
        profit = (current_price - purchase_price) * value
        return {"roi": round(roi, 2), "profit": round(profit, 2)}

    async def calculate_portfolio_performance(self, user_id: int, portfolio_id: int):
        # Отримуємо дані портфеля
        portfolio_data = await self.get_portfolio_data(user_id, portfolio_id)

        # Якщо портфель не знайдений
        if not portfolio_data:
            return {"status": "error", "message": "Portfolio not found"}

        # Тепер ми працюємо з одиничним об'єктом, а не зі списком
        ticker = portfolio_data['ticker']
        purchase_price = Decimal(portfolio_data['price'])
        value = Decimal(portfolio_data['value'])
        setup_time = portfolio_data['setup_time']

        # Отримання поточної ціни з API
        current_price = await self.get_current_price(ticker)

        # Розрахунок ROI та прибутку
        roi_data = self.calculate_roi(ticker, value, purchase_price, current_price)

        # Повертаємо результат
        return {
            "ticker": ticker,
            "purchase_price": purchase_price,
            "current_price": current_price,
            "value": value,
            "setup_time": setup_time,
            **roi_data
        }

    async def get_current_price(self, ticker: str):
        data = await self.foreign_api_data.get_coin_data(ticker)
        if "error" in data:
            raise HTTPException(status_code=404, detail="Coin data not found")
        return Decimal(data['price'])

