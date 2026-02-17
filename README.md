# 🏠 E-petites Annonces

Plateforme de petites annonces 100% Python réalisée par **RASOAHERINIAINA Marie Fidelicia** pour le projet python UPA-2026.

## 📋 Description
- **Backend** : Django REST Framework
- **Web** : Streamlit + Folium
- **Mobile** : Kivy + Plyer (GPS/Caméra)

## 📋 Description

E-petites Annonces est une plateforme complète de petites annonces avec :
- 📢 **Publication** d'annonces avec photos
- 🔍 **Recherche** avancée (mots-clés, catégorie, ville, prix)
- 🗺️ **Carte interactive** avec Folium
- 💬 **Messagerie** avec chatbot intelligent
- ❤️ **Favoris** et ⚠️ **Signalement**
- 📊 **Statistiques** de vues
- 🌍 **Support France et Madagascar**

## 🚀 Installation rapide

```bash
git clone https://github.com/Fidelicia/E-petites-annonces.git
cd e-petites-annonces

# Backend Django
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend Streamlit (nouveau terminal)
cd frontend_streamlit
pip install -r requirements.txt
streamlit run app.py

# Mobile Kivy (nouveau terminal)
cd mobile
pip install -r requirements.txt
python run.py
