# PokeFinder — Plan de Tests Complet

_Dernière mise à jour : 12 mars 2026_

Ce document couvre **tous les tests** — interface, formulaires, navigation, API, et intégration.
**Pré-requis** : `uvicorn main:app --reload --port 8000` + Live Server `http://127.0.0.1:5500`

---

## Légende

| Symbole | Signification |
|---------|--------------|
| ✅ | Validé |
| 🔲 | À tester |
| 🐛 | Bug corrigé, à re-tester |

---

## 1. Landing Page — `index.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T01 | Ouvrir `http://127.0.0.1:5500` | Landing page s'affiche, hero visible, pas d'erreur console | ✅ |
| T02 | Placeholder typewriter dans la barre de recherche | Le texte s'anime et cycle entre les suggestions (ETB 151, Display…) | ✅ |
| T03 | Cliquer dans la barre de recherche | L'animation s'arrête, le champ est éditable | ✅ |
| T04 | Taper un terme et cliquer Rechercher (ou Entrée) | Redirige vers `User/Nav/search_result.html?q=TERME` | ✅ |
| T05 | Recherche hero — champ vide + clic Rechercher | Pas de redirection, focus revient sur le champ | ✅ |
| T06 | Pills de suggestion (ETB 151, Display…) | Clic remplit le champ, focus dessus | ✅ |
| T07 | Compteurs KPI animés (section stats) | Les nombres s'animent de 0 → valeur cible avec easing cubique | ✅ |
| T08 | Bouton "Connexion" dans le header | Redirige vers `User/Auth/auth.html` | ✅ |
| T09 | Pill "ESPACE COLLECTIONNEUR" | Redirige vers `User/user_index.html` | ✅ |
| T10 | Pill "ESPACE VENDEUR" | Redirige vers `Seller/seller_index.html` | ✅ |
| T11 | Footer — liens Accueil + Mentions légales | Les deux liens fonctionnent | ✅ |
| T12 | Responsive mobile (< 480px) | Page lisible, pills nav visibles (scroll horizontal), pas de débordement | ✅ |
| T13 | Responsive tablette (768px) | Layout fluide, colonnes s'adaptent | ✅ |

---

## 2. Auth Collectionneur — `User/Auth/auth.html`

### 2.1 Navigation & UI

| # | Test | Attendu | État |
|---|------|---------|------|
| T14 | Tabs Connexion / Inscription | Le slider anime, le bon panneau s'affiche | ✅ |
| T15 | Bouton "Retour" | Revient à la page précédente (`history.back()`) | ✅ |
| T16 | Lien "Espace Pro ici" en bas | Redirige vers `Seller/Auth/auth.html` | ✅ |
| T17 | Ouvrir la page en étant déjà connecté | Redirect auto vers `user_index.html` | ✅ |

### 2.2 Validation des champs

| # | Test | Attendu | État |
|---|------|---------|------|
| T18 | Email login — taper "abc" puis quitter le champ | Bordure rouge + message "Adresse email invalide" | ✅ |
| T19 | Email login — taper "test@email.com" | Bordure verte, message d'erreur disparaît | ✅ |
| T20 | Pseudo inscription — laisser vide et submit | Message "Pseudo requis" en rouge | ✅ |
| T21 | Pseudo inscription — taper "A" (1 char) et quitter | Bordure rouge (min 2) | ✅ |
| T22 | Email inscription — format invalide | Bordure rouge + message | ✅ |
| T23 | Mot de passe — taper "abc" | Barre de force rouge "Très faible", bordure rouge | ✅ |
| T24 | Mot de passe — taper "Abcdefgh1" | Barre verte "Fort", bordure verte | ✅ |
| T25 | Mot de passe — taper "Abcdefgh1!xyz" | Barre verte "Excellent" | ✅ |
| T26 | Submit inscription avec tous les champs invalides | Toutes les erreurs s'affichent, pas d'appel API | ✅ |

### 2.3 Visibilité mot de passe

| # | Test | Attendu | État |
|---|------|---------|------|
| T27 | Icône œil sur le champ MDP (login) | Clic bascule texte/mot de passe, icône change (eye ↔ eye-slash) | ✅ |
| T28 | Icône œil sur le champ MDP (inscription) | Même comportement que T27 | ✅ |

