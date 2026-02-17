"""
E-petites Annonces - Application Principale
VERSION FINALE - COMPATIBLE STREAMLIT ANCIENNE VERSION
"""
import streamlit as st
import sys
from pathlib import Path

# Configuration MUST BE FIRST
st.set_page_config(
    page_title="E-petites Annonces",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajouter le chemin racine
sys.path.append(str(Path(__file__).parent))

from database import init_db

# Initialiser la base de données
init_db()

# ============================================
# SESSION STATE - INITIALISATION COMPLÈTE
# ============================================
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'accueil'
if 'selected_annonce' not in st.session_state:
    st.session_state.selected_annonce = None
if 'selected_interlocuteur' not in st.session_state:
    st.session_state.selected_interlocuteur = None
if 'signal_annonce' not in st.session_state:
    st.session_state.signal_annonce = None

# ============================================
# CSS GLOBAL
# ============================================
st.markdown("""
<style>
    /* Variables */
    :root {
        --turquoise: #06D6A0;
        --bleu: #118AB2;
        --noir: #073B4C;
        --blanc: #FFFFFF;
        --gris: #F8F9FA;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #06D6A0 0%, #118AB2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Boutons */
    .stButton > button {
        border-radius: 25px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        border: none !important;
        width: 100%;
        margin: 2px 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 15px rgba(6,214,160,0.2) !important;
    }
    
    /* Formulaires */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #06D6A0 !important;
        box-shadow: 0 0 0 2px rgba(6,214,160,0.2) !important;
    }
    
    /* Cartes */
    .annonce-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #06D6A0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .annonce-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(6,214,160,0.2);
    }
    
    /* Messages */
    .message-sent {
        background: linear-gradient(135deg, #06D6A0 0%, #05b386 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 4px 20px;
        margin: 10px 0 10px auto;
        max-width: 70%;
        box-shadow: 0 2px 8px rgba(6,214,160,0.3);
    }
    
    .message-received {
        background: #F8F9FA;
        color: #333;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 4px;
        margin: 10px auto 10px 0;
        max-width: 70%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-left: 3px solid #06D6A0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR NAVIGATION - AVEC experimental_rerun
# ============================================
def sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="text-align:center; padding:20px 0;">
            <div style="
                background: linear-gradient(135deg, #06D6A0 0%, #118AB2 100%);
                width: 80px;
                height: 80px;
                border-radius: 50%;
                margin: 0 auto 15px;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <span style="font-size: 40px; color: white;">🏠</span>
            </div>
            <h2 style="color: #06D6A0; margin:0;">E-petites</h2>
            <p style="color: #118AB2;">Annonces</p>
            <p style="font-size:12px; color:#666;">🇫🇷 France • 🇲🇬 Madagascar</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # === MENU PRINCIPAL ===
        if st.button("🏠 Accueil", key="nav_accueil"):
            st.session_state.page = "accueil"
            st.experimental_rerun()
        
        if st.button("🔍 Recherche", key="nav_recherche"):
            st.session_state.page = "recherche"
            st.experimental_rerun()
        
        if st.button("🗺️ Carte", key="nav_carte"):
            st.session_state.page = "carte"
            st.experimental_rerun()
        
        st.markdown("---")
        
        # === MENU CONNECTÉ ===
        if st.session_state.user:
            st.markdown(f"**👤 {st.session_state.user['username']}**")
            
            if st.button("📝 Mes annonces", key="nav_mes_annonces"):
                st.session_state.page = "mes_annonces"
                st.experimental_rerun()
            
            if st.button("❤️ Favoris", key="nav_favoris"):
                st.session_state.page = "favoris"
                st.experimental_rerun()
            
            if st.button("💬 Messages", key="nav_messagerie"):
                st.session_state.page = "messagerie"
                st.experimental_rerun()
            
            if st.button("👤 Profil", key="nav_profil"):
                st.session_state.page = "profil"
                st.experimental_rerun()
            
            st.markdown("---")
            
            if st.button("➕ Publier", key="btn_publish"):
                st.session_state.page = "publier"
                st.experimental_rerun()
            
            if st.button("🚪 Déconnexion", key="btn_logout"):
                st.session_state.user = None
                st.session_state.page = "accueil"
                st.success("✅ Déconnecté")
                st.experimental_rerun()
        
        # === MENU NON CONNECTÉ ===
        else:
            st.markdown("### 🔐 Connexion")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔑 Se connecter", key="btn_login"):
                    st.session_state.page = "connexion"
                    st.experimental_rerun()
            with col2:
                if st.button("📝 S'inscrire", key="btn_register"):
                    st.session_state.page = "inscription"
                    st.experimental_rerun()
            
            st.markdown("---")
            st.markdown("""
            <div style="text-align:center; color:#666; font-size:12px;">
                👋 Bienvenue !<br>
                Connectez-vous pour publier<br>
                et gérer vos annonces.
            </div>
            """, unsafe_allow_html=True)

# ============================================
# PAGES
# ============================================
def page_accueil():
    from pages.accueil import afficher_accueil
    afficher_accueil()

def page_recherche():
    from pages.recherche import afficher_recherche
    afficher_recherche()

def page_carte():
    from pages.carte import afficher_carte
    afficher_carte()

def page_publier():
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour publier une annonce")
        st.session_state.page = "connexion"
        st.experimental_rerun()
    else:
        from pages.publier import afficher_publier
        afficher_publier()

def page_mes_annonces():
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour voir vos annonces")
        st.session_state.page = "connexion"
        st.experimental_rerun()
    else:
        from pages.mes_annonces import afficher_mes_annonces
        afficher_mes_annonces()

def page_favoris():
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour voir vos favoris")
        st.session_state.page = "connexion"
        st.experimental_rerun()
    else:
        from pages.favoris import afficher_favoris
        afficher_favoris()

def page_messagerie():
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour accéder à la messagerie")
        st.session_state.page = "connexion"
        st.experimental_rerun()
    else:
        from pages.messagerie import afficher_messagerie
        afficher_messagerie()

def page_profil():
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour voir votre profil")
        st.session_state.page = "connexion"
        st.experimental_rerun()
    else:
        from pages.profil import afficher_profil
        afficher_profil()

def page_connexion():
    from pages.connexion import afficher_connexion
    afficher_connexion()

def page_inscription():
    from pages.inscription import afficher_inscription
    afficher_inscription()

def page_detail():
    if st.session_state.selected_annonce:
        from pages.detail_annonce import afficher_detail_annonce
        afficher_detail_annonce()
    else:
        st.session_state.page = "accueil"
        st.experimental_rerun()

def page_signalement():
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour signaler une annonce")
        st.session_state.page = "connexion"
        st.experimental_rerun()
    else:
        from pages.signalement import afficher_signalement
        afficher_signalement()

# ============================================
# ROUTER
# ============================================
def router():
    """Affiche la page selon st.session_state.page"""
    
    # Gestion spéciale pour le détail
    if st.session_state.selected_annonce and st.session_state.page != "detail":
        st.session_state.page = "detail"
        st.experimental_rerun()
        return
    
    # Mapping des pages
    pages = {
        "accueil": page_accueil,
        "recherche": page_recherche,
        "carte": page_carte,
        "publier": page_publier,
        "mes_annonces": page_mes_annonces,
        "favoris": page_favoris,
        "messagerie": page_messagerie,
        "profil": page_profil,
        "connexion": page_connexion,
        "inscription": page_inscription,
        "detail": page_detail,
        "signalement": page_signalement,
    }
    
    # Exécuter la page
    page = st.session_state.page
    if page in pages:
        try:
            pages[page]()
        except Exception as e:
            st.error(f"❌ Erreur de chargement: {e}")
            import traceback
            st.code(traceback.format_exc())
            st.session_state.page = "accueil"
            st.experimental_rerun()
    else:
        st.session_state.page = "accueil"
        st.experimental_rerun()

# ============================================
# MAIN
# ============================================
def main():
    sidebar()
    router()

if __name__ == "__main__":
    main()