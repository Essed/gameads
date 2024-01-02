from api.models import AdCampaingGameUI, AdCampaingUI, AdCampaingCreate, AdCapamaingsUI, UpdateCompaingRequest
from api.models import AdCampaing, AdCampaings, AdCampaingBase
from api.models import AppCard
from api.models import Metric
from db.dals import AdCampaingDAL
from db.dals import AdCampaingGameMetricDAL
from datetime import datetime
from typing import Union, List
from random import uniform

from db.models import AdCampaingGameMetric

async def _create_new_adcampaing(body: AdCampaingCreate, content_path: str, user_id: int, session) -> AdCampaingUI:    
    async with session.begin():
        adcampaing_dal = AdCampaingDAL(session)
        adcampaing = await adcampaing_dal.create_campaing(
            name=body.name,
            message=body.message,
            content_path=content_path,
            registred_at=datetime.utcnow(),
            budget=body.budget,
            user_id=user_id
        )
        return AdCampaingUI(
            adcampaing_id=adcampaing.adcampaing_id,
            name=adcampaing.name,
            message=adcampaing.message,
            budget=adcampaing.budget,
            user_id=adcampaing.user_id,
            content_path=adcampaing.content_path
            
        )


async def _get_campaings_user_own(user_id: int, session) -> Union[List[AdCapamaingsUI], None]:
    async with session.begin():
        adcampaing_dal = AdCampaingDAL(session)
        adcampaings = await adcampaing_dal.get_campaings_user_own(user_id=user_id)
        return AdCapamaingsUI(
            campaings=adcampaings
        )
    
async def _get_games_campaings_own(user_id: int, session) -> Union[List[AdCampaings], None]:
    async with session.begin(): 
        adcampaingmetric_dal = AdCampaingGameMetricDAL(session)
        campaingmetric = await adcampaingmetric_dal.get_games_campaings_own(user_id)
        campaing_id = [row.adcampaing_id for row in campaingmetric]
        campaing_url = [row.campaing_link.content_path for row in campaingmetric]
        campaing_descriptions = [row.campaing_link.message for row in campaingmetric]
        game_id_list = [row.game_id for row in campaingmetric]

        game_name = [row.game_metrics.name if row.game_metrics is not None else None for row in campaingmetric]
        downloads = [row.game_metrics.downloads if row.game_metrics is not None else None for row in campaingmetric]
        img_url_list = [row.game_metrics.content_path if row.game_metrics is not None else None for row in campaingmetric]
        developer_names = [row.game_metrics.developer_link.name if row.game_metrics is not None else None for row in campaingmetric]

        campaing_names = [row.campaing_link.name  for row in campaingmetric]
        status_campaings = [row.campaing_link.is_active for row in campaingmetric]
        metric_cpm = [row.cpm for row in campaingmetric]
        metric_ctr = [row.ctr for row in campaingmetric]
        metric_cpc = [row.cpc for row in campaingmetric]
        metric_cr = [row.cr for row in campaingmetric]
        metric_cpa = [row.cpa for row in campaingmetric]


        campaings: List[AdCampaing] = list()

        for i in range(0, len(campaingmetric)):
                
            if i+1 < len(campaingmetric):
                if campaing_id[i] == campaing_id[i+1]:
                    continue

            if any(campaign.id == campaing_id[i] for campaign in campaings):
                continue

            campaing = AdCampaing(
                id = campaing_id[i],
                title = campaing_names[i],
                img_url=campaing_url[i],
                description = campaing_descriptions[i],
                is_runned=status_campaings[i],
                appcard=[]            
            )

            campaings.append(campaing)

        appcards = list()
        appcards_container = dict() 

        for i in range(0, len(campaingmetric)):
            if game_id_list[i] is None:     
                continue
            apc = AppCard(
                id = game_id_list[i],
                img_url=img_url_list[i],
                title = game_name[i],
                developer=developer_names[i],
                downloads=downloads[i],
                cpc = metric_cpc[i],
                ctr = metric_ctr[i],
                cr = metric_cr[i],
                cpm = metric_cpm[i],
                cpa = metric_cpa[i]
            )
            appcards.append(apc)
            if not appcards_container.get(str(campaing_id[i])):
                appcards_container[str(campaing_id[i])] = appcards       
            else:
                appcards_container[str(campaing_id[i])].extend(appcards)


            appcards = []

        

        for adcampaing in campaings:
            adcampaing_id = str(adcampaing.id)
            if adcampaing_id in appcards_container:
                adcampaing.appcard.extend(appcards_container[adcampaing_id])

        return AdCampaings(
            campaigns=campaings
        )
    
async def _update_campaing_status_by_id(user_id: int, campaing_id: int, status: bool, session) -> Union[bool, None]:
    async with session.begin():
        adcampaing_dal = AdCampaingDAL(session)
        await adcampaing_dal.update_campaing_by_id(
            user_id = user_id, 
            campaing_id = campaing_id, 
            status = status
        )


async def _update_game_in_campaing(campaing_id: int, user_id: int, session, updated_campaing_params: dict) -> Union[int, None]:
    async with session.begin():
        adcampainggamemtric_dal = AdCampaingGameMetricDAL(session)

        request_model = UpdateCompaingRequest.parse_obj(updated_campaing_params)
        
        base_model = AdCampaingGameUI(
            game_id=request_model.game_id
        )

        base_model = base_model.model_dump(exclude_none=True)


        await adcampainggamemtric_dal.update_game_id_in_campaing(
            campaing_id=campaing_id,
            user_id=user_id,
            **base_model
        )



async def _update_campaing(user_id: int, campaing_id: int, session, updated_campaing_params: dict) -> Union[AdCampaing, None]: 
    async with session.begin():
        adcampaing_dal = AdCampaingDAL(session)
       
        
        request_model = UpdateCompaingRequest.parse_obj(updated_campaing_params)                
        base_model = AdCampaingBase(
            name=request_model.title,
            message=request_model.description,
            content_path=request_model.img_url
        )
       
        
        base_model = base_model.model_dump(exclude_none=True)

        await adcampaing_dal.update_campaing(
            campaing_id=campaing_id,
            user_id=user_id,
            **base_model
        )

        


async def _get_campaing_status_by_id(campaing_id: int, session) -> Union[bool, None]:
    adcampaing_dal = AdCampaingDAL(session)
    campaing_status = await adcampaing_dal.get_campaing_status(campaing_id)
    return campaing_status

async def _add_game_in_campaing(campaing_id: int, user_id: int, game_id: int, session) -> AdCampaingGameMetric:
    adcampaing_dal = AdCampaingGameMetricDAL(session)
    metrics_model = Metric(
        cpc = round(uniform(0.1, 10.0), 2),
        ctr = round(uniform(0.5, 5.0), 2),
        cpm = round(uniform(10.0, 100.0), 2),
        cr = round(uniform(1.0, 10.0), 2),
        cpa = round(uniform(10.0, 200.0), 2),
    )
    return await adcampaing_dal.create_game_in_campaing(campaing_id, game_id, user_id, metrics_model)
    


async def _remove_game_from_campaing(campaing_id: int, user_id: int, game_id: int, session) -> None:
    adcampainggamemetric_dal = AdCampaingGameMetricDAL(session)
    await adcampainggamemetric_dal.delete_game_from_campaing(campaing_id, user_id, game_id)

async def _exists_game_in_campaing(campain_id: int, user_id: int, game_id: int, session) -> Union[bool, None]:
    adcampainggamemetric_dal = AdCampaingGameMetricDAL(session)
    return await adcampainggamemetric_dal.exist_game_in_campain(campain_id, game_id, user_id)