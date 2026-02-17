"""
Page d'accueil - CARTE AGRANDIE
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database import get_all_annonces, get_stats
from components.cards import annonce_card, stat_card
from components.map import afficher_carte_annonces

def afficher_accueil():
    """Affiche la page d'accueil"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🏠 E-petites Annonces</h1>
        <p>La plateforme 100% Python pour acheter et vendre localement</p>
        <div style="margin-top: 15px;">
            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; margin: 0 5px;">
                🇫🇷 France
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; margin: 0 5px;">
                🇲🇬 Madagascar
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistiques
    stats = get_stats()
    cols = st.columns(4)
    with cols[0]:
        stat_card(stats['annonces'], "Annonces", "📋")
    with cols[1]:
        stat_card(stats['vues'], "Vues", "👁️")
    with cols[2]:
        stat_card(stats['utilisateurs'], "Membres", "👤")
    with cols[3]:
        stat_card(stats['messages'], "Messages", "💬")
    
    # CARTE AGRANDIE - MÊME TAILLE QUE LES ANNONCES
    st.markdown("### 🗺️ Carte des annonces")
    annonces = get_all_annonces(limit=50)
    
    # Conteneur avec hauteur augmentée
    with st.container():
        afficher_carte_annonces(annonces)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Dernières annonces
    st.markdown("### 📢 Dernières annonces")
    annonces = get_all_annonces(limit=10)
    
    if annonces:
        for annonce in annonces:
            annonce_card(annonce, show_actions=True)
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    else:
        st.info("Aucune annonce pour le moment")