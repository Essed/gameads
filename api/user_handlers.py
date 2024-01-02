from api.__init__ import *
from api.actions.user import _create_new_user
from api.actions.user import _delete_new_user
from api.actions.user import _get_user_by_id
from api.actions.user import _update_user
from db.models import User
from api.actions.auth import get_current_user_from_token

user_router = APIRouter()


@user_router.post("/", response_model=UserUI)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> UserUI:
    try:
        return await _create_new_user(body, db)
    except Exception as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    
    deleted_user_id = await _delete_new_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return DeleteUserResponse(deleted_user_id = deleted_user_id)


@user_router.get("/", response_model=UserUI)
async def get_user_by_id(
    user_id: Union[int, None] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UserUI:
    if user_id is None:
        user_id = current_user.user_id
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: int,
    body: UpdatedUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    updated_user_params = body.model_dump(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=422, detail="at least one parametr for user update info should be provided")
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    updated_user_by_id = await _update_user(updated_user_params, user_id, db)
    return UpdatedUserResponse(update_user_id=updated_user_by_id)

