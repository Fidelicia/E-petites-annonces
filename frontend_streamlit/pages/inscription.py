"""
Page Inscription - CORRIGÉE SANS use_container_width
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database import create_user, get_user

def afficher_inscription():
    """Affiche le formulaire d'inscription"""
    
    st.markdown("""
    <div style="max-width:600px; margin:auto; padding:20px;">
        <h2 style="color:#06D6A0; text-align:center;">🚀 Créer un compte</h2>
        <p style="text-align:center; color:#666;">Rejoignez la communauté E-petites Annonces</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("← Retour à l'accueil"):
            st.session_state.page = "accueil"
    
    st.markdown("---")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("👤 Nom d'utilisateur *", placeholder="john_doe")
            email = st.text_input("📧 Email *", placeholder="votre@email.com")
        with col2:
            password = st.text_input("🔒 Mot de passe *", type="password", placeholder="Minimum 6 caractères")
            confirm = st.text_input("🔁 Confirmer *", type="password", placeholder="Identique")
        
        col_loc1, col_loc2 = st.columns(2)
        with col_loc1:
            ville = st.text_input("🏙️ Ville", placeholder="Ex: Paris, Antananarivo")
        with col_loc2:
            pays = st.selectbox("🌍 Pays", ["France", "Madagascar"])
        
        telephone = st.text_input("📞 Téléphone (optionnel)", placeholder="+33 6 12 34 56 78")
        
        accept = st.checkbox("J'accepte les conditions générales d'utilisation *")
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            submit = st.form_submit_button("🎉 Créer mon compte")
        
        if submit:
            erreurs = []
            if not username:
                erreurs.append("❌ Nom d'utilisateur requis")
            if not email or '@' not in email:
                erreurs.append("❌ Email valide requis")
            if len(password) < 6:
                erreurs.append("❌ Mot de passe (min 6 caractères)")
            if password != confirm:
                erreurs.append("❌ Mots de passe différents")
            if not accept:
                erreurs.append("❌ Conditions non acceptées")
            
            if erreurs:
                for e in erreurs:
                    st.error(e)
            else:
                user_id = create_user(username, email, password, ville, pays, telephone)
                if user_id:
                    st.success(f"✅ Compte créé ! Bienvenue {username}")
                    st.session_state.user = get_user(user_id)
                    st.session_state.page = "accueil"
                else:
                    st.error("❌ Email ou nom d'utilisateur déjà utilisé")
    
    st.markdown("---")
    
    st.markdown("### 🔑 Déjà inscrit ?")
    if st.button("Se connecter maintenant"):
        st.session_state.page = "connexion"