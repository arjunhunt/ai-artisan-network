"""
==============================================================================
AI ARTISAN COMMERCE NETWORK - DATA MODELS & SCHEMAS
==============================================================================
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class UserRole(str, Enum):
    ARTISAN = "ARTISAN"
    BUYER = "BUYER"
    ADMIN = "ADMIN"


class VerificationStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class GIStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    FAILED = "FAILED"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    EXPIRED = "EXPIRED"


class ProductStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    VERIFIED = "VERIFIED"
    PUBLISHED = "PUBLISHED"
    SOLD_OUT = "SOLD_OUT"
    ARCHIVED = "ARCHIVED"


class EscrowState(str, Enum):
    ORDER_CREATED = "ORDER_CREATED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    PAYMENT_SECURED = "PAYMENT_SECURED"
    ARTISAN_ACCEPTED = "ARTISAN_ACCEPTED"
    CRAFTING = "CRAFTING"
    QUALITY_CHECK = "QUALITY_CHECK"
    DISPATCHED = "DISPATCHED"
    DELIVERED = "DELIVERED"
    RETURN_WINDOW = "RETURN_WINDOW"
    ESCROW_RELEASED = "ESCROW_RELEASED"
    DISPUTED = "DISPUTED"
    REFUNDED = "REFUNDED"
    CANCELLED = "CANCELLED"


# --- Request & Response Models ---

class AuthLoginRequest(BaseModel):
    role: UserRole
    identifier: str  # mobile, email, or demo username
    otp: Optional[str] = "123456"
    vishwakarma_id: Optional[str] = None


class ArtisanOnboardingRequest(BaseModel):
    name: str
    mobile: str
    email: Optional[str] = None
    state: str
    district: str
    village_city: str
    craft_category: str
    specific_craft: str
    years_experience: int
    languages: List[str] = ["Hindi"]
    vishwakarma_id: Optional[str] = None
    gi_association: Optional[str] = None
    cooperative_association: Optional[str] = None
    bank_account_masked: Optional[str] = "••••••••4821"
    ifsc_code: Optional[str] = "SBIN0001234"
    profile_photo: Optional[str] = None


class CraftAnalyzeRequest(BaseModel):
    voice_transcript: str
    artisan_name: Optional[str] = "Savita Tai"
    artisan_region: Optional[str] = "Maharashtra"
    language: Optional[str] = "mr-IN"


class ImageAnalysisRequest(BaseModel):
    image_url: str
    craft_hint: Optional[str] = None
    category_hint: Optional[str] = None


class PriceCalculateRequest(BaseModel):
    material_cost: float
    labor_hours: float
    state_name: Optional[str] = "Maharashtra"
    craft_name: Optional[str] = "Paithani Weaving"
    skill_level: Optional[str] = "Skilled"
    desired_margin_pct: Optional[float] = 20.0
    packaging_cost: Optional[float] = 100.0
    logistics_cost: Optional[float] = 150.0
    overhead_cost: Optional[float] = 100.0
    artisan_intended_price: Optional[float] = None


class GIVerifyRequest(BaseModel):
    gi_number: str
    craft: str
    region: str
    artisan_name: str
    product_category: Optional[str] = None


class ProductCreateRequest(BaseModel):
    artisan_id: Optional[int] = 1
    artisan_name: str
    title: str
    short_description: Optional[str] = ""
    description: Optional[str] = ""
    heritage_story: Optional[str] = ""
    category: str
    craft_type: str
    state_cluster: str
    materials: List[str] = []
    technique: Optional[str] = ""
    motifs: List[str] = []
    dimensions: Optional[str] = "Standard"
    weight: Optional[str] = "500g"
    care_instructions: Optional[str] = "Dry clean only"
    image_urls: List[str] = []
    material_cost: float
    labor_hours: float
    hourly_wage_rate: float
    suggested_fair_price: float
    selling_price: float
    stock_quantity: int = 1
    is_made_to_order: bool = False
    production_days: int = 3
    gi_number: Optional[str] = None
    gi_verified: bool = False
    tags: List[str] = []
    status: ProductStatus = ProductStatus.PUBLISHED


class OrderCreateRequest(BaseModel):
    product_id: int
    quantity: int = 1
    buyer_id: Optional[int] = 1
    buyer_name: str
    buyer_phone: str
    delivery_address: str
    delivery_pincode: str
    delivery_city: str
    delivery_state: str
    payment_method: str = "DEMO_UPI_ESCROW"


class OrderStateUpdateRequest(BaseModel):
    order_id: int
    new_state: EscrowState
    note: Optional[str] = None
    actor: Optional[str] = "artisan"


class ChatMessageRequest(BaseModel):
    order_id: int
    sender_role: str  # artisan / buyer
    sender_name: str
    message: str
    source_language: Optional[str] = "auto"
    target_language: Optional[str] = "en"


class ReviewCreateRequest(BaseModel):
    product_id: int
    order_id: Optional[int] = None
    buyer_name: str
    rating: int
    review_title: str
    comment: str


class AIAssistantQueryRequest(BaseModel):
    user_role: str
    query: str
    context_data: Optional[Dict[str, Any]] = None


class PincodeCheckRequest(BaseModel):
    pincode: str
