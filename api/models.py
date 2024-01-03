from pydantic import EmailStr, field_validator, Field
from pydantic import BaseModel
from typing import Optional, List

from db.models import Base

class TunedModel(BaseModel):
    class Config:
        from_attributes = True


class UserUI(TunedModel):
    username: str
    email: EmailStr
    balance: float
    role: str
    is_active: bool


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    def validate_name(cls, value):
        if value != "":
            return value


class UpdatedUserRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = Field(None)



class UpdatedUserResponse(BaseModel):
    update_user_id: int



class DeleteUserResponse(BaseModel):
    deleted_user_id: int


class EmptyResponse(TunedModel):
    status_code: Optional[str] = Field(None, )


class AdCampaingCreate(BaseModel):
    name: str
    message: str
    budget: float
    content_path: str

    @field_validator("name")
    def validate_name(cls, value):
        if value != "":
            return value



class AdCampaingBase(TunedModel):
    name: Optional[str] = Field(None,)
    message: Optional[str] = Field(None,)
    content_path: Optional[str] = Field(None,)


class AdCampaingUI(TunedModel):
    adcampaing_id: int
    name: str
    message: str
    budget: float
    content_path: str


class AdCampaingUserUI(TunedModel):
    _id: int
    title: str
    img_url: str


class AdCapamaingsUI(TunedModel):
    campaings: List[AdCampaingUI]


class AdCampaingGameUI(TunedModel):
    game_id: int

class AppCard(TunedModel):
    id: int
    img_url: str
    title: str
    developer: str
    downloads: int
    cpc: float
    ctr: float
    cr: float
    cpm: float
    cpa: float    


class Metric(TunedModel):
    cpc: float
    ctr: float
    cr:  float
    cpm: float
    cpa: float

class AdCampaing(TunedModel):
    id: int
    title: str
    img_url: str
    description: str
    is_runned: bool
    appcard: List[AppCard]


class CampaingGameRequest(TunedModel):
    campaing_id: int
    app_id: int



class AdCampaings(TunedModel):
    campaigns: List[AdCampaing]


class UpdatedCampaignRequest(TunedModel):
    is_runned: bool


class UpdateCompaingRequest(TunedModel):
    title: Optional[str] = Field(None,)
    img_url: Optional[str] = Field(None,)
    description: Optional[str] = Field(None,)
    game_id: Optional[int] = Field(None, )

class AppUI(TunedModel):
    id: int
    title: str
    developer: str
    description: str
    type: str
    downloads: int
    img_url: str

class AppsUI(TunedModel):
    apps: List[AppUI]

class Token(BaseModel):
    access_token: str
    token_type: str


class UploadedFileResonse(TunedModel):
    img_url: str


class CampaignGameRequest(TunedModel):
    id: int

class CampaignURL(TunedModel):
    url: str