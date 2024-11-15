from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, DECIMAL, UUID
from sqlalchemy.orm import DeclarativeBase, relationship
import uuid


class Base(DeclarativeBase):
    pass

class UserTable(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    help = relationship('HelpTable', back_populates='user')


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    tag = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)

    user = relationship('UserTable', back_populates='sub')

class UserPortfolio(Base):
    __tablename__ = 'user_portfolios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=False, default=uuid.uuid4)
    ticker = Column(String(50), nullable=False)
    value = Column(DECIMAL(precision=20, scale=5), nullable=False)
    price = Column(DECIMAL(precision=20, scale=5), nullable=False)
    setup_time = Column(TIMESTAMP, nullable=False)

    user = relationship('UserTable', back_populates='portfolio')

class HelpTable(Base):
    __tablename__ = 'help_messages'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    text = Column(String(255), nullable=False)
    add_time = Column(TIMESTAMP, nullable=False)

    user = relationship('UserTable', back_populates='help')