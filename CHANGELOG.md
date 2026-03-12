# CHANGELOG — PokeFinder

## Correctifs UI/UX — Sections 7-15 — 13 mars 2026

### Bugs corrigés

| Ticket | Correction |
|--------|-----------|
| T79 | **Filtres boutiques** (`store_list.html`) : les 5 boutons (Toutes/Physiques/En ligne/<5km/Ouvertes) togglent `.active` et filtrent la liste en temps réel |
| T83 | **Recherche dans boutique** (`store.html`) : le champ de recherche filtre les produits (`.sp-card`) par titre en temps réel |
| T86 | **Pré-remplissage recherche** (`search_result.html`) : lecture de `?q=` dans l'URL, pré-remplit la barre de recherche et le titre h1 dynamiquement |
| T87 | **Tabs résultats** (`search_result.html`) : les onglets Tout/Produits/Boutiques togglent `.active` et filtrent les cartes résultat par type |
| T14 | **Redirect profil par rôle** (`user_index.html`, `seller_index.html`) : le bouton "Mon compte" redirige vers le bon profil selon `user_metadata.role` (seller → Seller/Profile, collector → User/Profile) |
| T107 | **Horaires vendeur** (`Seller/Profile/profile.html`) : grille redessinée — checkbox ouvert/fermé par jour, 2 créneaux (matin + après-midi), dimanche déverrouillé |
| T110/T111 | **Pages légales fusionnées** : `User/legal.html` et `Seller/legal.html` fusionnées en une seule page `legal.html` à la racine avec 5 onglets (Mentions légales, CGU, CGV Partenaires, Confidentialité, Données & RGPD). Anciens fichiers redirigent vers la nouvelle page. Tous les footer links mis à jour |

### Fichiers créés

| Fichier | Contenu |
|---------|---------|
| `legal.html` | Page légale unifiée avec 5 onglets (Mentions, CGU, CGV, Confidentialité, RGPD) |

### Fichiers modifiés

| Fichier | Modifications |
|---------|--------------|
| `User/Stores/store_list.html` | JS : filtres togglent `.active`, filtrent par type/distance/horaire |
| `User/Stores/store.html` | JS : recherche interne filtre `.sp-card` par titre |
| `User/Nav/search_result.html` | JS : lecture `?q=` URL, pré-remplissage, tabs fonctionnelles. Suppression valeur hardcodée "ETB 151" |
| `User/user_index.html` | Auth script : redirection "Mon compte" conditionnelle par rôle |
| `Seller/seller_index.html` | Auth script : redirection "Mon compte" conditionnelle par rôle |
| `Seller/Profile/profile.html` | Grille horaires : 5 colonnes (jour, checkbox, matin, séparateur, après-midi), dimanche déverrouillé, JS toggle checkbox |
| `User/legal.html` | Remplacé par redirect vers `../legal.html` |
| `Seller/legal.html` | Remplacé par redirect vers `../legal.html` |
| `index.html` | Footer link → `legal.html` |
| Tous les footers (12 fichiers) | Liens "Mentions légales" mis à jour vers `legal.html` racine |

---

## Phase 1 : Front-End Statique ✅

### 1.1 Espace Collectionneur

| Page | Fichier | Statut | Contenu clé |
|------|---------|--------|-------------|
| Auth | `User/Auth/auth.html` | ✅ | Login/register tabs, email+mdp, Google SSO, lien vers Seller auth |
| Catalogue | `User/Products/product_list.html` | ✅ | Recherche, filtres (Tous/ETB/Display/Booster/Coffret), tri, grille 6 produits |
| Détail produit | `User/Products/product.html` | ✅ | 2 colonnes, tags série/type, prix + fourchette, 3 stats, liste vendeurs |
| Liste boutiques | `User/Stores/store_list.html` | ✅ | Map placeholder + liste scroll, filtres (Physiques/En ligne/<5km/Ouvertes) |
| Détail boutique | `User/Stores/store.html` | ✅ | Cover, meta grid (adresse/horaires/tel/stock), recherche interne, grille produits |
| Profil | `User/Profile/profile.html` | ✅ | Sidebar + contenu : infos perso, comparatif Gratuit 0€ vs Premium 4.99€/mois, mdp |
| Recherche | `User/Nav/search_result.html` | ✅ | Barre pré-remplie, tabs (Tout/Produits/Boutiques), résultats mixtes + map |
| Légal | `User/legal.html` | ✅ | Mentions légales, CGU, Confidentialité (tabs) |

