from tortoise import fields, models

class Prescription(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="prescriptions")
    upload = fields.OneToOneField("models.Upload", related_name="prescription") # 처방전 사진 연결
    hospital_name = fields.CharField(max_length=255, null=True)             # 병원명
    prescribed_date = fields.DateField(null=True)                           # 처방일/조제일
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "prescriptions"