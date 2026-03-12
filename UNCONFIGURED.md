# Fonctionnalités non configurées

Ce document liste les fonctionnalités qui nécessitent une configuration externe pour fonctionner pleinement.

---

## 1. Google OAuth (Connexion via Google)

**État** : ❌ Non configuré  
**Impact** : les boutons « Continuer avec Google » sur les pages de connexion (Dresseur + Vendeur) ne fonctionnent pas.

**Pour activer** :
1. Aller dans le [dashboard Supabase](https://supabase.com/dashboard) → Authentication → Providers → Google
2. Activer le provider Google
3. Renseigner le Client ID et Client Secret issus de la [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
4. Configurer les Redirect URIs dans Google Cloud : `https://zgnwvurkosyxvdlakwuf.supabase.co/auth/v1/callback`

---

## 2. Google Maps / Places API (Autocomplétion d'adresse)

**État** : ❌ Non configuré (clé API placeholder)  
**Impact** : l'autocomplétion d'adresse sur la page d'inscription vendeur affiche une erreur `InvalidKeyMapError`. La saisie manuelle d'adresse fonctionne comme fallback.

**Pour activer** :
1. Créer un projet dans la [Google Cloud Console](https://console.cloud.google.com/)
2. Activer l'API « Places API » et « Maps JavaScript API »
3. Générer une clé API avec restrictions (HTTP referrers)
4. Remplacer `GOOGLE_MAPS_KEY` dans `Seller/Auth/auth.html` par la vraie clé

---

## 3. Stripe / Paiement (Abonnements vendeur)

**État** : ❌ Non implémenté  
**Impact** : la page Profil Vendeur affiche les plans Starter / Premium mais le bouton de mise à niveau n'est pas relié à un système de paiement.

**Pour activer** :
1. Créer un compte [Stripe](https://stripe.com)
2. Implémenter Stripe Checkout ou Stripe Elements côté frontend
3. Ajouter un webhook côté backend pour mettre à jour le champ `subscription` dans la table `stores`

---

## 4. Notifications push / Email d'alertes

**État** : ❌ Non implémenté  
**Impact** : les alertes de stock et notifications mentionnées dans l'UI sont visuelles uniquement.

**Pour activer** :
1. Configurer un service de mailing (SendGrid, Resend, etc.) dans Supabase Edge Functions ou le backend FastAPI
2. Implémenter la logique de déclenchement (nouveau stock, baisse de prix, etc.)

---

## 5. Confirmation d'email

**État** : ⚠️ Désactivé volontairement  
**Impact** : les utilisateurs peuvent se connecter immédiatement après inscription sans vérifier leur email.

**Pour activer** :
1. Dashboard Supabase → Authentication → Settings → « Confirm email » → Activer
2. Personnaliser le template d'email si besoin

---

> **Note** : toutes les fonctionnalités front-end (UI, navigation, formulaires, validation) fonctionnent indépendamment de ces configurations. Ce document est destiné au déploiement en production.
