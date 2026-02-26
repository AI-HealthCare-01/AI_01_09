from pydantic import BaseModel


class ChronicDiseaseResponse(BaseModel):
    id: int
    disease_name: str


class ChronicDiseaseListResponse(BaseModel):
    items: list[ChronicDiseaseResponse]


class ChronicDiseaseCreateRequest(BaseModel):
    disease_name: str


class AllergyResponse(BaseModel):
    id: int
    allergy_name: str


class AllergyListResponse(BaseModel):
    items: list[AllergyResponse]


class AllergyCreateRequest(BaseModel):
    allergy_name: str
