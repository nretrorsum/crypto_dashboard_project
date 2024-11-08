from abc import ABC, abstractmethod

class Database(ABC):

    @abstractmethod
    async def get_user(self, user_id, model):
        raise NotImplementedError

    @abstractmethod
    async def get_portfolio(self, user_id, model):
        raise NotImplementedError

    @abstractmethod
    async def add_portfolio(self, user_id, model):
        raise NotImplementedError
