"""
Composant de carte - VERSION AGRANDIE
"""
import streamlit as st
import folium
from streamlit_folium import folium_static
import random

def afficher_carte_annonces(annonces):
    """Affiche une carte AGRANDIE avec les annonces"""
    
    if not annonces:
        st.info("Aucune annonce à afficher sur la carte")
        return
    
    # Centre par défaut
    center_lat, center_lon = 46.603354, 1.888334
    zoom = 5
    
    # Créer la carte PLUS GRANDE
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, control_scale=True)
    
    # Ajouter les marqueurs
    for annonce in annonces[:50]:
        lat = center_lat + random.uniform(-2, 2)
        lon = center_lon + random.uniform(-2, 2)
        
        popup_html = f"""
        <div style="width:250px;">
            <h4 style="color:#06D6A0; margin:0;">{annonce.get('titre', '')[:40]}</h4>
            <p style="font-size:18px; font-weight:bold; margin:10px 0; color:#333;">
                {annonce.get('prix', 0)} €
            </p>
            <p style="margin:5px 0;">
                📍 {annonce.get('ville', '')}, {annonce.get('pays', '')}
            </p>
            <p style="margin:5px 0;">
                📁 {annonce.get('categorie', '')}
            </p>
            <p style="margin:5px 0; color:#666;">
                👤 {annonce.get('vendeur', '')}
            </p>
        </div>
        """
        
        folium.Marker(
            [lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=annonce.get('titre', '')[:30],
            icon=folium.Icon(color='green', icon='home', prefix='fa')
        ).add_to(m)
    
    # Afficher la carte avec dimensions AGRANDIES
    folium_static(m, width=800, height=500)
    
    # Légende
    st.markdown("""
    <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px; text-align: center;">
        <span style="color: #666;">📍 {0} annonces affichées sur la carte</span>
    </div>
    """.format(len(annonces[:50])), unsafe_allow_html=True)

def afficher_carte_annonce_detail(annonce):
    """Carte pour détail d'annonce"""
    if not annonce:
        return
    
    st.markdown("### 🗺️ Localisation")
    
    if annonce.get('pays') == 'Madagascar':
        center_lat, center_lon = -18.8792, 47.5079
    else:
        center_lat, center_lon = 48.8566, 2.3522
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, control_scale=True)
    
    popup_html = f"""
    <div style="width:200px;">
        <h4 style="color:#06D6A0;">{annonce.get('titre', '')[:30]}</h4>
        <p><strong>{annonce.get('prix', 0)} €</strong></p>
        <p>📍 {annonce.get('ville', '')}, {annonce.get('pays', '')}</p>
    </div>
    """
    
    folium.Marker(
        [center_lat, center_lon],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=annonce.get('titre', '')[:20],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    folium_static(m, width=700, height=350)