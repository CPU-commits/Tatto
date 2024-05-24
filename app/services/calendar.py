import json
# FastApi
from app.dependencies import exceptions
from app.dependencies import status
# Models
from app.models.calendar import Calendar, Settings, CalendarBlock
# Interfaces
from app.interfaces.block import CalendarBlock as CalendarBlockI
# Services
from app.services.profiles import profiles_service

class CalendarService():
    def get_calendar(self, id_user: str) -> Calendar:
        profile = profiles_service.get_by_id_user(id_user)

        return json.loads(Calendar.objects(profile=profile.id).first().to_json())
    
    def _exists_calendar(self, id_profile: str) -> bool:
        return Calendar.objects().first(profile=id_profile).only('_id') is not None
    
    def _get_default_calendar_values(self) -> Settings:
        return Settings(
            days_advance=7,
        )
    
    def _init_calendar(self, id_profile: str) -> Calendar:
        calendar = Calendar(
            settings=self._get_default_calendar_values(),
            profile=id_profile,
        )
        calendar.save()
        return calendar

    def add_calendar_block(self, calendar_block: CalendarBlockI, id_user: str) -> Calendar:
        profile = profiles_service.get_by_id_user(id_user)

        exists_calendar = self._exists_calendar(profile.id)
        if exists_calendar is False:
            self._init_calendar(profile.id)
        # Exists block ?
        exists_block = Calendar.objects(blocks__in=[CalendarBlock(
            **calendar_block.to_model(),
        )])
        if exists_block:
            raise exceptions.HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Ya existe este bloque',
            )

        return Calendar.objects(profile=profile.id).update_one(
            add_to_set__blocks=[CalendarBlock(**calendar_block.to_model())],
        )

calendar_service = CalendarService()