### 1.2 Espace Vendeur

| Page | Fichier | Statut | Contenu clé |
|------|---------|--------|-------------|
| Auth | `Seller/Auth/auth.html` | ✅ | Login/register, champs boutique (nom, email, tel, adresse) |
| Dashboard | `Seller/dashboard.html` | ✅ | 4 KPI, tableau stock avec barres, tendances + recommandations |
| Scanner | `Seller/Barcode/barcode.html` | ✅ | Viewfinder + ligne scan animée, mode Entrée/Sortie, input manuel, historique |
| Profil | `Seller/Profile/profile.html` | ✅ | Infos boutique, horaires éditables, abo Starter 19€/Pro 39€, sécurité |
| Légal | `Seller/legal.html` | ✅ | Mentions légales, CGV Partenaires, Données & RGPD (tabs) |

### Pages pré-existantes (non modifiées)
- `index.html` — Landing page
- `User/user_index.html` — Hub collectionneur
- `Seller/seller_index.html` — Hub vendeur

### Conventions respectées
- CSS variables partagées (`style.css`), styles spécifiques en `<style>` inline
- Font Awesome 6.4 + Sora (Google Fonts)
- Paths relatifs (`../../style.css` pour pages profondes, `../style.css` pour niveau 1)
- Ton naturel, pas d'"IA-speak"
- Données fictives réalistes, pas de faux indicateurs live

---

**Prochaine étape → Phase 2 : Architecture Back-End (Supabase, Firebase Auth, API Python)**

## Production Pass — 10 mars 2026 ✅

### Animations
- **Barre de recherche** (`index.html`): placeholder typewriter animé — cycle parmi 6 suggestions, pause 2,2 s, efface proprement, ne s'active pas si l'input est focus.
- **Compteurs KPI** (`index.js`): sélecteur étendu à `.kpi-val[data-target]` + `.stat-number[data-target]`; easing cubique `1 - (1-t)³` au lieu de linéaire.
- **Barres de progression** (`index.js`): animées via `data-target-width` + IntersectionObserver → width `0 → N%` en 1,1 s. Appliqué sur :
  - `Seller/seller_index.html` : progression stock  
  - `Seller/dashboard.html` : toutes les stock-bar (5 lignes)

### UI/UX
- **Section Premium** (`user_index.html`): fond plein jaune vif `#fef08a → #fde047`, texte `#111`, sous-cartes blanches, glow `rgba(234,179,8,0.28)`, CTA `#111 / #fef08a`.
- **Header index.html**: suppression du bouton "Espace Pro" redondant → un seul CTA "Connexion".
- **Hero panel** (`index.html`): remplacement du placeholder "Visuel à intégrer" par un vrai panneau de stats (boutiques, requêtes, produit tendance, alerte Premium).
- **Nav** : tous les liens "Accueil" dans les barres de nav = icône seule (fa-house ou fa-store pour le hub vendeur).
- **"Accueil Vendeur"** → icône `fa-store` seule dans `Seller/Barcode/barcode.html`, `Seller/legal.html`, `Seller/dashboard.html`.
- **search_result.html**: suppression du bouton maison redondant dans header-actions.