### 2.4 Fonctionnel

| # | Test | Attendu | État |
|---|------|---------|------|
| T29 | Signup avec un nouvel email valide | Redirect direct vers `user_index.html` (Confirm email OFF) | ✅ |
| T30 | Login avec le compte créé | Redirect `user_index.html` + nom affiché | ✅ |
| T31 | Déconnexion depuis le hub | Retour à l'état "Connexion" (bouton visible, nom disparu) | ✅ |
| T32 | Login avec mauvais mot de passe | Message d'erreur **en français** : "Identifiants incorrects…" | ✅ |
| T33 | Login avec email inexistant | Message d'erreur en français (pas de crash) | ✅ |
| T34 | Bouton "Google" | ⚠️ Non configuré — voir `UNCONFIGURED.md` | ✅ |
| T35 | Vérif Supabase : table `profiles` | Ligne créée avec `role = collector` | ✅ |

---

## 3. Auth Vendeur — `Seller/Auth/auth.html`

### 3.1 Navigation & UI

| # | Test | Attendu | État |
|---|------|---------|------|
| T36 | Tabs Connexion / Inscription | Slider anime, bons panneaux | ✅ |
| T37 | Bouton "Retour" | Revient à la page précédente (`history.back()`) | ✅ |
| T38 | Lien "Espace dresseur ici" | Redirige vers `User/Auth/auth.html` | ✅ |

### 3.2 Validation des champs (Inscription)

| # | Test | Attendu | État |
|---|------|---------|------|
| T39 | Nom boutique — vide et submit | Erreur "Nom de boutique requis" | ✅ |
| T40 | Email — format invalide | Bordure rouge + message | ✅ |
| T41 | Téléphone — taper des lettres | Seuls les chiffres passent, lettres ignorées | ✅ |
| T42 | Téléphone — taper "0612345678" | Formaté auto en "6 12 34 56 78" (sans le 0 initial) | ✅ |
| T43 | Sélecteur pays — changer en "US +1" | Le sélecteur change, le numéro stocké sera +1XXXXXXXXX | ✅ |
| T44 | Sélecteur pays — option "— Aucun" | Disponible, aucun préfixe ajouté au numéro | ✅ |
| T45 | Adresse — taper "12 rue" | ⚠️ Google Maps non configuré — saisie manuelle OK — voir `UNCONFIGURED.md` | ✅ |
| T46 | Mot de passe — barre de force | Fonctionne identiquement au formulaire User | ✅ |
| T47 | Submit avec champs invalides | Toutes les erreurs s'affichent en même temps | ✅ |

### 3.3 Visibilité mot de passe

| # | Test | Attendu | État |
|---|------|---------|------|
| T48 | Icône œil sur le champ MDP (login) | Clic bascule texte/mot de passe, icône change | ✅ |
| T49 | Icône œil sur le champ MDP (inscription) | Même comportement | ✅ |

### 3.4 Fonctionnel

| # | Test | Attendu | État |
|---|------|---------|------|
| T50 | Signup vendeur avec tous les champs valides | Redirect vers `seller_index.html` (Confirm email OFF) | ✅ |
| T51 | Vérif Supabase : table `stores` | Boutique créée avec owner_id, name, city, postal_code, phone avec préfixe | ✅ |
| T52 | Login vendeur | Redirect `seller_index.html` + nom affiché | ✅ |
| T53 | Login collector sur l'espace vendeur | Message "Ce compte n'est pas un compte vendeur" | ✅ |
| T54 | Login avec mauvais mot de passe | Message d'erreur **en français** | ✅ |

---

## 4. Hub Collectionneur — `User/user_index.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T55 | Page non connecté | Boutons "Connexion" / "Inscription" visibles | ✅ |
| T56 | Page connecté | Nom d'utilisateur + "Mon compte" + "Déconnexion" visibles | ✅ |
| T57 | Clic "Déconnexion" | Déconnecté, page revient à l'état non connecté | ✅ |
| T58 | Clic "Catalogue" | Redirige vers `Products/product_list.html` | ✅ |
| T59 | Clic "Boutiques proches" | Redirige vers `Stores/store_list.html` | ✅ |
| T60 | Section Premium | CTA visible avec prix 4.99€/mois | ✅ |
| T61 | Section "Comment ça marche ?" | 3 étapes affichées clairement | ✅ |
| T62 | Footer liens | Accueil + Mentions légales fonctionnels | ✅ |
| T63 | Responsive mobile | Tout est lisible, nav-links visibles, pas de coupure | ✅ |

