# Contexte Projet & Guidelines TCG Finder (PokeFinder)

**Ces informations sont le socle de chaque instruction. Lis ce contexte avant toute modification de code.**

## 1. Identité du Projet
* **Nom Actuel** : PokeFinder / FindMyPacks / TCG Finder.
* **Concept** : Le "Waze" ou "Leboncoin" du Pokémon TCG. Permet aux collectionneurs (dresseurs) de trouver en temps réel les magasins physiques et virtuels ayant du stock sur des cartes & paquets (ETB, displays...), tout en offrant un outil aux revendeurs pour tracker et vendre leur stock rapidement.
* **Modèle** : 
  - Freemium pour les Dresseurs (Alerte gratuite, Premium = Alerte avec 1h d'avance).
  - Abonnement pour les Vendeurs Pro.
* **Cible** : Déploiement France abord > États-Unis (40% de part de marché TCG) > Japon.

## 2. Guidelines UI / UX & Ton
* **Ton de l'interface et de la rédaction** : On bannit le "Ton IA" et les formules trop "corporate" (ex: "Découvrez notre solution innovante"). Le ton doit être direct, humain, dynamique et ancré dans l'enthousiasme du TCG. 
* **Bannir les faux semblants** : Pas de petits "points clignotants 'Live'" sur des boutons si ça n'a pas de sens immédiat (un bouton "Mode Vendeur" ne clignote pas). Pas de fausses sections de "mini stats" génériques si ça n'apporte rien à l'usage.
* **Lisibilité** : La lisibilité prime. Boutons avec des bords francs (pill, rounded), fond contrasté. Accentuer les "CTA" (Call to Action) comme "Connexion" avec des styles très visibles (`btn-outline-dark`).

## 3. Tech Stack / Architecture du Code
* **Architecture Actuelle Front** : Vanilla HTML, CSS (`style.css`), JS. Aucun framework lourd (pas de React/Vue pour le moment).
* **Styling** : Utilisation intensive des CSS Variables (ex: `--primary`, `--text`, `--surface`). Flexbox & CSS Grid pour la mise en page. Icônes via **Font Awesome 6.4**.
* **Cible Build Final** : Doit pouvoir être converti en application mobile hybride via **Capacitor**. Le HTML/CSS doit garder en tête qu'il s'affichera autant sur du Safari Mac que sur un petit iPhone.
* **Future Stack Back-end** :
  - Authentification : Firebase.
  - Base de données : Supabase.
  - API & Logic Backend : Python.

## 4. Structure des Dossiers Front-end
Les modifications doivent respecter cette arborescence (Ségrégation claire des parcours) :
* `/` (Racine) : `index.html` (Landing page unifiée pour tout le monde), `style.css`, `index.js`.
* `/User/` (Zone Dresseur) : Vues pour chercher des produits et les vendeurs disponibles.
* `/Seller/` (Zone Vendeur) : Dashboard pro, utilitaires (ex: `/Barcode/`) pour l'entrée du stock en magasin.

## 5. Règle absolue à chaque prompt
Pour toute demande de rajout de fonctionnalité ou maquette :
1. Privilégier le **minimalisme** avant de surcharger. 
2. Toujours séparer les styles CSS dans le fichier existant (ou dans une balise `<style>` propre pour du test ciblé avant refacto).
3. Respecter l'ambiance "TCG / Carte à collectionner". Ne pas faire une interface de banque. 
