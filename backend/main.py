import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import products, search, stocks, dashboard, alerts

load_dotenv()

app = FastAPI(
    title="PokeFinder API",
    description="Backend API for PokeFinder — stock tracking & alerts for Pokémon TCG products.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS ─────────────────────────────────────────────────────
raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5500")
origins = [o.strip() for o in raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTERS ──────────────────────────────────────────────────
app.include_router(products.router,  prefix="/products",  tags=["Produits"])
app.include_router(search.router,    prefix="/search",    tags=["Recherche"])
app.include_router(stocks.router,    prefix="/stocks",    tags=["Stocks"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(alerts.router,    prefix="/alerts",    tags=["Alertes"])


@app.get("/health", tags=["Système"])
def health():
    return {"status": "ok", "version": "2.0.0"}
