from tortoise import fields, models

class MultimodalAsset(models.Model):
    id = fields.IntField(pk=True)
    source_table = fields.CharField(max_length=50) # llm_life_guides 등 소스 테이블명
    source_id = fields.IntField()                  # 해당 테이블의 PK
    asset_type = fields.CharField(max_length=20)   # IMAGE_NEWS(카드뉴스), VOICE_GUIDE(음성)
    asset_url = fields.CharField(max_length=512)

    class Meta:
        table = "multimodal_assets"