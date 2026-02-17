"""
Page Profil - CORRIGÉE SANS use_container_width
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database import get_user, update_user, get_user_annonces, get_user_favoris

def afficher_profil():
    """Affiche la page de profil"""
    
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour voir votre profil")
        st.session_state.page = "connexion"
        return
    
    st.title("👤 Mon Profil")
    
    user = get_user(st.session_state.user['id'])
    
    if not user:
        st.error("❌ Utilisateur non trouvé")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Mes informations")
        
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        ">
            <h3 style="color: #06D6A0;">{user['username']}</h3>
            <p>📧 {user['email']}</p>
            <p>📍 {user.get('ville', 'Non spécifiée')}, {user.get('pays', 'Non spécifié')}</p>
            <p>📞 {user.get('telephone', 'Non renseigné')}</p>
            <p>📅 Membre depuis {user['created_at'][:10]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Statistiques")
        
        annonces = get_user_annonces(st.session_state.user['id'])
        favoris = get_user_favoris(st.session_state.user['id'])
        
        st.metric("Annonces", len(annonces))
        st.metric("Favoris", len(favoris))
        st.metric("Vues totales", sum(a['vues'] for a in annonces))
    
    st.markdown("---")
    st.markdown("### ✏️ Modifier mon profil")
    
    with st.form("edit_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_ville = st.text_input("Ville", value=user.get('ville', ''))
            new_pays = st.selectbox("Pays", ["France", "Madagascar"], 
                                  index=0 if user.get('pays') == 'France' else 1)
        
        with col2:
            new_telephone = st.text_input("Téléphone", value=user.get('telephone', ''))
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit = st.form_submit_button("💾 Enregistrer")
        with col_btn2:
            cancel = st.form_submit_button("Annuler")
        
        if submit:
            if update_user(st.session_state.user['id'], new_ville, new_pays, new_telephone):
                st.success("✅ Profil mis à jour !")
                st.session_state.user = get_user(st.session_state.user['id'])
                st.experimental_rerun()
    
    st.markdown("---")
    
    if st.button("🚪 Se déconnecter"):
        st.session_state.user = None
        st.session_state.page = "accueil"
        st.success("✅ Déconnecté")