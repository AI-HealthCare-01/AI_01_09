from tortoise import fields, models

class ChatMessage(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="chat_messages")
    session_id = fields.CharField(max_length=100) # 대화 세션 묶음
    role = fields.CharField(max_length=20)        # user 또는 assistant
    message = fields.TextField()
    # [RAG 핵심] 질문 시 참고한 가이드 ID를 연결하여 맥락 유지
    reference_guide = fields.ForeignKeyField("models.LLMLifeGuide", related_name="chats", null=True)
    is_deleted = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_messages"