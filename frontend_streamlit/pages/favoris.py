"""
Page Favoris - CORRIGÉE SANS COLONNES IMBRIQUÉES
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database import get_user_favoris, toggle_favori
from components.cards import annonce_card

def afficher_favoris():
    """Affiche la page des favoris"""
    
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour voir vos favoris")
        st.session_state.page = "connexion"
        return
    
    st.title("❤️ Mes Annonces Favorites")
    
    try:
        favoris = get_user_favoris(st.session_state.user['id'])
        
        if favoris:
            st.markdown(f"**📊 {len(favoris)} annonce(s) favorite(s)**")
            st.markdown("---")
            
            # Affichage SIMPLE - PAS DE COLONNES IMBRIQUÉES !
            for fav in favoris:
                with st.container():
                    st.image(fav.get('image', 'https://images.pexels.com/photos/356056/pexels-photo-356056.jpeg'), 
                            width=200)
                    st.markdown(f"**{fav['titre']}**")
                    st.markdown(f"**{fav['prix']} €**")
                    st.markdown(f"📍 {fav['ville']}, {fav['pays']}")
                    st.markdown(f"👤 {fav.get('vendeur', 'Anonyme')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("👁️ Voir", key=f"view_fav_{fav['id']}"):
                            st.session_state.selected_annonce = fav['id']
                            st.session_state.page = "detail"
                            st.experimental_rerun()
                    with col2:
                        if st.button("❌ Retirer", key=f"remove_fav_{fav['id']}"):
                            toggle_favori(st.session_state.user['id'], fav['id'])
                            st.success("✅ Retiré des favoris")
                            st.experimental_rerun()
                    
                    st.markdown("---")
        else:
            st.info("""
            ## 🤍 Aucun favori pour le moment
            
            Parcourez les annonces et cliquez sur le cœur ❤️ pour les ajouter à vos favoris.
            """)
            
            if st.button("🔍 Parcourir les annonces"):
                st.session_state.page = "accueil"
                st.experimental_rerun()
                
    except Exception as e:
        st.error(f"Erreur: {e}")