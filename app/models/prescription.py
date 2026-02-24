from tortoise import fields, models

class Prescription(models.Model):
    id = fields.IntField(pk=True)
    hospital_name = fields.CharField(max_length=255, null=True) # 정제된 병원 이름
    prescribed_date = fields.DateField(null=True)              # 정제된 처방 일자
    user = fields.ForeignKeyField("models.User", related_name="prescriptions")
    # 1개의 이미지는 1개의 처방전 결과 (1:1)
    upload = fields.OneToOneField("models.Upload", related_name="prescription")

    class Meta:
        table = "prescriptions"