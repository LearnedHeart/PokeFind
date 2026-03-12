from pydantic import BaseModel, UUID4
from typing import Optional, Any
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    collector = "collector"
    seller = "seller"


class SubscriptionPlan(str, Enum):
    free = "free"
    premium = "premium"
    starter = "starter"
    pro = "pro"


class ProductType(str, Enum):
    etb = "etb"
    display = "display"
    booster = "booster"
    coffret = "coffret"
    tripack = "tripack"
    blister = "blister"
    autre = "autre"


class StockAction(str, Enum):
    entry = "entry"
    exit = "exit"
    correction = "correction"


# ─── Response models ──────────────────────────────────────────

class Product(BaseModel):
    id: UUID4
    name: str
    series: str
    type: ProductType
    barcode: Optional[str] = None
    price_avg: Optional[float] = None
    image_url: Optional[str] = None
    language: str = "FR"
    created_at: datetime


class ProductDetail(Product):
    store_count: Optional[int] = 0
    search_count_24h: Optional[int] = 0


class Store(BaseModel):
    id: UUID4
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    phone: Optional[str] = None
    hours: Optional[Any] = None
    is_online: bool = False
    subscription: SubscriptionPlan


class StockItem(BaseModel):
    id: UUID4
    store_id: UUID4
    product_id: UUID4
    quantity: int
    price: Optional[float] = None
    updated_at: datetime
    store: Optional[Store] = None
    product: Optional[Product] = None


class StockUpsert(BaseModel):
    product_id: UUID4
    quantity: int
    price: Optional[float] = None


class StockScan(BaseModel):
    barcode: str
    quantity: int
    price: Optional[float] = None


class SearchResult(BaseModel):
    products: list[Product]
    stores: list[Store]
    total: int


class DashboardStats(BaseModel):
    total_products: int
    stock_value: float
    entries_today: int
    low_stock_count: int
    recent_events: list[dict]
    top_products: list[dict]


class AlertSubscription(BaseModel):
    product_id: UUID4
    radius_km: int = 25
    city: Optional[str] = None


class AlertSubscriptionOut(AlertSubscription):
    id: UUID4
    user_id: UUID4
    is_active: bool
    created_at: datetime
    product: Optional[Product] = None
