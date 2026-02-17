from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivy.uix.image import AsyncImage
from widgets.annonce_card import AnnonceCard
from widgets.navbar import Navbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp

class CarteScreen(Screen):
    """Carte interactive - VERSION AVEC SCROLL AÉRÉ"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_pays = 'France'
        self.current_ville = 'Paris'
        self.build_ui()
    
    def build_ui(self):
        # LAYOUT PRINCIPAL
        layout = MDBoxLayout(orientation='vertical', spacing=0, padding=0)
        
        # ===== TOOLBAR FIXE (10%) =====
        self.toolbar = MDTopAppBar(
            title="🗺️ Carte des villes",
            elevation=4,
            md_bg_color=(0, 0.8, 0.8, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[
                ["crosshairs-gps", lambda x: self.ma_position()]
            ],
            size_hint_y=0.08
        )
        layout.add_widget(self.toolbar)
        
        # ===== SCROLLVIEW PRINCIPAL (TOUT LE CONTENU SCROLLABLE) =====
        scroll_principal = ScrollView(
            size_hint_y=0.84,
            bar_width=dp(6),
            bar_color=(0, 0.8, 0.8, 1),
            bar_inactive_color=(0.8, 0.8, 0.8, 0.5),
            do_scroll_x=False,
            do_scroll_y=True
        )
        
        conteneur = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(15),
            spacing=dp(20)
        )
        conteneur.bind(minimum_height=conteneur.setter('height'))
        
        # ===== 1. SECTION CARTE / VILLE ACTUELLE =====
        self.carte_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            padding=dp(20),
            md_bg_color=(0.98, 0.98, 0.98, 1),
            radius=[dp(20), dp(20), dp(20), dp(20)],
            elevation=4,
            spacing=dp(10)
        )
        
        # Icône de la ville
        self.carte_icon = MDIconButton(
            icon='map-marker',
            icon_size='64sp',
            size_hint=(1, 0.5),
            disabled=True,
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1)
        )
        self.carte_card.add_widget(self.carte_icon)
        
        # Nom de la ville
        self.ville_label = MDLabel(
            text="📍 Paris, France",
            font_style='H5',
            bold=True,
            halign='center',
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            size_hint_y=0.25
        )
        self.carte_card.add_widget(self.ville_label)
        
        # Description
        self.desc_label = MDLabel(
            text="Capitale • 2.1M habitants • Région Île-de-France",
            font_style='Subtitle1',
            halign='center',
            theme_text_color='Secondary',
            size_hint_y=0.25
        )
        self.carte_card.add_widget(self.desc_label)
        
        conteneur.add_widget(self.carte_card)
        
        # ===== 2. BOUTONS PAYS =====
        pays_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            padding=dp(15),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(15), dp(15), dp(15), dp(15)],
            elevation=2
        )
        
        pays_layout = MDBoxLayout(
            spacing=dp(15),
            size_hint_y=1
        )
        
        self.btn_france = MDRaisedButton(
            text='🇫🇷 France',
            size_hint=(0.5, 1),
            md_bg_color=(0, 0.8, 0.8, 1),
            on_release=lambda x: self.changer_pays('France')
        )
        pays_layout.add_widget(self.btn_france)
        
        self.btn_mada = MDRaisedButton(
            text='🇲🇬 Madagascar',
            size_hint=(0.5, 1),
            md_bg_color=(0.5, 0.5, 0.5, 1),
            on_release=lambda x: self.changer_pays('Madagascar')
        )
        pays_layout.add_widget(self.btn_mada)
        
        pays_card.add_widget(pays_layout)
        conteneur.add_widget(pays_card)
        
        # ===== 3. SECTION VILLES =====
        villes_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(15),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(15), dp(15), dp(15), dp(15)],
            elevation=2
        )
        villes_card.bind(minimum_height=villes_card.setter('height'))
        
        # Titre des villes
        villes_card.add_widget(MDLabel(
            text="📍 Villes disponibles",
            font_style='H6',
            bold=True,
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(40)
        ))
        
        # Grille des villes (2 colonnes)
        self.villes_grid = GridLayout(
            cols=2,
            spacing=dp(15),
            padding=[dp(0), dp(10), dp(0), dp(10)],
            size_hint_y=None
        )
        self.villes_grid.bind(minimum_height=self.villes_grid.setter('height'))
        
        self.villes_france = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Bordeaux', 'Lille', 'Nice', 'Nantes']
        self.villes_mada = ['Antananarivo', 'Toamasina', 'Fianarantsoa', 'Mahajanga', 'Toliara', 'Antsiranana', 'Antsirabe', 'Nosy Be']
        
        self.mettre_a_jour_villes('France')
        
        villes_card.add_widget(self.villes_grid)
        conteneur.add_widget(villes_card)
        
        # ===== 4. SECTION ANNONCES =====
        annonces_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(15),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(15), dp(15), dp(15), dp(15)],
            elevation=2
        )
        annonces_card.bind(minimum_height=annonces_card.setter('height'))
        
        # En-tête des annonces
        self.resultats_label = MDLabel(
            text="📋 Annonces à Paris",
            font_style='H6',
            bold=True,
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(40)
        )
        annonces_card.add_widget(self.resultats_label)
        
        # Liste des annonces (scrollable)
        scroll_annonces = ScrollView(
            size_hint_y=None,
            height=dp(300),
            bar_width=dp(6),
            bar_color=(0, 0.8, 0.8, 1)
        )
        
        self.grid_annonces = GridLayout(
            cols=1,
            spacing=dp(10),
            padding=[dp(0), dp(5), dp(0), dp(5)],
            size_hint_y=None
        )
        self.grid_annonces.bind(minimum_height=self.grid_annonces.setter('height'))
        scroll_annonces.add_widget(self.grid_annonces)
        annonces_card.add_widget(scroll_annonces)
        
        conteneur.add_widget(annonces_card)
        
        scroll_principal.add_widget(conteneur)
        layout.add_widget(scroll_principal)
        
        # ===== NAVBAR FIXE EN BAS (8%) =====
        navbar = Navbar()
        navbar.size_hint_y = 0.08
        layout.add_widget(navbar)
        
        self.add_widget(layout)
        
        # Charger les annonces
        self.charger_annonces_ville('Paris', 'France')
    
    def mettre_a_jour_villes(self, pays):
        """Mettre à jour la grille des villes avec des cartes stylées"""
        self.villes_grid.clear_widgets()
        villes = self.villes_france if pays == 'France' else self.villes_mada
        couleur = (0, 0.8, 0.8, 1) if pays == 'France' else (0.8, 0.4, 0, 1)
        
        for ville in villes[:8]:  # Maximum 8 villes
            # Carte ville stylée
            ville_card = MDCard(
                orientation='vertical',
                size_hint_y=None,
                height=dp(90),
                padding=dp(10),
                md_bg_color=(0.98, 0.98, 0.98, 1),
                radius=[dp(12), dp(12), dp(12), dp(12)],
                elevation=2,
                on_release=lambda x, v=ville: self.charger_ville(v)
            )
            
            # Icône
            icon = MDIconButton(
                icon='map-marker',
                icon_size='32sp',
                size_hint_y=0.6,
                disabled=True,
                theme_text_color='Custom',
                text_color=couleur
            )
            ville_card.add_widget(icon)
            
            # Nom
            label = MDLabel(
                text=ville,
                font_style='Subtitle1',
                bold=True,
                halign='center',
                size_hint_y=0.4
            )
            ville_card.add_widget(label)
            
            self.villes_grid.add_widget(ville_card)
    
    def changer_pays(self, pays):
        """Changer de pays"""
        self.current_pays = pays
        
        if pays == 'France':
            self.btn_france.md_bg_color = (0, 0.8, 0.8, 1)
            self.btn_mada.md_bg_color = (0.5, 0.5, 0.5, 1)
            self.mettre_a_jour_villes('France')
            self.charger_ville('Paris')
        else:
            self.btn_mada.md_bg_color = (0.8, 0.4, 0, 1)
            self.btn_france.md_bg_color = (0.5, 0.5, 0.5, 1)
            self.mettre_a_jour_villes('Madagascar')
            self.charger_ville('Antananarivo')
    
    def charger_ville(self, ville):
        """Charger une ville"""
        self.current_ville = ville
        
        # Mettre à jour les infos
        self.ville_label.text = f"📍 {ville}, {self.current_pays}"
        
        # Descriptions détaillées
        descriptions = {
            'Paris': 'Capitale de la France • 2.1M habitants • Île-de-France',
            'Lyon': 'Capitale des Gaules • 520k habitants • Auvergne-Rhône-Alpes',
            'Marseille': 'Cité phocéenne • 870k habitants • Provence-Alpes-Côte d\'Azur',
            'Toulouse': 'Ville rose • 490k habitants • Occitanie',
            'Bordeaux': 'Capitale du vin • 260k habitants • Nouvelle-Aquitaine',
            'Lille': 'Capitale des Flandres • 230k habitants • Hauts-de-France',
            'Nice': 'Perle de la Côte d\'Azur • 340k habitants • Provence-Alpes-Côte d\'Azur',
            'Nantes': 'Cité des Ducs • 320k habitants • Pays de la Loire',
            'Antananarivo': 'Capitale de Madagascar • 1.3M habitants • Analamanga',
            'Toamasina': 'Principal port • 300k habitants • Atsinanana',
            'Fianarantsoa': 'Capitale du Sud • 200k habitants • Haute Matsiatra',
            'Mahajanga': 'Ville côtière • 250k habitants • Boeny',
            'Toliara': 'Port du Sud • 160k habitants • Atsimo-Andrefana',
            'Antsiranana': 'Port du Nord • 130k habitants • Diana',
            'Antsirabe': 'Ville thermale • 260k habitants • Vakinankaratra',
            'Nosy Be': "Île paradisiaque • 110k habitants • Diana",
        }
        
        self.desc_label.text = descriptions.get(ville, 'Ville')
        
        # Couleurs selon le pays
        if self.current_pays == 'France':
            self.carte_icon.text_color = (0, 0.8, 0.8, 1)
            self.ville_label.text_color = (0, 0.8, 0.8, 1)
        else:
            self.carte_icon.text_color = (0.8, 0.4, 0, 1)
            self.ville_label.text_color = (0.8, 0.4, 0, 1)
        
        self.resultats_label.text = f"📋 Annonces à {ville} ({self.current_pays})"
        self.charger_annonces_ville(ville, self.current_pays)
    
    def charger_annonces_ville(self, ville, pays):
        """Charger les annonces d'une ville"""
        self.grid_annonces.clear_widgets()
        app = MDApp.get_running_app()
        
        toutes = app.db.get_annonces_recentes(50)
        count = 0
        
        for annonce in toutes:
            if annonce.get('ville') == ville and annonce.get('pays') == pays:
                try:
                    card = AnnonceCard(
                        annonce_id=annonce['id'],
                        titre=annonce['titre'],
                        prix=str(annonce['prix']) if annonce['prix'] else 'Prix non spécifié',
                        image_url=annonce['image_urls'][0],
                        ville=annonce['ville']
                    )
                    self.grid_annonces.add_widget(card)
                    count += 1
                except:
                    pass
        
        if count == 0:
            msg_card = MDCard(
                orientation='vertical',
                size_hint_y=None,
                height=dp(100),
                padding=dp(20),
                md_bg_color=(0.98, 0.98, 0.98, 1),
                radius=[dp(12), dp(12), dp(12), dp(12)]
            )
            msg_card.add_widget(MDLabel(
                text="😕",
                font_style='H2',
                halign='center',
                size_hint_y=0.5
            ))
            msg_card.add_widget(MDLabel(
                text=f"Aucune annonce à {ville}",
                halign='center',
                theme_text_color='Secondary',
                size_hint_y=0.5
            ))
            self.grid_annonces.add_widget(msg_card)
    
    def ma_position(self):
        """Ma position simulée"""
        if self.current_pays == 'France':
            self.charger_ville('Paris')
            position = "Paris, France"
        else:
            self.charger_ville('Antananarivo')
            position = "Antananarivo, Madagascar"
        
        dialog = MDDialog(
            title="📍 Ma position",
            text=f"Vous êtes à {position}",
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def go_back(self):
        MDApp.get_running_app().sm.current = 'home'