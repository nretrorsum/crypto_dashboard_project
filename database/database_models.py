from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

class UserTable(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    hashed_password = Column(String(150), nullable=False)
    subscription = Column(Integer, ForeignKey('subscriptions.id'),nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    join_date = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_verified = Column(Boolean, nullable=False)

    portfolio = relationship('UserPortfolio', back_populates='user')
    sub = relationship('Subscription', back_populates='user')

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    tag = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

    user = relationship('UserTable', back_populates='sub')

class UserPortfolio(Base):
    __tablename__ = 'user_portfolios'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'),nullable=False)
    ticker = Column(String(50), nullable=False)
    value = Column(DECIMAL(precision=20, scale=5), nullable=False)
    price = Column(DECIMAL(precision=20, scale=5), nullable=False)
    setup_time = Column(TIMESTAMP, nullable=False)

    user = relationship('UserTable', back_populates='portfolio')