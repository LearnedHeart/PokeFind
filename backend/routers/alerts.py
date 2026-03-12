from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from jose import jwt, JWTError
import os

from database import supabase_admin
from models import AlertSubscription

router = APIRouter()


def get_collector_id(authorization: Optional[str] = Header(None)) -> str:
    """Extract and validate the collector's user ID from Bearer JWT."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(
            token,
            os.environ["JWT_SECRET"],
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token invalide")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")


def require_premium(user_id: str):
    """Raise 403 if the user does not have a premium subscription."""
    res = (
        supabase_admin.table("profiles")
        .select("subscription")
        .eq("id", user_id)
        .single()
        .execute()
    )
    if not res.data or res.data.get("subscription") not in ("premium",):
        raise HTTPException(
            status_code=403,
            detail="Les alertes sont réservées aux membres Premium.",
        )


@router.get("")
def list_alerts(user_id: str = Depends(get_collector_id)):
    require_premium(user_id)
    res = (
        supabase_admin.table("alert_subscriptions")
        .select("*, product:products(id,name,series,type,image_url)")
        .eq("user_id", user_id)
        .eq("is_active", True)
        .execute()
    )
    return {"alerts": res.data}


@router.post("")
def create_alert(body: AlertSubscription, user_id: str = Depends(get_collector_id)):
    require_premium(user_id)

    # Check product exists
    prod_res = (
        supabase_admin.table("products")
        .select("id, name")
        .eq("id", str(body.product_id))
        .single()
        .execute()
    )
    if not prod_res.data:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    res = (
        supabase_admin.table("alert_subscriptions")
        .upsert(
            {
                "user_id": user_id,
                "product_id": str(body.product_id),
                "radius_km": body.radius_km,
                "city": body.city,
                "is_active": True,
            },
            on_conflict="user_id,product_id",
        )
        .execute()
    )
    return {"alert": res.data[0] if res.data else {}}


@router.delete("/{alert_id}")
def delete_alert(alert_id: str, user_id: str = Depends(get_collector_id)):
    require_premium(user_id)

    # Verify ownership
    res = (
        supabase_admin.table("alert_subscriptions")
        .select("id, user_id")
        .eq("id", alert_id)
        .single()
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=404, detail="Alerte introuvable")
    if res.data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Accès refusé")

    supabase_admin.table("alert_subscriptions").delete().eq("id", alert_id).execute()
    return {"deleted": True}
