from tortoise import fields, models

class Allergy(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="allergies") # 알러지 정보 (N:1)
    allergy_name = fields.CharField(max_length=100)                  # 성분명 (예: 페니실린, 복숭아 등)

    class Meta:
        table = "allergies"