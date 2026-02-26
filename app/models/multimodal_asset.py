from tortoise import fields, models


class MultimodalAsset(models.Model):
    """
    텍스트 기반 가이드를 바탕으로 생성된 시각/청각 에셋 정보를 관리하는 모델입니다.
    카드뉴스 이미지 또는 TTS 음성 파일의 URL 링크를 저장합니다.
    """

    id = fields.IntField(pk=True)
    source_table = fields.CharField(max_length=50)  # llm_life_guides 등 소스 테이블명
    source_id = fields.IntField()  # 해당 테이블의 PK
    asset_type = fields.CharField(max_length=20)  # IMAGE_NEWS(카드뉴스), VOICE_GUIDE(음성)
    asset_url = fields.CharField(max_length=512)

    class Meta:
        table = "multimodal_assets"
