from api.__init__ import *
from api.actions.auth import get_current_user_from_token
from api.actions.game import _get_all_games
from db.models import User

game_router = APIRouter()

@game_router.get("/", response_model=AppsUI)
async def get_apps(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> AppsUI:
    games = await _get_all_games(db)
    
    return games