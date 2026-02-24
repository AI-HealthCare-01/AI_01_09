from tortoise import fields, models

class MultimodalAsset(models.Model):                                 # REG-OCR-005: 카드뉴스/음성 변환 자산 (이미지/음성 변환)
    id = fields.IntField(pk=True)
    source_table = fields.CharField(max_length=50)                   # "llm_life_guides", "ocr_results" 등
    source_id = fields.IntField()
    asset_type = fields.CharField(max_length=20)                     # "IMAGE", "VOICE"
    asset_url = fields.CharField(max_length=512)

    class Meta:
        table = "multimodal_assets"