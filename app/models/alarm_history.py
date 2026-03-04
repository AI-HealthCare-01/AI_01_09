from typing import TYPE_CHECKING

from tortoise import fields, models

if TYPE_CHECKING:
    from app.models.alarm import Alarm


class AlarmHistory(models.Model):
    """
    알람 발송 내역과 사용자의 확인 여부를 기록하는 모델입니다.
    Alarm(MED/혈압/혈당) 모두의 발송 이력을 통합 관리합니다.
    - MED 타입: is_confirmed = 복약 완료 체크 여부
    - 혈압/혈당 타입: is_confirmed = 측정 완료 체크 여부
    """

    id = fields.IntField(pk=True)
    sent_at = fields.DatetimeField(auto_now_add=True)  # 알람 발송 시각
    is_confirmed = fields.BooleanField(default=False)  # 확인(복약/측정 완료) 여부
    alarm: fields.ForeignKeyRelation["Alarm"] = fields.ForeignKeyField("models.Alarm", related_name="histories")

    class Meta:
        table = "alarm_history"
