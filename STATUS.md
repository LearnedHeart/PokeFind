# PokeFinder — État d'implémentation

_Dernière mise à jour : 10 mars 2026_

---

## ✅ IMPLÉMENTÉ

### Front-End (Phase 1 — 100%)
| Page | Fichier | Notes |
|------|---------|-------|
| Landing | `index.html` | Hero, KPIs animés, panneau stats, footer |
| Hub Collectionneur | `User/user_index.html` | Auth state (nom + déconnexion si connecté) |
| Hub Vendeur | `Seller/seller_index.html` | Auth state (nom + déconnexion si connecté) |
| Auth Collectionneur | `User/Auth/auth.html` | Login + Signup câblés Supabase, Google OAuth bouton, redirect fixé |
| Auth Vendeur | `Seller/Auth/auth.html` | Login + Signup câblés Supabase, création boutique auto, redirect fixé |
| Catalogue | `User/Products/product_list.html` | UI statique (filtres, grille) |
| Détail produit | `User/Products/product.html` | UI statique (2 colonnes, stats, liste vendeurs) |
| Liste boutiques | `User/Stores/store_list.html` | UI statique (map placeholder, filtres) |
| Détail boutique | `User/Stores/store.html` | UI statique (horaires, stock, meta) |
| Profil Collectionneur | `User/Profile/profile.html` | UI statique (infos perso, Premium) |
| Résultats recherche | `User/Nav/search_result.html` | UI statique (tabs Tout/Produits/Boutiques) |
| Dashboard Vendeur | `Seller/dashboard.html` | UI statique (KPIs animés, barres stock) |
| Scanner Vendeur | `Seller/Barcode/barcode.html` | UI statique (viewfinder, historique) |
| Profil Vendeur | `Seller/Profile/profile.html` | UI statique (horaires, abonnement) |
| Légal Collectionneur | `User/legal.html` | Mentions légales, CGU, Confidentialité |
| Légal Vendeur | `Seller/legal.html` | Mentions légales, CGV, RGPD |

### Base de données (Supabase)
| Élément | Détail |
|---------|--------|
| Tables | `profiles`, `stores`, `products`, `stocks`, `stock_events`, `search_events`, `alert_subscriptions`, `alert_notifications` |
| View | `trending_products` (search_count_24h, search_count_7d, store_count) |
| Triggers | `on_auth_user_created` → crée `profiles` auto au signup ; `updated_at` auto sur profiles/stores/stocks |
| RLS | Activé sur toutes les tables avec policies read/write selon rôle |
| Seed | 15 produits Pokémon réels + search events trending |
| Enum types | `user_role`, `subscription_plan`, `product_type`, `stock_action` |
| FTS | Index GIN sur `products.fts` (tsvector French + unaccent) |

### Authentification
| Feature | État |
|---------|------|
| Signup Collectionneur (email/mdp) | ✅ Fonctionnel + redirect |
| Signup Vendeur (email/mdp + boutique) | ✅ Fonctionnel + création store + redirect |
| Login Collectionneur | ✅ Fonctionnel + redirect |
| Login Vendeur (avec vérif rôle) | ✅ Fonctionnel — bloque si role≠seller |
| Déconnexion | ✅ Fonctionnel |
| Auth state sur hub pages | ✅ Nom affiché + bouton déconnexion |
| Redirect si déjà connecté | ✅ (sur les pages auth) |
| Google OAuth | ⚠️ Bouton présent, nécessite config Google Cloud Console |
| Reset mot de passe | ❌ Non implémenté |