---

## 5. Hub Vendeur — `Seller/seller_index.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T64 | Page connecté (vendeur) | Nom + "Mon compte" + "Déconnexion" | ✅ |
| T65 | Clic "Dashboard" (header nav) | Redirige vers `dashboard.html` | ✅ |
| T66 | Clic "Scanner" (header nav) | Redirige vers `Barcode/barcode.html` | ✅ |
| T67 | Clic "Profil" (header nav) | Redirige vers `Profile/profile.html` | ✅ |
| T68 | Section "Ressources" | Liens vers Mentions légales fonctionnel | ✅ |
| T69 | Barres de progression stock | Animées au scroll (IntersectionObserver) | ✅ |
| T70 | Responsive mobile | Nav-links visibles, layout adaptatif | ✅ |

---

## 6. Catalogue Produits — `User/Products/product_list.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T71 | La page s'ouvre sans erreur console | Grille de produits visible | ✅ |
| T72 | Filtres type (Tous / ETB / Display / Booster / Coffret) | Clic change l'état actif (fond sombre), produits filtrés | ✅ |
| T73 | Barre de recherche catalogue | Filtre les produits en temps réel par titre | ✅ |
| T74 | Tri (Tendance / Prix ↑ / Prix ↓ / Nouveauté / Rareté) | Le sélecteur change | ✅ |
| T75 | Filtre "ETB" puis recherche "151" | Seul "ETB Pokémon 151" affiché | ✅ |
| T76 | Clic sur une carte produit | Redirige vers `product.html` | ✅ |
| T77 | Navigation header : Accueil, Boutiques, Espace Dresseur | Liens fonctionnels | ✅ |
| T78 | Responsive mobile | Nav-links visibles, grille passe de 3 → 2 → 1 colonne(s) | ✅ |

---

## 7. Détail Produit — `User/Products/product.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T72 | La page affiche un produit (données statiques pour l'instant) | Image + nom + série + type + prix visibles | ✅ |
| T73 | Tags (série, type) | Affichés en pills | ✅ |
| T74 | Stats produit (popularité, vendeurs, prix) | 3 stats visibles | 🔲 |
| T75 | Liste vendeurs ayant le produit | Cartes avec nom/adresse/prix (statiques) | ✅ |
| T76 | Bouton "Voir la boutique" | Redirige vers `store.html` | 🔲 |
| T77 | Navigation retour vers le catalogue | Lien fonctionnel | 🔲 |

---

## 8. Liste Boutiques — `User/Stores/store_list.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T78 | La page s'ouvre | Map placeholder + liste boutiques visible | ✅ |
| T79 | Filtres (Physiques / En ligne / < 5km / Ouvertes) | Les boutons toggle visuellement | ✅ |
| T80 | Clic sur une boutique | Redirige vers `store.html` | 🔲 |
| T81 | Responsive | La map et la liste s'empilent sur mobile | 🔲 |

---

## 9. Détail Boutique — `User/Stores/store.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T82 | La page affiche une boutique | Cover + meta grid (adresse, horaires, tel, stock) | 🔲 |
| T83 | Recherche interne boutique | Le champ est fonctionnel | ✅ |
| T84 | Grille produits de la boutique | Produits affichés (statiques) | 🔲 |
| T85 | Navigation retour | Lien vers `store_list.html` ou catalogue | 🔲 |

---

## 10. Résultats Recherche — `User/Nav/search_result.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T86 | La page s'ouvre avec `?q=TERME` | Barre pré-remplie avec le terme | ✅ |
| T87 | Tabs Tout / Produits / Boutiques | Switch de tabs fonctionnel | ✅ |
| T88 | Résultats mixtes (produits + boutiques) | Affichés dans le bon tab | 🔲 |
| T89 | Map placeholder | Visible dans l'onglet Boutiques | 🔲 |

