"""
Carte d'annonce réutilisable
"""
import streamlit as st
import pandas as pd
from datetime import datetime

def annonce_card(annonce: dict, show_actions: bool = True):
    """
    Affiche une carte d'annonce
    """
    with st.container():
        # Style de la carte
        st.markdown("""
        <style>
        .annonce-card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background: white;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .annonce-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .annonce-promue {
            border-left: 5px solid #FFD166;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Classe CSS conditionnelle
        card_class = "annonce-card"
        if annonce.get('est_promu'):
            card_class += " annonce-promue"
        
        with st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True):
            # En-tête
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Badge promu
                if annonce.get('est_promu'):
                    st.markdown('<span style="background: #FFD166; padding: 3px 8px; border-radius: 5px; font-size: 12px;">⭐ PROMUE</span>', 
                              unsafe_allow_html=True)
                
                # Titre
                st.markdown(f"### {annonce.get('titre', 'Sans titre')}")
                
                # Catégorie et ville
                st.caption(f"📁 {annonce.get('categorie_nom', 'Non catégorisé')} | 📍 {annonce.get('ville', 'N/A')}")
            
            with col2:
                # Prix
                prix = annonce.get('prix', 0)
                st.markdown(f"""
                <div style="text-align: right;">
                    <h3 style="color: #118AB2; margin: 0;">{prix}€</h3>
                    <small style="color: #888;">{ 'Négociable' if annonce.get('negociable') else 'Fixe' }</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Description (tronquée)
            description = annonce.get('description', '')
            if len(description) > 150:
                description = description[:150] + "..."
            st.write(description)
            
            # Images (première image seulement)
            images = annonce.get('images', [])
            if images:
                # Récupérer l'URL de la première image
                first_image = images[0]
                if first_image.get('image'):
                    # Dans un vrai projet, on chargerait l'image depuis l'URL
                    # Pour la démo, on affiche un placeholder
                    st.image("https://via.placeholder.com/300x200/06D6A0/FFFFFF?text=Annonce", 
                            caption="Image de l'annonce", width=300)
            
            # Footer avec statistiques
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            
            with col_f1:
                st.caption(f"👁️ {annonce.get('vues', 0)} vues")
            
            with col_f2:
                date_str = annonce.get('date_creation', '')
                if date_str:
                    try:
                        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        st.caption(f"📅 {date_obj.strftime('%d/%m/%Y')}")
                    except:
                        st.caption("📅 Date N/A")
            
            with col_f3:
                distance = annonce.get('distance')
                if distance:
                    st.caption(f"📍 {distance} km")
            
            with col_f4:
                type_annonce = annonce.get('type_annonce', 'offre')
                type_text = "📤 Offre" if type_annonce == 'offre' else "📥 Demande"
                st.caption(type_text)
            
            # Actions
            if show_actions:
                st.markdown("---")
                col_a1, col_a2, col_a3 = st.columns(3)
                
                with col_a1:
                    if st.button("👁️ Voir détails", key=f"view_{annonce['id']}"):
                        st.session_state.selected_annonce = annonce['id']
                        st.rerun()
                
                with col_a2:
                    favori = annonce.get('est_favori', False)
                    btn_text = "❤️ Retirer" if favori else "🤍 Ajouter"
                    if st.button(btn_text, key=f"fav_{annonce['id']}"):
                        from utils.api_client import api_client
                        if favori:
                            # Retirer des favoris
                            pass
                        else:
                            # Ajouter aux favoris
                            pass
                
                with col_a3:
                    if st.button("💬 Contacter", key=f"msg_{annonce['id']}"):
                        st.session_state.contact_annonce = annonce['id']
                        st.rerun()