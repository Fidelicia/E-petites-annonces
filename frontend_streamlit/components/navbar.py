"""
Barre de navigation moderne - CORRIGÉ
"""
import streamlit as st
from database import get_unread_count

def afficher_navbar():
    """Affiche la barre de navigation"""
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="text-align:center; margin-bottom:30px;">
            <h2 style="color:#06D6A0; margin-bottom:0;">🏠 E-petites</h2>
            <h4 style="color:#118AB2; margin-top:0;">Annonces</h4>
            <p style="font-size:12px; color:#666;">🇫🇷 France • 🇲🇬 Madagascar</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Menu navigation
        afficher_menu_navigation()
        
        st.markdown("---")
        
        # Section utilisateur
        afficher_section_utilisateur()
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style="text-align:center; font-size:12px; color:#888; padding:10px;">
            <p>🐍 100% Python</p>
            <p>📍 Géolocalisation</p>
            <p>💬 Messagerie instantanée</p>
        </div>
        """, unsafe_allow_html=True)

def afficher_menu_navigation():
    """Affiche le menu de navigation"""
    menu_items = [
        ("🏠 Accueil", "accueil"),
        ("🔍 Recherche", "recherche"),
    ]
    
    for nom, page in menu_items:
        # Utiliser un style custom pour les boutons
        if st.button(nom, key=f"nav_{page}"):
            st.session_state.current_page = page
            st.experimental_rerun()
    
    # Section connecté
    if st.session_state.user:
        menu_connecte = [
            ("📝 Mes Annonces", "mes_annonces"),
            ("❤️ Favoris", "favoris"),
            ("💬 Messagerie", "messagerie"),
            ("👤 Profil", "profil"),
        ]
        
        for nom, page in menu_connecte:
            badge = ""
            if page == "messagerie":
                try:
                    unread = get_unread_count(st.session_state.user['id'])
                    if unread > 0:
                        badge = f" ({unread}📬)"
                except:
                    pass
            
            if st.button(f"{nom}{badge}", key=f"nav_con_{page}"):
                st.session_state.current_page = page
                st.experimental_rerun()

def afficher_section_utilisateur():
    """Affiche la section utilisateur"""
    if st.session_state.user:
        st.markdown(f"**👤 {st.session_state.user.get('username', 'Utilisateur')}**")
        
        # Bouton publier
        if st.button("➕ Publier une annonce", key="btn_publish_main"):
            st.session_state.current_page = "publier"
            st.experimental_rerun()
        
        # Déconnexion
        if st.button("🚪 Déconnexion", key="btn_logout_main"):
            st.session_state.user = None
            st.success("✅ Déconnecté avec succès")
            st.experimental_rerun()
    else:
        st.markdown("**🔐 Connexion**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Se connecter", key="btn_login_main"):
                st.session_state.current_page = "connexion"
                st.experimental_rerun()
        with col2:
            if st.button("S'inscrire", key="btn_register_main"):
                st.session_state.current_page = "inscription"
                st.experimental_rerun()