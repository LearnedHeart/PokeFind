# Feuille de Route / Roadmap (PokeFinder)

Ce document décrit les prochaines étapes concrètes pour transformer le prototype front-end actuel en l'application finale (Web + Mobile App via Capacitor).

## Phase 1 : Finalisation du Front-End Statique (UI/UX)
**Objectif :** Avoir des maquettes interactives fluides pour chaque écran du `plan.txt` avant d'y brancher la moindre base de données.

### 1.1 Espace Collectionneur (Dresseur)
- [x] **Authentification (`User/Auth/auth.html`)** : Interface de Login / Inscription (email, Google) très épurée.
- [x] **Recherche & Catalogue (`User/Products/product_list.html`)** :
  - Grille des produits avec des filtres (types, prix, séries, rareté).
  - Tri par tendance, nouveauté ou disponibilité immédiate.
- [x] **Détail Produit (`User/Products/product.html`)** :
  - Photo, informations, et statistiques temps réel (popularité).
  - Liste/Carte des vendeurs l'ayant en stock autour de l'utilisateur.
- [x] **Magasins (`User/Stores/store_list.html` & `store.html`)** :
  - Liste et page dédiée pour chaque boutique (horaires, adresse, inventaire).
- [x] **Profil Utilisateur (`User/Profile/profile.html`)** : Gestion de l'abonnement Freemium/Premium, mot de passe, préférences.

### 1.2 Espace Vendeur (Pro)
- [x] **Authentification (`Seller/Auth/auth.html`)** : Formulaire dédié avec informations magasin.
- [x] **Dashboard Principal (`Seller/dashboard.html` / `seller_index.html`)** : 
  - Vue d'ensemble des statistiques de la boutique.
  - Tendances et recommandations d'achats (fournisseurs).
- [x] **Outil de Scan Code-Barres (`Seller/Barcode/barcode.html`)** :
  - Interface simulant la caméra pour entrée/sortie rapide du stock.
- [x] **Gestion de Stock & Profil (`Seller/Profile/profile.html`)** : Édition des horaires de la boutique, gestion de l'abonnement vendeur.

---

## Phase 2 : Architecture Back-End
**Objectif :** Créer la plomberie technique pour stocker et distribuer l'information.

### 2.1 Base de Données (Supabase)
- Création du schéma de données relationnel :
  - `Users` (Rôle: Dresseur ou Vendeur, Premium: bool)
  - `Stores` (Lieu, horaires, propriétaire)
  - `Products` (Base de données globale TCG Pokémon : Nom, Série, Code-barres)
  - `Stocks` (Table de liaison Store/Product avec quantité)

### 2.2 Authentification (Firebase)
- Configuration du projet Firebase Auth.
- Implémentation du système de login différencié (User vs Seller).

### 2.3 API & Logique Métier (Python)
- Créer une API de recherche globale super rapide.
- Implémenter le calcul de "distance" (Magasins autour de moi).
- Implémenter la logique Premium : Alertes de restock envoyées avec 1h d'avance.

---

## Phase 3 : Intégration Dynamique (Front 🤝 Back)
**Objectif :** Connecter les pages HTML statiques aux données réelles.

- [ ] Connecter le login Firebase sur `auth.html`.
- [ ] Câbler la barre de recherche `hero-search` avec l'API.
- [ ] Dynamiser la page "Détail Produit" en interrogeant Supabase pour chercher le stock en temps réel.
- [ ] Mettre en place le moteur de notifications pour alerter les collectionneurs d'un restock proche.

---

## Phase 4 : Déploiement & Application Mobile
**Objectif :** Passer d'un site web à une App distribuée sur les stores.

- [ ] **Packaging Mobile** : Encapsuler HTML/CSS/JS dans **Capacitor**.
- [ ] **Fonctionnalités Nativent** : 
  - Activer la permission Caméra (Plugin natif) pour le scan de codes-barres vendeur.
  - Activer la Géolocalisation (Plugin natif) afin de l'intégrer aux filtres utilisateurs.
- [ ] **Monétisation** : Intégration Stripe (Achats In-App) pour devenir "Dresseur Premium" ou payer "l'Abonnement Vendeur".
- [ ] **Lancement** : Tests France → Planification de l'expansion US / Japon.