---

## 11. Profil Collectionneur — `User/Profile/profile.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T90 | La page s'ouvre | Sidebar + contenu (infos perso, Premium, mdp) | 🔲 |
| T91 | Sidebar navigation | Les onglets (Profil / Abonnement / Sécurité) changent le contenu | 🔲 |
| T92 | Comparaison Gratuit 0€ vs Premium 4.99€ | Les deux cartes sont visibles, CTA Premium clair | 🔲 |
| T93 | Changer mot de passe (section Sécurité) | Formulaire présent avec ancien / nouveau / confirmation | 🔲 |
| T94 | Responsive | La sidebar passe en tabs horizontaux sur mobile | 🔲 |

---

## 12. Dashboard Vendeur — `Seller/dashboard.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T95 | La page s'ouvre | 4 KPI cards + tableau stock + tendances | 🔲 |
| T96 | KPI compteurs animés | Nombres s'animent de 0 → valeur | 🔲 |
| T97 | Tableau stock avec barres | Barres de progression animées au scroll | 🔲 |
| T98 | Section tendances et recommandations | Visible et lisible | 🔲 |
| T99 | Navigation : icône maison → seller_index | Lien fonctionnel | 🔲 |
| T100 | Responsive | Le dashboard s'empile sur mobile, pas de scroll H | 🔲 |

---

## 13. Scanner Code-Barres — `Seller/Barcode/barcode.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T101 | La page s'ouvre | Viewfinder avec ligne scan animée | 🔲 |
| T102 | Toggle Entrée / Sortie | Les deux modes switchent, label visible | 🔲 |
| T103 | Input manuel | Champ "Saisie manuelle" fonctionnel | 🔲 |
| T104 | Historique des scans | Section historique visible (vide ou statique) | 🔲 |
| T105 | Navigation retour | Icône store → `seller_index.html` | 🔲 |

---

## 14. Profil Vendeur — `Seller/Profile/profile.html`

| # | Test | Attendu | État |
|---|------|---------|------|
| T106 | La page s'ouvre | Infos boutique + horaires + abonnement | 🔲 |
| T107 | Horaires éditables | Checkbox ouvert/fermé par jour, 2 créneaux (matin + après-midi), dimanche déverrouillé | ✅ |
| T108 | Abonnement Starter 19€ / Pro 39€ | Cartes comparatives visibles | 🔲 |
| T109 | Section Sécurité (changement mdp) | Formulaire présent | 🔲 |

---

## 15. Pages Légales

| # | Test | Attendu | État |
|---|------|---------|------|
| T110 | `legal.html` (racine) — Tabs | Mentions légales / CGU / CGV / Confidentialité / RGPD switchent (page unique fusionnée) | ✅ |
| T111 | Anciens `User/legal.html` et `Seller/legal.html` | Redirigent vers `legal.html` racine | ✅ |
| T112 | Contenu légal complet | Pas de placeholders ou texte développeur | 🔲 |

---

## 16. API Backend

### 16.1 Endpoints publics

```bash
# T113 — Health check
curl http://127.0.0.1:8000/health
# Attendu : {"status":"ok","version":"2.0.0"}

# T114 — Liste produits (pas de champ fts)
curl http://127.0.0.1:8000/products
# Attendu : 15 produits, AUCUN champ "fts" dans les objets

# T115 — Limite
curl "http://127.0.0.1:8000/products?limit=1"
# Attendu : 1 seul produit

# T116 — Filtre type
curl "http://127.0.0.1:8000/products?type=etb"
# Attendu : 3 ETB uniquement

# T117 — Trending (pas de champ fts)
curl http://127.0.0.1:8000/products/trending
# Attendu : liste avec search_count, SANS champ "fts"

# T118 — Détail produit
curl http://127.0.0.1:8000/products/11111111-0001-0000-0000-000000000000
# Attendu : { "product": {...}, "stocks": [] }

# T119 — Barcode existant
curl http://127.0.0.1:8000/products/barcode/0820650854378
# Attendu : objet produit

# T120 — Barcode inexistant (T23 fix)
curl http://127.0.0.1:8000/products/barcode/0000000000000
# Attendu : 404 "Produit non trouvé pour ce code-barres" (PAS de 500)

# T121 — Recherche
curl "http://127.0.0.1:8000/search?q=Charizard"
# Attendu : 2 produits, 0 boutiques

# T122 — Recherche boutiques
curl "http://127.0.0.1:8000/search?q=Masques"
# Attendu : produits Masques de Crépuscule

# T123 — Recherche trop courte
curl "http://127.0.0.1:8000/search?q=a"
# Attendu : 400 erreur min 2 caractères
```

