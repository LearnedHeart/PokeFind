from fastapi import APIRouter, Query, HTTPException
from database import supabase_admin

router = APIRouter()


@router.get("")
def search(
    q: str = Query(..., min_length=2, description="Terme de recherche"),
    type: str = Query(None, description="Filtrer par type de produit"),
):
    """
    Unified full-text search across products and stores.
    Also logs the search event for trending purposes.
    """
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Requête trop courte (min 2 caractères)")

    term = q.strip()

    # ── Product full-text search (PostgreSQL FTS via RPC) ───────
    # We use ilike as a fallback since FTS requires a RPC function.
    COLS = "id,name,series,type,barcode,price_avg,image_url,description,language,created_at"
    products_res = (
        supabase_admin.table("products")
        .select(COLS)
        .or_(f"name.ilike.%{term}%,series.ilike.%{term}%")
        .limit(20)
        .execute()
    )

    # ── Store search ─────────────────────────────────────────────
    stores_res = (
        supabase_admin.table("stores")
        .select("id,name,city,address,phone,lat,lng,subscription")
        .eq("is_active", True)
        .or_(f"name.ilike.%{term}%,city.ilike.%{term}%,address.ilike.%{term}%")
        .limit(10)
        .execute()
    )

    # ── Log search event for trending ────────────────────────────
    if products_res.data:
        events = [{"product_id": p["id"], "query": term} for p in products_res.data[:5]]
        supabase_admin.table("search_events").insert(events).execute()

    products = products_res.data or []
    stores = stores_res.data or []

    return {
        "query": term,
        "products": products,
        "stores": stores,
        "total": len(products) + len(stores),
    }
