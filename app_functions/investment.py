from decimal import Decimal
from api_processing.api_request import coin_data_request
from fastapi import HTTPException
from database.repository import repository
from database.database_models import UserPortfolio


class Investment:
    def __init__(self, repository, coin_request):
        self.repository = repository
        self.coin_request = coin_request

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
        portfolio_data = await self.get_portfolio_data(user_id, portfolio_id)

        if not portfolio_data:
            return {"status": "error", "message": "Portfolio not found"}

        ticker = portfolio_data.ticker
        purchase_price = Decimal(portfolio_data.price)
        value = Decimal(portfolio_data.value)
        setup_time = portfolio_data.setup_time

        current_price = await self.get_current_price(ticker)

        roi_data = self.calculate_roi(ticker, value, purchase_price, current_price)

        return {
            "ticker": ticker,
            "purchase_price": purchase_price,
            "current_price": current_price,
            "value": value,
            "setup_time": setup_time,
            **roi_data
        }

    async def get_current_price(self, ticker: str):
        data = await self.coin_request.get_coin_data_by_symbol(ticker)

        if isinstance(data, list) and data:
            price_data = data[0]
            try:
                price = price_data['quote']['USD']['price']
                return Decimal(price)
            except KeyError:
                print("No 'price' key in requested data structure", price_data)
                raise HTTPException(status_code=404, detail="Price data not found for ticker.")
        else:
            print("Unresolved data structure:", data)
            raise HTTPException(status_code=404, detail="Coin data not found")

investment = Investment(repository, coin_data_request)


