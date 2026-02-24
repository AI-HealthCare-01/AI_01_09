from tortoise import fields, models

class PrescriptionDrug(models.Model):
    id = fields.IntField(pk=True)
    prescription = fields.ForeignKeyField("models.Prescription", related_name="drugs")
    standard_drug_name = fields.CharField(max_length=255)                # 가공된 약 이름
    dosage_amount = fields.FloatField(null=True)                         # 1회 복용량
    dosage_unit = fields.CharField(max_length=20, null=True)              # 단위 (mg, 정 등)
    daily_frequency = fields.IntField(null=True)                         # 1일 복용 횟수
    duration_days = fields.IntField(null=True)                           # 복용 일수
    is_linked_to_meds = fields.BooleanField(default=False)               # 복용 관리 연동 여부

    class Meta:
        table = "prescription_drugs"