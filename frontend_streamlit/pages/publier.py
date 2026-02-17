"""
Page Publier - AVEC IMAGES EN LIGNE
"""
import streamlit as st
import sys
import random
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database import create_annonce

# Images en ligne par catégorie
IMAGES_EN_LIGNE = {
    'Immobilier': 'https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg',
    'Véhicules': 'https://images.pexels.com/photos/170811/pexels-photo-170811.jpeg',
    'Multimédia': 'https://images.pexels.com/photos/607812/pexels-photo-607812.jpeg',
    'Maison': 'https://images.pexels.com/photos/276583/pexels-photo-276583.jpeg',
    'Loisirs': 'https://images.pexels.com/photos/261985/pexels-photo-261985.jpeg',
    'Mode': 'https://images.pexels.com/photos/994523/pexels-photo-994523.jpeg',
    'Services': 'https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg',
    'Emplois': 'https://images.pexels.com/photos/3760067/pexels-photo-3760067.jpeg',
    'Produits locaux': 'https://images.pexels.com/photos/4110250/pexels-photo-4110250.jpeg',
    'Autres': 'https://images.pexels.com/photos/356056/pexels-photo-356056.jpeg',
}

def afficher_publier():
    """Affiche le formulaire de publication"""
    
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour publier une annonce")
        st.session_state.page = "connexion"
        return
    
    st.title("🚀 Publier une annonce")
    
    with st.form("publish_form"):
        st.markdown("### 📋 Informations")
        
        col1, col2 = st.columns(2)
        with col1:
            titre = st.text_input("Titre *", placeholder="Ex: iPhone 13 Pro")
        with col2:
            prix = st.number_input("Prix *", min_value=0.0, step=1.0, value=0.0)
        
        categorie = st.selectbox("Catégorie *", [
            "Immobilier", "Véhicules", "Multimédia", "Maison",
            "Loisirs", "Mode", "Services", "Emplois", "Produits locaux", "Autres"
        ])
        
        description = st.text_area("Description *", height=150)
        
        st.markdown("### 📍 Localisation")
        
        col_loc1, col_loc2 = st.columns(2)
        with col_loc1:
            ville = st.text_input("Ville *")
        with col_loc2:
            pays = st.selectbox("Pays *", ["France", "Madagascar"])
        
        # Image en ligne (pas d'upload)
        st.markdown("### 📸 Image")
        st.info("✅ Une image sera automatiquement ajoutée selon la catégorie")
        
        # Aperçu de l'image
        image_url = IMAGES_EN_LIGNE.get(categorie, IMAGES_EN_LIGNE['Autres'])
        st.image(image_url, width=200, caption=f"Image d'illustration - {categorie}")
        
        st.markdown("---")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit = st.form_submit_button("📤 Publier")
        with col_btn2:
            cancel = st.form_submit_button("Annuler")
        
        if submit:
            # Validation
            erreurs = []
            if not titre:
                erreurs.append("❌ Titre requis")
            if prix <= 0:
                erreurs.append("❌ Prix valide requis")
            if not description:
                erreurs.append("❌ Description requise")
            if not ville:
                erreurs.append("❌ Ville requise")
            
            if erreurs:
                for e in erreurs:
                    st.error(e)
            else:
                # Prendre l'image en ligne selon la catégorie
                image_en_ligne = IMAGES_EN_LIGNE.get(categorie, IMAGES_EN_LIGNE['Autres'])
                
                # Créer l'annonce
                annonce_id = create_annonce(
                    titre=titre,
                    description=description,
                    prix=prix,
                    categorie=categorie,
                    utilisateur_id=st.session_state.user['id'],
                    ville=ville,
                    pays=pays,
                    image_path=image_en_ligne  # ← Image en ligne !
                )
                
                if annonce_id:
                    st.success(f"✅ Annonce #{annonce_id} publiée avec succès !")
                    st.session_state.selected_annonce = annonce_id
                    st.session_state.page = "detail"
                    st.experimental_rerun()
        
        if cancel:
            st.session_state.page = "accueil"
            st.experimental_rerun()