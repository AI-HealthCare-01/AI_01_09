from tortoise import fields, models


class PrescriptionDrug(models.Model):
    """
    처방전에 포함된 개별 약품 상세 정보를 관리하는 모델입니다.
    용량, 복용 빈도 및 기간 정보를 포함하며 특정 처방전(Prescription)에 속합니다.
    """

    id = fields.IntField(pk=True)
    standard_drug_name = fields.CharField(max_length=255)  # AI가 식별한 표준 약물명
    dosage_amount = fields.FloatField(null=True)  # 1회 투여량
    daily_frequency = fields.IntField(null=True)  # 하루 횟수
    duration_days = fields.IntField(null=True)  # 복용 일수
    # [핵심] 사용자가 복용 명단 추가 승인 시 True로 변경
    is_linked_to_meds = fields.BooleanField(default=False)
    prescription = fields.ForeignKeyField("models.Prescription", related_name="drugs")

    class Meta:
        table = "prescription_drugs"
