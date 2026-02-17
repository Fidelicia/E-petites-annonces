"""
Page Connexion - CORRIGÉE
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database import authenticate_user

def afficher_connexion():
    """Affiche le formulaire de connexion"""
    
    st.markdown("""
    <div style="max-width:500px; margin:auto; padding:20px;">
        <h2 style="color:#06D6A0; text-align:center;">🔑 Connexion</h2>
        <p style="text-align:center; color:#666;">Accédez à votre compte E-petites Annonces</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("← Retour à l'accueil"):
            st.session_state.page = "accueil"
    
    st.markdown("---")
    
    with st.form("login_form"):
        email = st.text_input("📧 Adresse email", placeholder="votre@email.com")
        password = st.text_input("🔒 Mot de passe", type="password", placeholder="Votre mot de passe")
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            submit = st.form_submit_button("🚀 Se connecter")
        
        if submit:
            if not email or not password:
                st.error("❌ Veuillez remplir tous les champs")
            else:
                user = authenticate_user(email, password)
                if user:
                    st.session_state.user = user
                    st.success(f"✅ Bienvenue {user['username']} !")
                    st.session_state.page = "accueil"
                else:
                    st.error("❌ Email ou mot de passe incorrect")
    
    st.markdown("---")
    
    with st.expander("🔍 Compte de démonstration"):
        st.markdown("""
        **Identifiants de test :**
        - 📧 **Email :** admin@admin.com
        - 🔒 **Mot de passe :** admin123
        """)
        
        if st.button("🔄 Utiliser le compte démo"):
            user = authenticate_user("admin@admin.com", "admin123")
            if user:
                st.session_state.user = user
                st.success(f"✅ Connecté en tant que {user['username']}")
                st.session_state.page = "accueil"  # ← PLUS DE PARENTHÈSE !
    
    st.markdown("### 👋 Pas encore de compte ?")
    if st.button("📝 Créer un compte maintenant"):
        st.session_state.page = "inscription"