### 16.2 Endpoints authentifiés (JWT vendeur)

**Récupérer le JWT :**
1. Login vendeur sur `Seller/Auth/auth.html`
2. Console (F12) → coller :
```js
Object.keys(localStorage).forEach(key => { if(key.includes('-auth-token')) console.log(JSON.parse(localStorage.getItem(key)).access_token) });
```

```bash
# T124 — Dashboard sans token
curl http://127.0.0.1:8000/dashboard
# Attendu : 401 "Token manquant"

# T125 — Dashboard avec token valide (T25 fix)
curl -H "Authorization: Bearer TON_JWT" http://127.0.0.1:8000/dashboard
# Attendu : { "store": {...}, "stats": {...} } (PAS de "Token invalide")

# T126 — Dashboard avec token bidon
curl -H "Authorization: Bearer tokenbidon" http://127.0.0.1:8000/dashboard
# Attendu : 401 "Token invalide ou expiré"

# T127 — Stocks d'une boutique (STORE_ID depuis Supabase → Table stores)
curl -H "Authorization: Bearer TON_JWT" http://127.0.0.1:8000/stocks/STORE_ID
# Attendu : { "stocks": [] }

# T128 — Upsert stock
curl -X POST \
  -H "Authorization: Bearer TON_JWT" \
  -H "Content-Type: application/json" \
  -d '{"product_id":"11111111-0001-0000-0000-000000000000","quantity":5,"price":59.99}' \
  http://127.0.0.1:8000/stocks/STORE_ID
# Attendu : { "stock": { "quantity": 5, ... } }

# T129 — Vérifier le stock
curl -H "Authorization: Bearer TON_JWT" http://127.0.0.1:8000/stocks/STORE_ID
# Attendu : 1 ligne avec quantity=5

# T130 — Scanner un barcode
curl -X POST \
  -H "Authorization: Bearer TON_JWT" \
  -H "Content-Type: application/json" \
  -d '{"barcode":"0820650854545","quantity":3,"price":5.49}' \
  http://127.0.0.1:8000/stocks/STORE_ID/scan
# Attendu : { "product": {...}, "stock": {...} }

# T131 — Scanner barcode inexistant
curl -X POST \
  -H "Authorization: Bearer TON_JWT" \
  -H "Content-Type: application/json" \
  -d '{"barcode":"9999999999999","quantity":1}' \
  http://127.0.0.1:8000/stocks/STORE_ID/scan
# Attendu : 404

# T132 — Dashboard après ajout stock
curl -H "Authorization: Bearer TON_JWT" http://127.0.0.1:8000/dashboard
# Attendu : total_products ≥ 1, stock_value > 0
```

### 16.3 Alertes Premium

```sql
-- Passer un compte en premium : SQL Editor Supabase
UPDATE public.profiles SET subscription = 'premium' WHERE email = 'ton@email.com';
```

```bash
# T133 — Alertes (compte premium)
curl -H "Authorization: Bearer TON_JWT_PREMIUM" http://127.0.0.1:8000/alerts
# Attendu : { "alerts": [] }

# T134 — Créer alerte
curl -X POST \
  -H "Authorization: Bearer TON_JWT_PREMIUM" \
  -H "Content-Type: application/json" \
  -d '{"product_id":"11111111-0001-0000-0000-000000000000","radius_km":25,"city":"Paris"}' \
  http://127.0.0.1:8000/alerts
# Attendu : { "alert": { "id": "..." } }

# T135 — Alertes sans premium
curl -H "Authorization: Bearer TON_JWT_FREE" http://127.0.0.1:8000/alerts
# Attendu : 403 "réservées aux membres Premium"
```

---

## 17. Vérifications Supabase

