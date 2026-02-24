from tortoise import fields, models

class Allergy(models.Model):
    id = fields.IntField(pk=True)
<<<<<<< HEAD
    allergy_name = fields.CharField(max_length=100) # 알러지 성분 (예: 페니실린)
    user = fields.ForeignKeyField("models.User", related_name="allergies")
=======
    user = fields.ForeignKeyField("models.User", related_name="allergies") # 알러지 정보 (N:1)
    allergy_name = fields.CharField(max_length=100, description="성분명 (예: 페니실린, 복숭아 등)")
>>>>>>> d6e51ba2c169e21bc320f74bba97c5fa8af7826c

    class Meta:
        table = "allergies"