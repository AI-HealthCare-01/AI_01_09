from tortoise import fields, models

class LLMLifeGuide(models.Model):
    """
    AI가 생성한 환자 맞춤형 복약 및 생활 가이드 전문을 관리하는 모델입니다.
    생성 당시의 환자 상태와 긴급 알림 포함 여부를 기록합니다.
    """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="life_guides")
    guide_type = fields.CharField(max_length=50) # 가이드 성격 (복약주의, 생활습관 등)
    # 생성 시점의 환자 상태(기저질환+알러지+현재약물) 요약 (RAG Context)
    user_current_status = fields.TextField()
    # [대시보드 하단] AI가 생성한 맞춤 가이드 전문
    generated_content = fields.TextField()
    is_emergency_alert = fields.BooleanField(default=False) # 긴급 주의사항 포함 여부
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "llm_life_guides"
