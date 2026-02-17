# E-petites annonces - Application Mobile 📱

## 📋 Description
Application mobile de petites annonces développée en 100% Python avec Kivy/KivyMD.
Disponible en France et Madagascar. Base de données SQLite intégrée.

## 🎨 Thème
- **Bleu turquoise (#00CED1)** : Actions principales, titres, toolbar
- **Blanc (#FFFFFF)** : Fond principal, cards
- **Noir (#000000)** : Bouton déconnexion, texte secondaire

## ⚡ Fonctionnalités complètes

### ✅ Authentification
- Connexion / Inscription avec BDD SQLite
- Mode démo avec compte test (test/test123)
- Déconnexion
- Profil utilisateur avec statistiques

### ✅ Gestion des annonces
- Consultation des annonces récentes
- Détail complet (images, description, vendeur)
- Publication avec prise de photo (plyer.camera)
- Suppression de ses propres annonces
- Compteur de vues automatique

### ✅ Favoris
- Ajout/Retrait des favoris
- Liste des favoris persistante
- Synchronisation BDD

### ✅ Messagerie
- Conversations entre utilisateurs
- Envoi de messages en temps réel
- Historique des conversations

### ✅ Recherche avancée
- Par mots-clés
- Par catégorie
- Par ville
- Par prix (slider)

### ✅ Géolocalisation
- Carte interactive avec MapView
- Marqueurs des annonces
- GPS avec plyer.gps
- France et Madagascar

### ✅ Signalement
- Signalement d'annonces inappropriées
- Enregistrement en BDD

### ✅ Statistiques
- Vues par annonce
- Favoris reçus
- Nombre d'annonces

## 🗄️ Base de données
- SQLite embarqué
- Tables : utilisateurs, annonces, favoris, messages, signalements, catégories
- Données de test pré-remplies

## 📦 Installation

```bash
# Cloner ou extraire le projet
cd e-petites-annonces/mobile

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python run.py