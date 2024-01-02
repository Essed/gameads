from api.models import AppUI, AppsUI
from db.dals import GameDAL
from typing import List


async def _get_all_games(session):
    async with session.begin():
        game_dal = GameDAL(session)
        games = await game_dal.get_games()

        apps: List[AppsUI] = list()
        for game in games:
            app = AppUI(
                id= game.game_id,
                title = game.name,
                developer=game.developer_link.name,
                description=game.description,
                type=game.type_app,
                downloads=game.downloads,
                img_url=game.content_path
            )

            apps.append(app)
        
        return AppsUI(apps = apps)
            