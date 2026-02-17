"""
Page détail d'une annonce - CORRIGÉE
"""
import streamlit as st
import sys
from pathlib import Path
import folium
from streamlit_folium import folium_static

sys.path.append(str(Path(__file__).parent.parent))
from database import get_annonce_by_id, is_favori, toggle_favori

COORDS = {
    'Paris': (48.8566, 2.3522),
    'Lyon': (45.7640, 4.8357),
    'Marseille': (43.2965, 5.3698),
    'Toulouse': (43.6047, 1.4442),
    'Antananarivo': (-18.8792, 47.5079),
    'Toamasina': (-18.1443, 49.3958),
    'Fianarantsoa': (-21.4545, 47.0877),
    'Mahajanga': (-15.7167, 46.3167),
}

def afficher_carte_annonce(annonce):
    ville = annonce.get('ville', '')
    pays = annonce.get('pays', '')
    
    if ville in COORDS:
        lat, lon = COORDS[ville]
    else:
        lat, lon = (48.8566, 2.3522) if pays == 'France' else (-18.8792, 47.5079)
    
    st.markdown(f"### 🗺️ Localisation - {ville}, {pays}")
    
    m = folium.Map(location=[lat, lon], zoom_start=12, control_scale=True)
    
    popup_html = f"""
    <div style="width:200px;">
        <h4 style="color:#06D6A0;">{annonce.get('titre', '')[:30]}</h4>
        <p><strong>{annonce.get('prix', 0)} €</strong></p>
        <p>📍 {annonce.get('ville', '')}, {annonce.get('pays', '')}</p>
    </div>
    """
    
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=annonce.get('titre', '')[:20],
        icon=folium.Icon(color='red' if pays == 'Madagascar' else 'blue', icon='info-sign')
    ).add_to(m)
    
    folium_static(m, width=700, height=350)

def afficher_detail_annonce():
    if not st.session_state.selected_annonce:
        st.error("❌ Aucune annonce sélectionnée")
        st.session_state.page = "accueil"
        st.experimental_rerun()
        return
    
    annonce = get_annonce_by_id(st.session_state.selected_annonce)
    
    if not annonce:
        st.error("❌ Annonce introuvable")
        st.session_state.selected_annonce = None
        st.session_state.page = "accueil"
        st.experimental_rerun()
        return
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Retour"):
            st.session_state.selected_annonce = None
            st.session_state.page = "accueil"
            st.experimental_rerun()
    
    st.markdown("---")
    
    col_img, col_info = st.columns([1, 1])
    
    with col_img:
        st.image(annonce.get('image', 'https://images.pexels.com/photos/356056/pexels-photo-356056.jpeg'), 
                use_column_width=True)
    
    with col_info:
        st.markdown(f"<h1 style='color: #06D6A0;'>{annonce['titre']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color: #118AB2;'>{annonce['prix']} €</h2>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"**📍 Localisation :** {annonce['ville']}, {annonce['pays']}")
        st.markdown(f"**📁 Catégorie :** {annonce['categorie']}")
        st.markdown(f"**👤 Vendeur :** {annonce['vendeur']}")
        st.markdown(f"**👁️ Vues :** {annonce['vues']}")
    
    st.markdown("---")
    st.markdown("### ⚡ Actions")
    
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    
    with col_b1:
        if st.button("🔄 Actualiser", key="btn_refresh"):
            st.experimental_rerun()
    
    with col_b2:
        if st.session_state.user:
            is_fav = is_favori(st.session_state.user['id'], annonce['id'])
            if is_fav:
                if st.button("❤️ Retirer", key="btn_remove_fav"):
                    toggle_favori(st.session_state.user['id'], annonce['id'])
                    st.success("✅ Retiré des favoris")
                    st.experimental_rerun()
            else:
                if st.button("🤍 Favoris", key="btn_add_fav"):
                    toggle_favori(st.session_state.user['id'], annonce['id'])
                    st.success("✅ Ajouté aux favoris")
                    st.experimental_rerun()
        else:
            if st.button("🤍 Favoris", key="btn_fav_noauth"):
                st.warning("🔒 Connectez-vous pour ajouter aux favoris")
    
    with col_b3:
        if st.session_state.user:
            if st.button("💬 Contacter", key="btn_contact"):
                st.session_state.selected_interlocuteur = annonce['user_id']
                st.session_state.page = "messagerie"
                st.experimental_rerun()
        else:
            if st.button("💬 Contacter", key="btn_contact_noauth"):
                st.warning("🔒 Connectez-vous pour contacter")
    
    with col_b4:
        if st.session_state.user:
            if st.button("⚠️ Signaler", key="btn_report"):
                st.session_state.signal_annonce = annonce['id']
                st.session_state.page = "signalement"
                st.experimental_rerun()
        else:
            if st.button("⚠️ Signaler", key="btn_report_noauth"):
                st.warning("🔒 Connectez-vous pour signaler")
    
    st.markdown("---")
    st.markdown("### 📝 Description")
    st.write(annonce['description'])
    
    st.markdown("---")
    afficher_carte_annonce(annonce)