### Nettoyage production
- Suppression de tout texte développeur : "Cette page pose un point d'entree clair…", "Le brief vendeur parle de…", "Le futur parcours ici…", "Session ideale", "Liens utiles", "Espace utilisateur du .", "Espace vendeur du .".
- Remplacement par du contenu réel et concis.
- Suppression de `loading="lazy"` sur tous les logos dans les headers (13 fichiers) — logos toujours visibles, ne doivent pas être chargés en lazy.
- Footer uniformisé sur tous les fichiers : **Accueil** + **Mentions légales** uniquement. Suppression des doublons CGU/CGV dans le footer-bottom de `index.html`.
- Section "Commencez maintenant" remplace "Liens utiles" dans `user_index.html`.
- Section "Accès rapide" remplace "Liens utiles" dans `seller_index.html`.
- "Comment ça marche ?" remplace "Session ideale" dans `user_index.html`.

---

## Phase 2 : Back-End & Authentification — 10 mars 2026 ✅

### Fichiers créés

| Fichier | Rôle |
|---------|------|
| `supabase/schema.sql` | Schéma PostgreSQL complet (tables, RLS, triggers, view) |
| `supabase/seed.sql` | 15 produits Pokémon + 3 boutiques + search events |
| `src/config.js` | Client Supabase JS (à remplir avec tes clés) |
| `src/auth.js` | Helpers auth : signIn, signUp, signOut, requireAuth, onAuthStateChange |
| `backend/requirements.txt` | Dépendances Python |
| `backend/.env.example` | Template des variables d'environnement |
| `backend/database.py` | Client Supabase admin (service role) |
| `backend/models.py` | Modèles Pydantic (Product, Store, Stock, etc.) |
| `backend/main.py` | App FastAPI + CORS + routeurs |
| `backend/routers/products.py` | `GET /products`, `/products/trending`, `/products/{id}`, `/products/barcode/{code}` |
| `backend/routers/search.py` | `GET /search?q=` — recherche produits + boutiques + log trending |
| `backend/routers/stocks.py` | `GET/POST /{store_id}`, `POST /{store_id}/scan` (authentifié) |
| `backend/routers/dashboard.py` | `GET /dashboard` — KPIs vendeur (authentifié) |
| `backend/routers/alerts.py` | `GET/POST/DELETE /alerts` — alertes premium (authentifié) |

### Fichiers modifiés

| Fichier | Modification |
|---------|--------------|
| `User/Auth/auth.html` | Supabase CDN + handlers login/register/Google OAuth |
| `Seller/Auth/auth.html` | Supabase CDN + handlers login/register vendeur + création boutique |
| `User/user_index.html` | Auth state : affiche nom + "Mon compte / Déconnexion" si connecté |
| `Seller/seller_index.html` | Auth state : affiche nom + "Mon compte / Déconnexion" si connecté |

---

## ⚙️ Guide de mise en place — Étapes EXTERNES à faire toi-même

### Étape 1 — Créer le projet Supabase

