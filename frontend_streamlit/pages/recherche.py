"""
Page Recherche
"""
import streamlit as st
import sys
from pathlib import Path

# 🔴 AJOUTE CES 2 LIGNES !
sys.path.append(str(Path(__file__).parent.parent))
from database import get_all_annonces
from components.cards import annonce_card

def afficher_recherche():
    """Affiche la page de recherche"""
    st.title("🔍 Recherche avancée")
    
    # Formulaire de recherche
    filters = afficher_filtres()
    
    # Résultats
    if filters['submitted']:
        afficher_resultats(filters)

def afficher_filtres():
    """Affiche les filtres de recherche"""
    filters = {
        'submitted': False,
        'search': '',
        'categorie': 'Toutes',
        'ville': '',
        'pays': 'Tous',
        'prix_min': 0,
        'prix_max': 10000
    }
    
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            search = st.text_input("Rechercher...")
            categorie = st.selectbox("Catégorie", 
                                   ["Toutes", "Immobilier", "Véhicules", "Multimédia", 
                                    "Maison", "Loisirs", "Mode", "Services", "Emplois", "Produits locaux", "Autres"])
        
        with col2:
            ville = st.text_input("Ville")
            pays = st.selectbox("Pays", ["Tous", "France", "Madagascar"])
        
        prix_min, prix_max = st.slider(
            "Fourchette de prix (€)",
            0, 10000, (0, 10000),
            step=10
        )
        
        submitted = st.form_submit_button("🔍 Rechercher")
        
        if submitted:
            filters.update({
                'submitted': True,
                'search': search,
                'categorie': categorie,
                'ville': ville,
                'pays': pays,
                'prix_min': prix_min,
                'prix_max': prix_max
            })
    
    return filters

def afficher_resultats(filters):
    """Affiche les résultats de recherche"""
    try:
        annonces = get_all_annonces(
            limit=50,
            search=filters['search'] if filters['search'] else None,
            categorie=filters['categorie'] if filters['categorie'] != "Toutes" else None,
            ville=filters['ville'] if filters['ville'] else None,
            pays=filters['pays'] if filters['pays'] != "Tous" else None,
            prix_min=filters['prix_min'],
            prix_max=filters['prix_max']
        )
        
        st.markdown(f"### 📋 Résultats ({len(annonces)} annonces)")
        
        if annonces:
            for annonce in annonces:
                annonce_card(annonce, show_full=False)
                st.markdown("---")
        else:
            st.info("Aucune annonce ne correspond à vos critères.")
    
    except Exception as e:
        st.error(f"Erreur lors de la recherche: {e}")