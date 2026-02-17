"""
Page "Mes Annonces" - Gestion complète des annonces utilisateur
"""
import streamlit as st

def afficher_mes_annonces():
    """Page principale "Mes Annonces" """
    
    # En-tête moderne
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:30px;">
        <div>
            <h1 style="color:#06D6A0; margin-bottom:5px;">📝 Mes Annonces</h1>
            <p style="color:#666;">Gérez toutes vos publications en un seul endroit</p>
        </div>
        <div style="font-size:48px;">🚀</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Vérifier l'authentification
    if not st.session_state.get("is_authenticated", False):
        st.warning("🔒 Connectez-vous pour accéder à vos annonces")
        
        if st.button("🔑 Se connecter"):
            st.session_state.show_login = True
            st.experimental_rerun()
        return
    
    # Statistiques rapides
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align:center; padding:20px; background:white; border-radius:12px; box-shadow:0 5px 15px rgba(0,0,0,0.05);">
            <div style="font-size:32px; color:#06D6A0;">📈</div>
            <h2 style="margin:10px 0;">3</h2>
            <p style="color:#666; margin:0;">Actives</p>
            <div style="color:#06D6A0; font-size:12px;">+1 cette semaine</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:20px; background:white; border-radius:12px; box-shadow:0 5px 15px rgba(0,0,0,0.05);">
            <div style="font-size:32px; color:#118AB2;">👁️</div>
            <h2 style="margin:10px 0;">1.2K</h2>
            <p style="color:#666; margin:0;">Vues totales</p>
            <div style="color:#06D6A0; font-size:12px;">+12%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align:center; padding:20px; background:white; border-radius:12px; box-shadow:0 5px 15px rgba(0,0,0,0.05);">
            <div style="font-size:32px; color:#FF6B6B;">❤️</div>
            <h2 style="margin:10px 0;">24</h2>
            <p style="color:#666; margin:0;">Favoris</p>
            <div style="color:#06D6A0; font-size:12px;">+5</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align:center; padding:20px; background:white; border-radius:12px; box-shadow:0 5px 15px rgba(0,0,0,0.05);">
            <div style="font-size:32px; color:#FFD166;">⭐</div>
            <h2 style="margin:10px 0;">4.8/5</h2>
            <p style="color:#666; margin:0;">Notes</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Bouton pour publier
    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        if st.button("➕ Publier une nouvelle annonce", 
                   use_container_width=True):
            st.session_state.show_publish = True
            st.experimental_rerun()
    
    with col_btn2:
        if st.button("🔄 Actualiser", 
                   use_container_width=True):
            st.experimental_rerun()
    
    # Exemples d'annonces
    mes_annonces_exemple = [
        {
            "id": 1,
            "titre": "iPhone 12 Pro 128GB",
            "prix": 600,
            "ville": "Paris 10e",
            "categorie": "Multimédia",
            "description": "iPhone 12 Pro en parfait état, batterie 92%. Avec coque et chargeur.",
            "image": "https://images.pexels.com/photos/607812/pexels-photo-607812.jpeg",
            "vues": 89,
            "promu": True,
            "statut": "active",
            "date_creation": "2024-02-07",
            "favoris_count": 12
        },
        {
            "id": 2,
            "titre": "Vélo de course professionnel",
            "prix": 450,
            "ville": "Paris 15e",
            "categorie": "Véhicules",
            "description": "Vélo de course en excellent état, cadre aluminium 56cm. Peu utilisé.",
            "image": "https://images.pexels.com/photos/276517/pexels-photo-276517.jpeg",
            "vues": 124,
            "promu": False,
            "statut": "active",
            "date_creation": "2024-02-08",
            "favoris_count": 8
        },
    ]
    
    if not mes_annonces_exemple:
        st.info("""
        🎯 **Vous n'avez pas encore publié d'annonce**
        
        Publiez votre première annonce gratuitement et commencez à vendre dès aujourd'hui !
        """)
        
        if st.button("🚀 Publier ma première annonce"):
            st.session_state.show_publish = True
            st.experimental_rerun()
    else:
        # Filtres
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        with col_filter1:
            statut_filter = st.selectbox("Filtrer par statut", 
                                       ["Tous", "Actives", "Vendues", "En attente", "Expirées"])
        with col_filter2:
            categorie_filter = st.selectbox("Filtrer par catégorie", 
                                          ["Toutes", "Multimédia", "Véhicules", "Maison", "Loisirs"])
        with col_filter3:
            tri_filter = st.selectbox("Trier par", 
                                    ["Plus récentes", "Plus de vues", "Plus de favoris", "Prix croissant"])
        
        # Grille d'annonces
        for annonce in mes_annonces_exemple:
            with st.container():
                col_card, col_actions = st.columns([3, 1])
                
                with col_card:
                    st.markdown(f"""
                    <div style="background:white; border-radius:12px; padding:20px; margin:15px 0; box-shadow:0 5px 15px rgba(0,0,0,0.05);">
                        <h4>{annonce['titre']}</h4>
                        <p><strong>{annonce['prix']} €</strong> - 📍 {annonce['ville']}</p>
                        <p>{annonce['description'][:150]}...</p>
                        <p>👁️ {annonce['vues']} vues | ❤️ {annonce['favoris_count']} favoris</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_actions:
                    st.markdown("""
                    <div style="display:flex; flex-direction:column; gap:10px; margin-top:20px;">
                        <button style="background:#06D6A0; color:white; border:none; padding:10px; border-radius:8px; cursor:pointer;">
                            ✏️ Modifier
                        </button>
                        <button style="background:#118AB2; color:white; border:none; padding:10px; border-radius:8px; cursor:pointer;">
                            📊 Stats
                        </button>
                        <button style="background:#FFD166; color:#333; border:none; padding:10px; border-radius:8px; cursor:pointer;">
                            ⭐ Promouvoir
                        </button>
                        <button style="background:#FF6B6B; color:white; border:none; padding:10px; border-radius:8px; cursor:pointer;">
                            🗑️ Supprimer
                        </button>
                    </div>
                    """, unsafe_allow_html=True)