from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ChronicDiseaseResponse(BaseModel):
    id: int
    disease_name: str
    when_to_diagnose: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ChronicDiseaseListResponse(BaseModel):
    items: list[ChronicDiseaseResponse]


class ChronicDiseaseSaveRequest(BaseModel):
    name: str
    when_to_Diagnose: str


class AllergyResponse(BaseModel):
    id: int
    allergy_name: Optional[str] = None
    symptom: Optional[str] = None
    category: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AllergyListResponse(BaseModel):
    items: list[AllergyResponse]


class AllergySaveRequest(BaseModel):
    category: str                      # 필수
    allergy_name: str                  # 필수
    symptom: Optional[str] = None      # 선택


class BloodPressureRecordResponse(BaseModel):
    id: int
    systolic: int
    diastolic: int
    pulse: Optional[int] = None
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BloodSugarRecordResponse(BaseModel):
    id: int
    glucose_mg_dl: float
    measure_type: str
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CurrentMedResponse(BaseModel):
    id: int
    medication_name: str
    one_dose: Optional[str] = None
    one_dose_count: Optional[str] = None
    dose_time: Optional[str] = None
    added_from: str
    start_date: str

    model_config = ConfigDict(from_attributes=True)


class CurrentMedSaveRequest(BaseModel):
    medication_name: str          # 필수
    dose_time: str                # 필수
    one_dose: Optional[str] = None
    one_dose_count: Optional[str] = None
    added_from: Optional[str] = None
    start_date: Optional[str] = None


class HealthProfileDetailResponse(BaseModel):
    id: int
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    weight_change: str
    sleep_change: str
    smoking_status: str
    drinking_status: str
    exercise_frequency: str
    diet_type: str

    model_config = ConfigDict(from_attributes=True)


class HealthProfileResponse(BaseModel):
    health_profile: Optional[HealthProfileDetailResponse] = None
    chronic_diseases: list[ChronicDiseaseResponse]
    allergies: list[AllergyResponse]
    current_meds: list[CurrentMedResponse]
    blood_pressure_records: list[BloodPressureRecordResponse]
    blood_sugar_records: list[BloodSugarRecordResponse]


class BloodSugarRequest(BaseModel):
    glucose_mg_dl: float
    measure_type: str


class BloodPressureRequest(BaseModel):
    systolic: str
    diastolic: str
    measure_type: str


class FullHealthProfileSaveRequest(BaseModel):
    # 기본 건강 정보
    family_history: str
    family_history_note: Optional[str] = None

    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    weight_change: str

    sleep_hours: Optional[float] = None
    sleep_change: str

    smoking_status: str
    smoking_years: Optional[int] = None
    smoking_per_week: Optional[float] = None

    drinking_status: str
    drinking_years: Optional[int] = None
    drinking_per_week: Optional[float] = None

    exercise_frequency: str
    diet_type: str
    
    allergies: Optional[List[AllergySaveRequest]] = Field(default_factory=list)
    chronic_diseases: Optional[List[ChronicDiseaseSaveRequest]] = Field(default_factory=list)
    medications: Optional[List[CurrentMedSaveRequest]] = Field(default_factory=list)