from pydantic import BaseModel


# ==========================================
# [추가된 기능] 선택 3: 알림 기능
# ==========================================
class AlarmCreateRequest(BaseModel):
    user_id: str
    drug_name: str
    alarm_time: str # HH:MM
    is_active: bool = True

class AlarmResponse(BaseModel):
    id: int
    drug_name: str
    alarm_time: str
    is_active: bool
