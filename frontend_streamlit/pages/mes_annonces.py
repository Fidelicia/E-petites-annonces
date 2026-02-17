"""
Page Mes Annonces - CORRIGÉE SANS COLONNES IMBRIQUÉES
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from database import get_user_annonces, delete_annonce

def afficher_mes_annonces():
    """Affiche la page Mes Annonces"""
    
    if not st.session_state.user:
        st.warning("🔒 Connectez-vous pour voir vos annonces")
        st.session_state.page = "connexion"
        return
    
    st.title("📝 Mes Annonces")
    
    # Bouton publier
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Gérer vos publications")
    with col2:
        if st.button("➕ Publier une annonce"):
            st.session_state.page = "publier"
            st.experimental_rerun()
    
    try:
        annonces = get_user_annonces(st.session_state.user['id'])
        
        if annonces:
            # Statistiques
            actives = len([a for a in annonces if a.get('statut') == 'active'])
            total_vues = sum(a.get('vues', 0) for a in annonces)
            
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Annonces actives", actives)
            with col_s2:
                st.metric("Annonces totales", len(annonces))
            with col_s3:
                st.metric("Vues totales", total_vues)
            
            st.markdown("---")
            
            # Liste des annonces
            for annonce in annonces:
                with st.container():
                    # Image
                    st.image(annonce.get('image', 'https://images.pexels.com/photos/356056/pexels-photo-356056.jpeg'), 
                            width=120)
                    
                    # Titre
                    st.markdown(f"**{annonce['titre']}**")
                    
                    # Statut
                    statut = annonce.get('statut', 'active')
                    statut_color = 'green' if statut == 'active' else 'red'
                    st.markdown(f"""
                    <span style="
                        background: {statut_color}20;
                        color: {statut_color};
                        padding: 4px 12px;
                        border-radius: 12px;
                        font-size: 12px;
                    ">
                        {statut.upper()}
                    </span>
                    """, unsafe_allow_html=True)
                    
                    # Infos
                    st.markdown(f"**Prix :** {annonce['prix']} € | **Ville :** {annonce['ville']}")
                    st.markdown(f"**Catégorie :** {annonce.get('categorie', 'Général')} | **Vues :** {annonce.get('vues', 0)}")
                    
                    # Boutons
                    col_b1, col_b2, col_b3 = st.columns(3)
                    with col_b1:
                        if st.button("👁️ Voir", key=f"view_{annonce['id']}"):
                            st.session_state.selected_annonce = annonce['id']
                            st.session_state.page = "detail"
                            st.experimental_rerun()
                    with col_b2:
                        if st.button("📊 Stats", key=f"stats_{annonce['id']}"):
                            st.info(f"Vues: {annonce.get('vues', 0)}")
                    with col_b3:
                        if st.button("🗑️ Supprimer", key=f"del_{annonce['id']}"):
                            if delete_annonce(annonce['id'], st.session_state.user['id']):
                                st.success("✅ Annonce supprimée")
                                st.experimental_rerun()
                    
                    st.markdown("---")
        else:
            st.info("Vous n'avez pas encore publié d'annonce")
            
    except Exception as e:
        st.error(f"Erreur: {e}")