from tortoise import fields, models

class LLMLifeGuide(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="life_guides")
    guide_type = fields.CharField(max_length=50)                     # 가이드 성격 ("MEDICATION", "LIFESTYLE", "EMERGENCY")
    user_current_status = fields.TextField()                         # 사용자가 직접 입력한 현재 몸 상태 (RAG의 핵심 Input)
    generated_content = fields.TextField()                           # AI가 생성한 최종 가이드 답변
    is_emergency_alert = fields.BooleanField(default=False)          # 호흡곤란 등 위험 단어 감지 시 자동 True (응급 로직)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "llm_life_guides"