1. Va sur **[supabase.com](https://supabase.com)** → **Start your project** → connecte-toi ou crée un compte
2. Clique **New Project**
   - **Organization** : la tienne (ou crée-en une)
   - **Name** : `pokefinder`
   - **Database Password** : génère-en un fort et **sauvegarde-le** (tu en auras besoin si tu accèdes à la DB directement)
   - **Region** : `West EU (Ireland)` — le plus proche de la France
3. Attends ~2 minutes que Supabase provisionne le projet

---

### Étape 2 — Récupérer tes clés API

1. Dans le dashboard Supabase, clique sur **Project Settings** (icône engrenage, barre gauche)
2. Onglet **API**
3. Copie les trois valeurs suivantes :

| Valeur | Où l'utiliser |
|--------|--------------|
| **Project URL** (ex: `https://abcxyz.supabase.co`) | `src/config.js` ligne `SUPABASE_URL` |
| **anon public** key (commence par `eyJ...`) | `src/config.js` ligne `SUPABASE_ANON_KEY` |
| **service_role** key (secrète — commence par `eyJ...`) | `backend/.env` ligne `SUPABASE_SERVICE_KEY` |
| **JWT Secret** (en bas de la même page) | `backend/.env` ligne `JWT_SECRET` |

4. Ouvre `src/config.js` et remplace `YOUR_SUPABASE_URL` et `YOUR_SUPABASE_ANON_KEY`

---

### Étape 3 — Initialiser la base de données

1. Dans le dashboard Supabase, clique **SQL Editor** (barre gauche, icône base de données)
2. Clique **New query**
3. Ouvre `supabase/schema.sql` depuis VS Code, copie tout le contenu, colle dans l'éditeur → clique **Run** (ou <kbd>Cmd+Enter</kbd>)
4. Attends le message `Success. No rows returned.`
5. Clique à nouveau **New query**
6. Ouvre `supabase/seed.sql`, copie tout, colle → **Run**
7. Pour vérifier : va dans **Table Editor** → tu dois voir les tables `products`, `stores`, `profiles`, etc.

---

### Étape 4 — Configurer l'authentification

1. Dans le dashboard Supabase : **Authentication** (barre gauche, icône utilisateur)
2. Onglet **Providers** → **Email**
   - Active **Enable Email Provider**
   - Pour le dev : **désactive "Confirm email"** (plus pratique pour tester sans vérifier les emails)
   - Sauvegarde
3. **(Optionnel) Google OAuth** :
   - Va sur [console.cloud.google.com](https://console.cloud.google.com)
   - Crée un projet → **APIs & Services** → **Credentials** → **Create OAuth 2.0 Client ID**
   - Type : Web application — **Authorized redirect URIs** : `https://ton-projet.supabase.co/auth/v1/callback`
   - Copie le **Client ID** et **Client Secret**
   - Dans Supabase : Authentication → Providers → Google → colle les deux valeurs → Save

---

### Étape 5 — Installer Python et le backend

Ouvre un terminal depuis VS Code (ou Terminal.app) :

```bash
# 1. Installer Python 3.11 si pas déjà fait
brew install python@3.11

# 2. Se placer dans le dossier backend
cd /Users/leandreraeth/Desktop/PokeFind/backend

# 3. Créer et activer l'environnement virtuel
python3.11 -m venv venv
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Créer le fichier .env
cp .env.example .env
```

---

### Étape 6 — Remplir le fichier `.env`

Ouvre `backend/.env` et remplace les valeurs :

```
SUPABASE_URL=https://ton-projet.supabase.co
SUPABASE_SERVICE_KEY=ta-service-role-key
SUPABASE_ANON_KEY=ta-anon-key
JWT_SECRET=ton-jwt-secret
CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
PORT=8000
```

---

### Étape 7 — Lancer le backend

```bash
# Dans backend/, avec le venv activé :
uvicorn main:app --reload --port 8000
```

- API accessible : **[http://localhost:8000](http://localhost:8000)**
- Documentation interactive : **[http://localhost:8000/docs](http://localhost:8000/docs)**
- Vérification santé : **[http://localhost:8000/health](http://localhost:8000/health)**

---

### Étape 8 — Ouvrir le front-end

Utilise **Live Server** (extension VS Code) — clique droit sur `index.html` → **Open with Live Server**. Cela donne une URL `http://127.0.0.1:5500` compatible avec les CORS configurés.

> **Sans Live Server** : l'ouverture directe en `file://` bloque les requêtes CORS du JS vers Supabase.

---

### Architecture résumée

```
Navigateur (HTML/CSS/JS vanilla)
    │
    ├── src/config.js + src/auth.js  →  Supabase JS SDK (CDN)
    │                                        │
    │                                   Supabase (Auth + DB)
    │                                   supabase.com
    │
    └── fetch(API_BASE + "/...")  →  FastAPI (localhost:8000)
                                          │
                                     Supabase (service role — bypasse RLS)
```

### Déploiement production (optionnel — plus tard)

- **Supabase** : rien à faire, c'est déjà en ligne
- **Backend Python** : déployer sur [Railway](https://railway.app) ou [Render](https://render.com)
  - Render : New Web Service → Connect repo → Build command : `pip install -r requirements.txt` → Start command : `uvicorn main:app --host 0.0.0.0 --port $PORT`
  - Ajoute les variables d'environnement dans le dashboard du service
- **Frontend** : déployer sur [Netlify](https://netlify.com) (drag & drop du dossier) ou GitHub Pages
  - Mets à jour `API_BASE` dans `src/config.js` avec l'URL de ton backend déployé

---

## Correctifs UI/UX — 12 mars 2026

### Bugs corrigés

| Ticket | Correction |
|--------|-----------|
| T04 | Recherche hero redirige maintenant vers `search_result.html?q=TERME` au lieu de `product_list.html` |
| T11/T58/T71 | **Mobile responsive** : les boutons de navigation ne disparaissent plus sur mobile — `display:none` remplacé par un nav compact scrollable horizontalement |
| T14/T34 | Boutons "Retour" utilisent `history.back()` au lieu d'URLs en dur (User Auth, Seller Auth, User Profile) |
| T29/T30 | Erreurs de login Supabase traduites en français (mapping `Invalid login credentials` → `Identifiants incorrects…`) |
| T39 | Formatage téléphone corrigé : "6 12 34 56 78" (pattern 1+2+2+2+2) au lieu de "61 23 45 67 8" |
| T40 | Drapeaux emoji remplacés par codes texte (FR, US, UK…), option "— Aucun" ajoutée |
| T63 | Section "Accès rapide" (redondante avec la nav header) remplacée par "Ressources" (Mentions légales, Support, Doc API) |
| T66 | Boutons de filtre catalogue changent d'état actif au clic + filtrent les produits affichés |
| T67 | Barre de recherche catalogue filtre les produits en temps réel par titre |

### Nouvelles fonctionnalités

| Feature | Détail |
|---------|--------|
| Toggle mot de passe (eye icon) | Ajouté sur TOUS les champs mot de passe (login + inscription, User + Seller) — icône œil/œil-barré |
| Nav mobile accessible | Tous les boutons de navigation restent visibles sur mobile, avec scroll horizontal si nécessaire |
| Navigation seller uniforme | barcode.html : ajouté lien "Profil" manquant ; profile.html : ajouté icône store ; tous les seller pages ont Dashboard + Scanner + Profil + Store |
| Profil User : flèche retour | Ajouté le bouton retour (flèche) manquant dans le header |
| Sélecteur téléphone élargi | Container agrandi de 90px → 110px, `min-width` ajouté pour éviter l'écrasement |

### Fichiers créés

| Fichier | Contenu |
|---------|---------|
| `UNCONFIGURED.md` | Documentation des fonctionnalités nécessitant une configuration externe (Google OAuth, Google Maps API, Stripe, Notifications, Confirmation email) |

### Fichiers modifiés

| Fichier | Modifications |
|---------|--------------|
| `style.css` | Media query 760px : `.nav-links` visible sur mobile (scroll horizontal), `.header-actions` adaptatif |
| `index.html` | Hero search : `<div>` → `<form>` avec `onsubmit`, bouton `<a>` → `<button type="submit">` |
| `index.js` | Ajout handler `handleHeroSearch()` — validation + redirect vers `search_result.html?q=` |
| `User/Auth/auth.html` | Retour → `history.back()`, toggle eye icon, traduction erreurs FR, CSS `.password-wrapper` + `.toggle-pwd` |
| `Seller/Auth/auth.html` | Retour → `history.back()`, toggle eye icon, traduction erreurs FR, option "Aucun", formatage corrigé, élargissement `max-width`, ajout drapeaux sur sélecteur tel |
| `User/Profile/profile.html` | Retour → `history.back()`, ajout flèche retour dans nav-links |
| `Seller/Barcode/barcode.html` | Ajout lien "Profil" dans nav-links |
| `Seller/Profile/profile.html` | Ajout icône store dans nav-links |
| `Seller/seller_index.html` | Section "Accès rapide" → "Ressources", remplacement "Mentions légales" par "FAQ" |
| `User/Products/product_list.html` | JS : filtres togglent `.active`, recherche filtre par titre en temps réel |
| `TESTS.md` | Sections 1–6 mises à jour avec validation de tous les tests UI/UX |

