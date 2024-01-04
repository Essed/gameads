from api.__init__ import *
from db.models import AdCampaingGameMetric, User
from api.actions.adcampaing import _create_new_adcampaing
from api.actions.adcampaing import _get_campaings_user_own
from api.actions.adcampaing import _get_games_campaings_own
from api.actions.adcampaing import _update_campaing_status_by_id
from api.actions.adcampaing import _update_campaing
from api.actions.adcampaing import _get_campaing_status_by_id
from api.actions.adcampaing import _add_game_in_campaing
from api.actions.adcampaing import _remove_game_from_campaing
from api.actions.adcampaing import _exists_game_in_campaing
from api.actions.adcampaing import _update_game_in_campaing
from api.actions.adcampaing import _get_campaing_by_id
from api.actions.adcampaing import _get_campaing_url
from api.actions.auth import get_current_user_from_token



campaing_router = APIRouter()

@campaing_router.post("/", response_model=AdCampaingUI)
async def create_campaign(body: AdCampaingCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> AdCampaingUI:
    try:
        created_campaign = await _create_new_adcampaing(body, body.content_path, current_user.user_id, db)
        await _add_game_in_campaing(created_campaign.adcampaing_id, current_user.user_id, None, db)
        return created_campaign
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@campaing_router.get("/", response_model=AdCapamaingsUI)
async def get_campaigns_user(user_id: Union[int, None] = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> AdCapamaingsUI:
    if user_id is None:
        user_id = current_user.user_id
    campaings = await _get_campaings_user_own(user_id, db)
    if campaings is None:
        raise HTTPException(status_code=404, detail=f"Campaigns for user with id {user_id} not found")
    return campaings


@campaing_router.get("/game_campaigns", response_model=AdCampaings)
async def get_games_campaign_user(user_id: Union[int, None] = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> AdCampaings:
    if user_id is None:
        user_id = current_user.user_id
    campaings =  await _get_games_campaings_own(user_id=current_user.user_id, session=db)
    if campaings is None:
        raise HTTPException(status_code=404, detail=f"Campaigns for user with id {user_id} not found")
    return campaings


@campaing_router.patch("/run/{id}", response_model=UpdatedCampaignRequest)
async def update_status_campaigns(id: int, body: UpdatedCampaignRequest, user_id: Union[int, None] = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    if user_id is None:
        user_id = current_user.user_id
    updated_status_param = body.model_dump(exclude_none=True)
    if updated_status_param is None:
        raise HTTPException(status_code=422, detail="at least one parametr for user update info should be provided") 
    if id is None:
        raise HTTPException(status_code=404, detail=f"Campaing with id {id} not found")
    await _update_campaing_status_by_id(user_id, id, updated_status_param.get('is_runned'), db)
    updated_campaing_by_id = await _get_campaing_status_by_id(id, db)
    return UpdatedCampaignRequest(is_runned=updated_campaing_by_id)


@campaing_router.patch("/{id}", response_model=EmptyResponse)
async def update_campaign(id: int, body: UpdateCompaingRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> EmptyResponse:
    if id is None:
        raise HTTPException(status_code=404, detail=f"Campaing with id {id} not found")
    updated_campaing_params = body.model_dump(exclude_none=True)
    if updated_campaing_params == {}:
        raise HTTPException(status_code=422, detail="at least one parametr for user update info should be provided")
    await _update_campaing(
        user_id=current_user.user_id, 
        campaing_id=id, session = db, 
        updated_campaing_params=updated_campaing_params
    )
    return EmptyResponse(status_code = "OK")


@campaing_router.patch("/udapte/{id}", response_model=EmptyResponse)
async def update_game_in_campaign(id: int, body: UpdateCompaingRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> EmptyResponse:
    if id is None:
        raise HTTPException(status_code=404, detail=f"Campaing with id {id} not found")
    updated_campaign_params = body.model_dump(exclude_none=True) 
    if updated_campaign_params == {}:
        raise HTTPException(status_code=422, detail="at least one parametr for user update info should be provided")
    await _update_game_in_campaing(id, current_user.user_id, db, updated_campaign_params)
    return EmptyResponse(status_code="OK")

@campaing_router.post("/app", response_model=EmptyResponse)
async def create_campaign_with_game(body: CampaingGameRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> AdCampaingGameMetric:
    
    exists_status = await  _exists_game_in_campaing(body.campaing_id, current_user.user_id, body.app_id, db)
    
    if exists_status is not None:
        raise HTTPException(status_code=422, detail=f"Game with id {body.app_id} added to campaing with id {body.campaing_id} yet")

    await _add_game_in_campaing(
        campaing_id=body.campaing_id,
        user_id=current_user.user_id,
        game_id=body.app_id,
        session=db
    )
    return EmptyResponse(status_code="OK")


@campaing_router.delete("/app", response_model=EmptyResponse)
async def remove_campaign_with_game(body: CampaingGameRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> AdCampaingGameMetric:
        
    await _remove_game_from_campaing(
        campaing_id=body.campaing_id,
        user_id=current_user.user_id,
        game_id=body.app_id,
        session=db
    )
    return EmptyResponse(status_code="OK")

@campaing_router.get("/{id}", response_model=AdCampaingUI)
async def get_campaign_by_id(id: int, db: AsyncSession = Depends(get_db)) -> AdCampaingUI:
    campaign = await _get_campaing_by_id(id, db)
    if campaign is None:
        raise HTTPException(status_code=422, detail=f"Campaign with {id} not found")
    return campaign


@campaing_router.get("/url/{game_id}", response_model=CampaignURL)
async def get_campaign_url(game_id: int, db: AsyncSession = Depends(get_db)) -> Union[CampaignURL, None]:
    campaing_url = await _get_campaing_url(game_id, "campaigns", db)
    if campaing_url == "":
        raise HTTPException(status_code=422, detail="Campaign for request game not found")
    return CampaignURL(url=campaing_url)