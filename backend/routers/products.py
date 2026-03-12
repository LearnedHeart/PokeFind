from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from database import supabase_admin

router = APIRouter()


@router.get("")
def list_products(
    type: Optional[str] = Query(None, description="Filtrer par type: etb, display, booster…"),
    series: Optional[str] = Query(None, description="Filtrer par série"),
    limit: int = Query(24, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    COLS = "id,name,series,type,barcode,price_avg,image_url,description,language,created_at"
    q = supabase_admin.table("products").select(COLS)
    if type:
        q = q.eq("type", type)
    if series:
        q = q.ilike("series", f"%{series}%")
    res = q.range(offset, offset + limit - 1).execute()
    return {"products": res.data, "total": len(res.data), "offset": offset, "limit": limit}


@router.get("/trending")
def trending_products(limit: int = Query(10, ge=1, le=50)):
    TRENDING_COLS = "id,name,series,type,barcode,price_avg,image_url,description,language,created_at,search_count_24h,search_count_7d,store_count"
    res = supabase_admin.table("trending_products").select(TRENDING_COLS).limit(limit).execute()
    return {"products": res.data}


@router.get("/{product_id}")
def get_product(product_id: str):
    # Product details
    COLS = "id,name,series,type,barcode,price_avg,image_url,description,language,created_at"
    res = supabase_admin.table("products").select(COLS).eq("id", product_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    # Stocks for this product across all stores
    stocks_res = (
        supabase_admin.table("stocks")
        .select("*, store:stores(id,name,city,address,phone,lat,lng,hours)")
        .eq("product_id", product_id)
        .gt("quantity", 0)
        .execute()
    )
    return {"product": res.data, "stocks": stocks_res.data}


@router.get("/barcode/{barcode}")
def get_by_barcode(barcode: str):
    COLS = "id,name,series,type,barcode,price_avg,image_url,description,language,created_at"
    res = supabase_admin.table("products").select(COLS).eq("barcode", barcode).limit(1).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Produit non trouvé pour ce code-barres")
    return res.data[0]
