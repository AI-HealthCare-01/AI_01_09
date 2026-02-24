from tortoise import fields, models

class Allergy(models.Model):
    id = fields.IntField(pk=True)
    allergy_name = fields.CharField(max_length=100) # 알러지 성분 (예: 페니실린)
    user = fields.ForeignKeyField("models.User", related_name="allergies")

    class Meta:
        table = "allergies"