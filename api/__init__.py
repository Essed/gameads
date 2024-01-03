from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import UserCreate, UserUI, DeleteUserResponse, UpdatedUserRequest, UpdatedUserResponse
from api.models import AdCampaingCreate, AdCampaingUI, AdCapamaingsUI
from api.models import AppCard, AdCampaings, AdCampaing
from api.models import EmptyResponse
from api.models import UpdatedCampaignRequest, UpdateCompaingRequest
from api.models import CampaingGameRequest
from api.models import AppsUI, AppUI
from api.models import UploadedFileResonse
from api.models import CampaignURL
from db.session import get_db
from fastapi import HTTPException
from typing import Union