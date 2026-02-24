from tortoise import fields, models

class ChatMessage(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="chats")
    session_id = fields.CharField(max_length=100)                    # 종료 버튼 전까지 대화를 묶어주는 고유값
    role = fields.CharField(max_length=20)                           # "user" (사용자) vs "assistant" (AI)
    message = fields.TextField()                                     # 실제 대화 내용
    guide_type = fields.CharField(max_length=50, null=True)          # REQ-CHAT-003: 질문 분류 (복약/증상/일반 등)
    is_deleted = fields.BooleanField(default=False)                  # "종료" 클릭 시 True로 변경 (사용자 화면에서 숨김)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chat_messages"