### API Backend (FastAPI)
| Endpoint | Méthode | Auth | État |
|----------|---------|------|------|
| `/health` | GET | Non | ✅ |
| `/products` | GET | Non | ✅ filtres type/series/limit/offset |
| `/products/trending` | GET | Non | ✅ |
| `/products/{id}` | GET | Non | ✅ avec stocks par boutique |
| `/products/barcode/{code}` | GET | Non | ✅ |
| `/search?q=` | GET | Non | ✅ produits + boutiques + log trending |
| `/stocks/{store_id}` | GET | JWT Vendeur | ✅ |
| `/stocks/{store_id}` | POST | JWT Vendeur | ✅ upsert + log event |
| `/stocks/{store_id}/scan` | POST | JWT Vendeur | ✅ par code-barres |
| `/dashboard` | GET | JWT Vendeur | ✅ KPIs + events + top produits |
| `/alerts` | GET | JWT Collectionneur Premium | ✅ |
| `/alerts` | POST | JWT Collectionneur Premium | ✅ |
| `/alerts/{id}` | DELETE | JWT Collectionneur Premium | ✅ |

---

## ❌ NON IMPLÉMENTÉ (priorités)

### Haute priorité — À faire en Phase 3

| Feature | Fichier(s) concerné(s) | Effort |
|---------|----------------------|--------|
| **Catalogue branché API** — charger les vrais produits depuis `/products` | `product_list.html` | Moyen |
| **Detai produit branché API** — stocks réels par boutique | `product.html` | Moyen |
| **Liste boutiques branchée API** — depuis `/stores` | `store_list.html` | Moyen |
| **Détail boutique branché API** — depuis `/stores/{id}` | `store.html` | Moyen |
| **Recherche branchée API** — résultats réels depuis `/search?q=` | `search_result.html` | Moyen |
| **Dashboard branché API** — KPIs réels depuis `/dashboard` | `dashboard.html` | Facile |
| **Scanner → POST stocks** — envoi vers `/stocks/{id}/scan` avec le JWT vendeur | `barcode.html` | Moyen |
| **Profil vendeur — Sauvegarder** — PATCH boutique dans Supabase | `Seller/Profile/profile.html` | Facile |
| **Profil collectionneur — Sauvegarder** — PATCH profil dans Supabase | `User/Profile/profile.html` | Facile |

### Moyenne priorité — Phase 3/4

| Feature | Détail | Effort |
|---------|--------|--------|
| **Alertes UI** — abonner/désabonner un produit (appel `/alerts`) | `product.html` | Moyen |
| **Géolocalisation boutiques** — `navigator.geolocation` → filtrer par distance | `store_list.html`, `search_result.html` | Élevé |
| **Carte interactive** — remplacer les map placeholders (Leaflet.js recommandé, gratuit) | `store_list.html`, `store.html`, `search_result.html` | Élevé |
| **Envoi d'alerte** — cron job ou Supabase Edge Function → push/email quand stock arrivé | Backend | Élevé |
| **Paiement — Abonnement Premium** | Stripe integration | Très élevé |
| **Reset mot de passe** — flow email Supabase | `User/Auth/auth.html`, `Seller/Auth/auth.html` | Facile |
| **Google OAuth** — config Google Cloud Console | `src/auth.js` + Supabase | Facile |
| **Upload avatar** — Supabase Storage | `User/Profile/profile.html` | Moyen |

### Basse priorité — Plus tard

| Feature | Détail |
|---------|--------|
| Notifications temps réel | Supabase Realtime subscriptions |
| Historique stock vendeur | Page dédiée / onglet dashboard |
| Export CSV stock | Dashboard vendeur |
| Page d'administration | Gestion catalogue produits global |
| App mobile | Capacitor (prévu dans CONTEXT_GUIDELINES) |
| Déploiement prod | Render (backend) + Netlify (frontend) |
| Multi-langue | FR → EN → JP |

---

## État global

```
Phase 1 — Front-End Statique     ████████████████████  100%
Phase 2 — Auth + DB + API Base   █████████████░░░░░░░   65%
Phase 3 — Wiring API → UI        ░░░░░░░░░░░░░░░░░░░░    0%
Phase 4 — Features Avancées      ░░░░░░░░░░░░░░░░░░░░    0%
```
