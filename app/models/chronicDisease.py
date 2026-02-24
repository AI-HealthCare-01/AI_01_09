from tortoise import fields, models

class ChronicDisease(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="chronic_diseases") # 특정 유저에게 속한 질환 리스트 (N:1)
    disease_name = fields.CharField(max_length=100)                  # 질환명 (예: 고혈압, 당뇨)

    class Meta:
        table = "chronic_diseases"