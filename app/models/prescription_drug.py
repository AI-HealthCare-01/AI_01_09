from tortoise import fields, models

class PrescriptionDrug(models.Model):
    id = fields.IntField(pk=True)
    standard_drug_name = fields.CharField(max_length=255) # AI가 식별한 표준 약물명
    dosage_amount = fields.FloatField(null=True)          # 1회 투여량
    daily_frequency = fields.IntField(null=True)          # 하루 횟수
    duration_days = fields.IntField(null=True)            # 복용 일수
    # [핵심] 사용자가 복용 명단 추가 승인 시 True로 변경
    is_linked_to_meds = fields.BooleanField(default=False)
    prescription = fields.ForeignKeyField("models.Prescription", related_name="drugs")

    class Meta:
        table = "prescription_drugs"