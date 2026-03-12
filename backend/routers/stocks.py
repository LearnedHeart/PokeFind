from fastapi import APIRouter, HTTPException, Header, Depends
from typing import Optional
import os

from database import supabase_admin
from models import StockUpsert, StockScan

router = APIRouter()


def get_seller_id(authorization: Optional[str] = Header(None)) -> str:
    """Extract and validate the seller's user ID from the Bearer JWT via Supabase Auth API."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")
    token = authorization.split(" ", 1)[1]
    try:
        user_resp = supabase_admin.auth.get_user(token)
        if not user_resp or not user_resp.user:
            raise HTTPException(status_code=401, detail="Token invalide")
        return user_resp.user.id
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")


def get_store_for_seller(store_id: str, seller_id: str) -> dict:
    """Verify the store belongs to the authenticated seller."""
    res = (
        supabase_admin.table("stores")
        .select("id, owner_id")
        .eq("id", store_id)
        .single()
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=404, detail="Boutique introuvable")
    if res.data["owner_id"] != seller_id:
        raise HTTPException(status_code=403, detail="Accès refusé")
    return res.data


@router.get("/{store_id}")
def get_store_stocks(store_id: str, seller_id: str = Depends(get_seller_id)):
    get_store_for_seller(store_id, seller_id)
    res = (
        supabase_admin.table("stocks")
        .select("*, product:products(id,name,series,type,barcode,image_url,price_avg)")
        .eq("store_id", store_id)
        .execute()
    )
    return {"stocks": res.data}


@router.post("/{store_id}")
def upsert_stock(store_id: str, body: StockUpsert, seller_id: str = Depends(get_seller_id)):
    get_store_for_seller(store_id, seller_id)

    # Upsert stock row
    upsert_res = (
        supabase_admin.table("stocks")
        .upsert(
            {
                "store_id": store_id,
                "product_id": str(body.product_id),
                "quantity": body.quantity,
                "price": body.price,
            },
            on_conflict="store_id,product_id",
        )
        .execute()
    )
    stock = upsert_res.data[0] if upsert_res.data else {}

    # Log the event
    if stock:
        supabase_admin.table("stock_events").insert({
            "stock_id": stock["id"],
            "store_id": store_id,
            "product_id": str(body.product_id),
            "action": "entry" if body.quantity > 0 else "correction",
            "delta": body.quantity,
            "quantity_after": body.quantity,
            "created_by": seller_id,
        }).execute()

    return {"stock": stock}


@router.post("/{store_id}/scan")
def scan_barcode(store_id: str, body: StockScan, seller_id: str = Depends(get_seller_id)):
    """Scan a barcode and add stock. Creates the product record if unknown."""
    get_store_for_seller(store_id, seller_id)

    # Find product by barcode
    prod_res = (
        supabase_admin.table("products")
        .select("id, name, series, type, barcode, image_url, price_avg")
        .eq("barcode", body.barcode)
        .single()
        .execute()
    )

    if not prod_res.data:
        raise HTTPException(
            status_code=404,
            detail=f"Produit avec code-barres '{body.barcode}' introuvable. Ajoutez-le d'abord dans le catalogue.",
        )

    product = prod_res.data

    # Upsert stock
    upsert_res = (
        supabase_admin.table("stocks")
        .upsert(
            {
                "store_id": store_id,
                "product_id": product["id"],
                "quantity": body.quantity,
                "price": body.price,
            },
            on_conflict="store_id,product_id",
        )
        .execute()
    )
    stock = upsert_res.data[0] if upsert_res.data else {}

    if stock:
        supabase_admin.table("stock_events").insert({
            "stock_id": stock["id"],
            "store_id": store_id,
            "product_id": product["id"],
            "action": "entry",
            "delta": body.quantity,
            "quantity_after": body.quantity,
            "created_by": seller_id,
        }).execute()

    return {"product": product, "stock": stock}
