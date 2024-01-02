from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_, select, exists, delete
from sqlalchemy.orm import joinedload
from enum import Enum
from api.models import Metric

from db.models import User
from db.models import AdCampaing
from db.models import AdCampaingGameMetric
from db.models import DeveloperGame, Developer
from db.models import Game
from datetime import datetime
from typing import List

class PlatformRole(str, Enum):
    ROLE_USER = "ROLE_USER"
    ROLE_ADMIN = "ROLE_ADMIN"
    ROLE_SUPERUSER = "ROLE_SUPERUSER"


class UserDAL():
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, email: str, hashed_password: str, role: str, registred_at: datetime) -> User:
        new_user = User(
            username = name,
            email = email,
            hashed_password = hashed_password,
            role=role,
            registred_at = registred_at
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        await self.db_session.commit()
        return new_user
    

    async def delete_user(self, user_id: int) -> Union[int, None]:
        query = update(User).\
            where(and_(User.user_id == user_id, User.is_active == True)).\
            values(is_active=False).\
            returning(User.user_id)
        res = await self.db_session.execute(query)
        deleted_users_id_row = res.fetchone()
        if deleted_users_id_row is not None:
            return deleted_users_id_row[0]


    async def get_user_by_id(self, user_id: int) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]


    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
    

    async def update_user(self, user_id: int, **kwargs) -> Union[int, None]:
        query = update(User).\
            where(and_(User.user_id == user_id, User.is_active == True)).\
            values(kwargs)
        await self.db_session.execute(query)





class AdCampaingDAL():

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_campaing(self, name: str, message: str, content_path: str, registred_at: datetime, user_id: int, budget: float) -> AdCampaing:
        new_campaing = AdCampaing(
            name = name,
            message = message,
            content_path = content_path,
            created_at = registred_at,
            user_id = user_id,
            budget = budget
        )
        self.db_session.add(new_campaing)
        await self.db_session.flush()
        await self.db_session.commit()
        return new_campaing

    async def get_campaings_user_own(self, user_id: int) -> Union[List[AdCampaing], None]:
        query = select(AdCampaing).where(AdCampaing.user_id == user_id)
        res = await self.db_session.execute(query)
        campaing_rows = res.fetchall()
        campaings = [row[0] for row in campaing_rows]
        return campaings
    
    async def get_campaing_by_id(self, campaing_id: int) -> Union[AdCampaing, None]:
        query = select(AdCampaing).where(AdCampaing.adcampaing_id == campaing_id)
        res = await self.db_session.execute(query)
        campaing_id_row = res.fetchone()
        if campaing_id_row is not None:
            return campaing_id_row[0]

    async def update_campaing_by_id(self, user_id: int, campaing_id: int, status: bool) -> Union[bool, None]:
        query = update(AdCampaing).\
            where(and_(AdCampaing.adcampaing_id == campaing_id, AdCampaing.user_id == user_id)).\
            values(is_active = status)
        await self.db_session.execute(query)

    async def get_campaing_status(self, campaing_id: int) -> Union[bool, None]:
        query = select(AdCampaing.is_active).where(AdCampaing.adcampaing_id == campaing_id)
        res = await self.db_session.execute(query)
        campaing_row = res.fetchone()
        if campaing_row is not None:
            return campaing_row[0]

    async def update_campaing(self, campaing_id: int, user_id: int, **kwargs) -> Union[AdCampaing, None]:
        query = update(AdCampaing).\
            where(and_(AdCampaing.adcampaing_id == campaing_id, 
                        AdCampaing.user_id == user_id)).\
            values(kwargs)
        await self.db_session.execute(query)
        await self.db_session.commit()
  


class AdCampaingGameMetricDAL():
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_game_in_campaing(self, campaing_id: int, game_id: int, user_id: int, metrics: Metric):
        new_game_campaing = AdCampaingGameMetric(
            adcampaing_id = campaing_id,
            user_id = user_id,
            game_id = game_id,
            cpm = metrics.cpm,
            ctr = metrics.ctr,
            cpc = metrics.cpc,
            cr = metrics.cr,
            cpa = metrics.cpa
        )
        self.db_session.add(new_game_campaing)  
        await self.db_session.flush()
        await self.db_session.commit()

    async def delete_game_from_campaing(self, campaing_id: int, user_id: int, game_id: int) -> None:
        query = delete(AdCampaingGameMetric).\
            where(and_(AdCampaingGameMetric.adcampaing_id == campaing_id, 
                        AdCampaingGameMetric.game_id == game_id,
                            AdCampaingGameMetric.user_id == user_id
                        )
                )
        await self.db_session.execute(query) 
        await self.db_session.commit()

    async def exist_game_in_campain(self, campaing_id: int, game_id: int, user_id: int) -> Union[bool, None]:
        query = select(AdCampaingGameMetric).where(
                    exists().where(
                            and_(AdCampaingGameMetric.adcampaing_id == campaing_id,
                                AdCampaingGameMetric.game_id == game_id,
                                AdCampaingGameMetric.user_id == user_id
                        )))
        res = await self.db_session.execute(query)       
        campaing_game = res.fetchone()           
        if campaing_game is not None:
            return campaing_game[0]

    async def get_games_campaings_own(self, user_id: int):
        query = select(AdCampaingGameMetric).\
            join(User, User.user_id == AdCampaingGameMetric.user_id).\
            options(joinedload(AdCampaingGameMetric.game_metrics).joinedload(Game.developer_link)).\
            join(AdCampaing, AdCampaing.adcampaing_id == AdCampaingGameMetric.adcampaing_id).\
            options(joinedload(AdCampaingGameMetric.campaing_link)).\
            filter(AdCampaingGameMetric.user_id == user_id)
        res = await self.db_session.execute(query)
        game_metric_row = res.fetchall()
        game_metrics = [row[0] for row in game_metric_row]
        if game_metrics is not None:
            return game_metrics
        else:
            return list()

    async def update_game_id_in_campaing(self, campaing_id: int, user_id: int, **kwargs) -> None:
        query = update(AdCampaingGameMetric).\
                where(and_(AdCampaingGameMetric.adcampaing_id == campaing_id,
                            AdCampaingGameMetric.game_id == None,
                            AdCampaingGameMetric.user_id == user_id)).\
                values(kwargs)
        await self.db_session.execute(query)
        await self.db_session.commit()
 

class DeveloperDAL():
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_developers_for_games(self, game_id: List[int]):
        query = select(Developer).\
                join(DeveloperGame, DeveloperGame.developer_id == Developer.developer_id).\
                where(DeveloperGame.game_id.in_(game_id))
        res = await self.db_session.execute(query)
        developers_name = res.fetchall()
        return developers_name
                

class GameDAL():
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_games(self) -> Union[List[Game], None]:
        query = select(Game).\
                join(Developer, Developer.developer_id == Game.developer_id).\
                options(joinedload(Game.developer_link))
        res = await self.db_session.execute(query)
        games = res.fetchall()
        games = [row[0] for row in games]
        if games is not None:
            return games