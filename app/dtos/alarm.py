from pydantic import BaseModel, Field


class AlarmResponse(BaseModel):
    id: int
    alarm_type: str
    medication_name: str
    alarm_time: str
    is_active: bool
    current_med_id: int


class AlarmCreateRequest(BaseModel):
    alarm_type: str = Field(default="MED")
    current_med_id: int | None = Field(None)
    alarm_time: str


class AlarmUpdateRequest(BaseModel):
    alarm_time: str | None = None
    is_active: bool | None = None


class AlarmToggleRequest(BaseModel):
    is_active: bool
