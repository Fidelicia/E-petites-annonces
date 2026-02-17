"""
Composants de cartes - CORRIGÉ (bouton contacter)
"""
import streamlit as st
from database import is_favori, toggle_favori

def annonce_card(annonce, show_actions=True):
    """Affiche une carte d'annonce"""
    
    with st.container():
        st.markdown(f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            border-left: 5px solid #06D6A0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        ">
            <div style="display: flex; gap: 15px;">
                <div style="flex: 1;">
                    <img src="{annonce.get('image', 'https://images.pexels.com/photos/356056/pexels-photo-356056.jpeg')}" 
                         style="width: 100%; height: 120px; object-fit: cover; border-radius: 8px;">
                </div>
                <div style="flex: 2;">
                    <h4 style="margin: 0 0 8px 0; color: #333;">{annonce.get('titre', 'Sans titre')}</h4>
                    <h3 style="margin: 0 0 10px 0; color: #06D6A0;">{annonce.get('prix', 0)} €</h3>
                    <p style="margin: 5px 0; font-size: 14px; color: #666;">
                        📍 {annonce.get('ville', '')}, {annonce.get('pays', '')} | 
                        📁 {annonce.get('categorie', '')}
                    </p>
                    <p style="margin: 5px 0; font-size: 14px; color: #666;">
                        👤 {annonce.get('vendeur', '')} | 👁️ {annonce.get('vues', 0)} vues
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if show_actions:
            afficher_actions_annonce(annonce)

def afficher_actions_annonce(annonce):
    """Affiche les boutons d'action"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👁️ Voir", key=f"view_{annonce['id']}"):
            st.session_state.selected_annonce = annonce['id']
            st.session_state.page = "detail"
            st.experimental_rerun()
    
    with col2:
        if st.session_state.user:
            is_fav = is_favori(st.session_state.user['id'], annonce['id'])
            fav_text = "❤️ Retirer" if is_fav else "🤍 Favori"
            if st.button(fav_text, key=f"fav_{annonce['id']}"):
                toggle_favori(st.session_state.user['id'], annonce['id'])
                st.experimental_rerun()
        else:
            if st.button("🤍 Favori", key=f"fav_{annonce['id']}_noauth"):
                st.warning("🔒 Connectez-vous pour ajouter aux favoris")
    
    with col3:
        if st.session_state.user:
            if st.button("💬 Contacter", key=f"contact_{annonce['id']}"):
                # 🔴 IMPORTANT: Définir l'interlocuteur
                st.session_state.selected_interlocuteur = annonce.get('user_id')
                st.session_state.page = "messagerie"
                st.experimental_rerun()
        else:
            if st.button("💬 Contacter", key=f"contact_{annonce['id']}_noauth"):
                st.warning("🔒 Connectez-vous pour contacter")
    
    with col4:
        if st.session_state.user:
            if st.button("⚠️ Signaler", key=f"report_{annonce['id']}"):
                st.session_state.signal_annonce = annonce['id']
                st.session_state.page = "signalement"
                st.experimental_rerun()
        else:
            if st.button("⚠️ Signaler", key=f"report_{annonce['id']}_noauth"):
                st.warning("🔒 Connectez-vous pour signaler")

def stat_card(value, label, icon):
    st.markdown(f"""
    <div style="
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        border-top: 4px solid #06D6A0;
        margin: 10px 0;
    ">
        <h3 style="margin: 0; color: #06D6A0; font-size: 28px;">{icon} {value}</h3>
        <p style="margin: 10px 0 0 0; color: #666; font-size: 14px;">{label}</p>
    </div>
    """, unsafe_allow_html=True)