from tortoise import fields, models

class ChronicDisease(models.Model):
    id = fields.IntField(pk=True)
    disease_name = fields.CharField(max_length=100) # 질환명 (예: 고혈압, 당뇨)
    user = fields.ForeignKeyField("models.User", related_name="chronic_diseases")

    class Meta:
        table = "chronic_diseases"