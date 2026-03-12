from fastapi import APIRouter, HTTPException, Depends
from routers.stocks import get_seller_id
from database import supabase_admin
from datetime import date

router = APIRouter()


@router.get("")
def get_dashboard(seller_id: str = Depends(get_seller_id)):
    """Return KPI stats for the authenticated seller's store."""

    # Find the seller's store
    store_res = (
        supabase_admin.table("stores")
        .select("id, name, subscription")
        .eq("owner_id", seller_id)
        .limit(1)
        .execute()
    )
    if not store_res.data:
        raise HTTPException(status_code=404, detail="Aucune boutique trouvée pour ce compte")

    store = store_res.data[0]
    store_id = store["id"]

    # All stocks for this store
    stocks_res = (
        supabase_admin.table("stocks")
        .select("quantity, price, product:products(name, series, type)")
        .eq("store_id", store_id)
        .execute()
    )
    stocks = stocks_res.data or []

    total_products = len(stocks)
    stock_value = sum(
        (s["quantity"] * (s["price"] or 0)) for s in stocks
    )
    low_stock_count = sum(1 for s in stocks if s["quantity"] <= 2)

    # Events today
    today = date.today().isoformat()
    events_res = (
        supabase_admin.table("stock_events")
        .select("id, action, delta, created_at, product:products(name)")
        .eq("store_id", store_id)
        .gte("created_at", f"{today}T00:00:00")
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )
    events = events_res.data or []
    entries_today = sum(1 for e in events if e["action"] == "entry")

    # Top products by quantity
    top = sorted(stocks, key=lambda s: s["quantity"], reverse=True)[:5]

    return {
        "store": store,
        "stats": {
            "total_products": total_products,
            "stock_value": round(stock_value, 2),
            "entries_today": entries_today,
            "low_stock_count": low_stock_count,
        },
        "recent_events": events[:10],
        "top_products": [
            {
                "name": s["product"]["name"] if s["product"] else "—",
                "series": s["product"]["series"] if s["product"] else "",
                "quantity": s["quantity"],
            }
            for s in top
        ],
    }
