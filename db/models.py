from typing import Collection
from sqlalchemy import Column, String, Boolean, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id: int = Column(Integer, primary_key=True)
    username: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    balance = Column(Float, nullable=False, default=0.00)
    registred_at = Column(DateTime, nullable=False)
    is_active: bool = Column(Boolean, default=True)
    role: str = Column(String, nullable=False)
   


class Payment(Base):
    __tablename__ = "payment"
    
    payment_id: int = Column(Integer, primary_key=True)
    value: float = Column(Float, nullable=False, default=0.00)
    created_at: DateTime = Column(DateTime, nullable=False)



class PaymentUser(Base):
    __tablename__ = "paymentuser"

    paymentuser_id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.user_id"))
    payment_id: int = Column(Integer, ForeignKey("payment.payment_id"))



class Game(Base):
    __tablename__ = "game"

    game_id: int  = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False)
    downloads: int = Column(Integer, nullable=False)
    content_path: str = Column(String, nullable=False)
    developer_id: int = Column(Integer, ForeignKey("developer.developer_id"))
    adcampaing_game_metrics = relationship("AdCampaingGameMetric", back_populates="game_metrics")
    type_app: str = Column(String, nullable=False)
    developer_link = relationship("Developer", back_populates="game_link", foreign_keys=[developer_id])



class BlacklistUserGame(Base):
    __tablename__ = "blacklistusergame"

    blacklist_id: int  = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.user_id"))
    game_id: int = Column(Integer, ForeignKey("game.game_id"))




class Developer(Base):
    __tablename__ = "developer"

    developer_id: int  = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    game_link = relationship("Game", back_populates="developer_link")




class DeveloperGame(Base):
    __tablename__ = "developergame"

    developergame_id: int = Column(Integer, primary_key=True)
    developer_id: int  = Column(Integer, ForeignKey("developer.developer_id"))
    game_id: int  = Column(Integer, ForeignKey("game.game_id"))



class AdCampaing(Base):
    __tablename__ = "adcampaing"

    adcampaing_id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    content_path: str = Column(String, nullable=False)
    message: str = Column(String, nullable=False)
    created_at: DateTime = Column(DateTime, nullable=False)
    user_id: int = Column(Integer, ForeignKey("user.user_id"))
    budget: float = Column(Float, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    campaing_metric_link = relationship("AdCampaingGameMetric", back_populates="campaing_link")

class AdCampaingGameMetric(Base):
    __tablename__ = "adcampainggamemetric"

    adcampainggamemetric_id : int = Column(Integer, primary_key=True)
    adcampaing_id: int = Column(Integer, ForeignKey("adcampaing.adcampaing_id"))
    user_id: int = Column(Integer, ForeignKey("user.user_id"))
    game_id: int = Column(Integer, ForeignKey("game.game_id"))
    game_metrics  = relationship("Game", back_populates="adcampaing_game_metrics", foreign_keys=[game_id])
    cpm: float = Column(Float, nullable=False)
    ctr: float = Column(Float, nullable=False)
    cpc: float = Column(Float, nullable=False)
    cr: float = Column(Float, nullable=False)
    cpa: float = Column(Float, nullable=False)
    campaing_link = relationship("AdCampaing", back_populates="campaing_metric_link", foreign_keys=[adcampaing_id])


class AdCampaingGame(Base):
    __tablename__ = "adcampainggame"

    adcampainggame_id: int = Column(Integer, primary_key=True)
    adcampaing_id: int = Column(Integer, ForeignKey("adcampaing.adcampaing_id"))
    game_id: int = Column(Integer, ForeignKey("game.game_id"))