| # | Quoi vérifier | Chemin |
|---|--------------|--------|
| T136 | Profiles créés avec bon rôle | Table Editor → profiles |
| T137 | Store créé avec owner_id correct | Table Editor → stores |
| T138 | Stocks ajoutés après T128/T130 | Table Editor → stocks |
| T139 | Events logués | Table Editor → stock_events |
| T140 | Search events logués | Table Editor → search_events |

---

## 18. Cross-Browser & Responsive

| # | Test | Attendu | État |
|---|------|---------|------|
| T141 | Chrome desktop | Toutes les pages s'affichent correctement | 🔲 |
| T142 | Safari desktop | Pas de bugs visuels, animations OK | 🔲 |
| T143 | Firefox desktop | Identique à Chrome | 🔲 |
| T144 | iPhone Safari (ou DevTools responsive 375px) | Layout mobile OK sur toutes les pages | 🔲 |
| T145 | iPhone SE (320px) | Pas de texte coupé, boutons accessibles | 🔲 |
| T146 | iPad (768px) | Layout tablette fluide | 🔲 |

---

## 19. Navigation globale (cohérence)

| # | Test | Attendu | État |
|---|------|---------|------|
| T147 | Depuis toute page User → logo = retour index.html | Tous les logos redirigent vers la landing | 🔲 |
| T148 | Header User : Catalogue / Boutiques / Mon compte | Liens fonctionnels depuis product_list, product, stores, etc. | 🔲 |
| T149 | Header Seller : Dashboard / Scanner / Profil | Liens fonctionnels depuis toutes les pages vendeur | 🔲 |
| T150 | Footer présent et cohérent sur toutes les pages | "Accueil" + "Mentions légales" partout | 🔲 |

---

## 20. Sécurité & Edge Cases

| # | Test | Attendu | État |
|---|------|---------|------|
| T151 | Accéder à `Seller/dashboard.html` sans être connecté | Comportement sécurisé (pas de données affichées / redirect) | 🔲 |
| T152 | Accéder au `/dashboard` API avec un JWT de collector | Devrait échouer (pas de boutique) | 🔲 |
| T153 | Accéder au `/stocks/STORE_ID` avec un JWT d'un autre vendeur | 403 "Accès refusé" | 🔲 |
| T154 | JWT expiré (attendre >1h) | 401 "Token invalide ou expiré" | 🔲 |
| T155 | SQL injection dans la recherche (`'; DROP TABLE--`) | Pas d'erreur, requête traitée normalement | 🔲 |
| T156 | XSS dans la recherche (`<script>alert(1)</script>`) | Le script n'est PAS exécuté, texte affiché en clair | 🔲 |

---

## Résumé

| Catégorie | Tests | Priorité |
|-----------|-------|---------|
| Landing & Navigation | T01-T12, T147-T150 | Moyenne |
| Auth User (validation) | T13-T32 | **Haute** |
| Auth Vendeur (validation) | T33-T49 | **Haute** |
| Hubs User/Seller | T50-T64 | Moyenne |
| Catalogue & Produits | T65-T77 | Moyenne |
| Boutiques | T78-T85 | Moyenne |
| Recherche | T86-T89 | Moyenne |
| Profils | T90-T109 | Basse |
| Légal | T110-T112 | Basse |
| API publique | T113-T123 | **Haute** |
| API auth (JWT) | T124-T132 | **Haute** |
| Alertes Premium | T133-T135 | Moyenne |
| Supabase vérifs | T136-T140 | Moyenne |
| Cross-browser | T141-T146 | Moyenne |
| Sécurité | T151-T156 | **Haute** |

---

## Outils de debug rapide

```bash
# Voir les logs uvicorn en temps réel
# (déjà affiché dans le terminal Python)

# Supabase Dashboard
# Logs → Database (erreurs triggers)
# Logs → API (requêtes RLS)
```

```js
// Console navigateur (F12)

// Récupérer le JWT
(async () => { const {data} = await sb.auth.getSession(); console.log(data?.session?.access_token); })()

// Voir l'utilisateur connecté
(async () => { const {data} = await sb.auth.getUser(); console.log(data?.user); })()

// Voir le profil
(async () => { const {data} = await sb.from('profiles').select('*').single(); console.log(data); })()
```
