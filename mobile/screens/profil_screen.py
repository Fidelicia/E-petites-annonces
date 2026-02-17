from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivy.uix.image import AsyncImage
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

class ProfilScreen(Screen):
    """Écran de profil moderne avec déconnexion et retour"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        # ===== TOOLBAR AVEC RETOUR =====
        self.toolbar = MDTopAppBar(
            title="👤 Mon profil",
            elevation=4,
            md_bg_color=(0, 0.8, 0.8, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[
                ["arrow-left", lambda x: self.go_back()]  # RETOUR À L'ACCUEIL
            ],
            right_action_items=[
                ["home", lambda x: self.go_back()]  # AUSSI UN BOUTON ACCUEIL
            ],
            size_hint_y=0.1
        )
        layout.add_widget(self.toolbar)
        
        # ===== SCROLLVIEW =====
        scroll = ScrollView(
            size_hint_y=0.9,
            bar_width=dp(4),
            bar_color=(0, 0.8, 0.8, 1)
        )
        
        conteneur = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(20),
            spacing=dp(20)
        )
        conteneur.bind(minimum_height=conteneur.setter('height'))
        
        # ===== 1. EN-TÊTE DE PROFIL =====
        header_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            padding=dp(20),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(20), dp(20), dp(20), dp(20)],
            elevation=4
        )
        
        # Avatar
        self.avatar = AsyncImage(
            source='https://i.pravatar.cc/150?u=default',
            size_hint=(None, None),
            size=(dp(80), dp(80)),
            pos_hint={'center_x': 0.5}
        )
        header_card.add_widget(self.avatar)
        
        # Nom d'utilisateur
        self.username_label = MDLabel(
            text='Utilisateur',
            font_style='H5',
            bold=True,
            halign='center',
            size_hint_y=None,
            height=dp(40),
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1)
        )
        header_card.add_widget(self.username_label)
        
        # Email
        self.email_label = MDLabel(
            text='email@exemple.com',
            font_style='Subtitle1',
            halign='center',
            size_hint_y=None,
            height=dp(30),
            theme_text_color='Secondary'
        )
        header_card.add_widget(self.email_label)
        
        conteneur.add_widget(header_card)
        
        # ===== 2. STATISTIQUES =====
        stats_card = MDCard(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(100),
            padding=dp(10),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(15), dp(15), dp(15), dp(15)],
            elevation=2
        )
        
        # Annonces
        annonces_box = MDBoxLayout(orientation='vertical', spacing=dp(5))
        self.stats_annonces = MDLabel(
            text='0',
            font_style='H4',
            bold=True,
            halign='center',
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1)
        )
        annonces_box.add_widget(self.stats_annonces)
        annonces_box.add_widget(MDLabel(
            text='Annonces',
            font_style='Caption',
            halign='center',
            theme_text_color='Secondary'
        ))
        stats_card.add_widget(annonces_box)
        
        # Vues
        vues_box = MDBoxLayout(orientation='vertical', spacing=dp(5))
        self.stats_vues = MDLabel(
            text='0',
            font_style='H4',
            bold=True,
            halign='center',
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1)
        )
        vues_box.add_widget(self.stats_vues)
        vues_box.add_widget(MDLabel(
            text='Vues',
            font_style='Caption',
            halign='center',
            theme_text_color='Secondary'
        ))
        stats_card.add_widget(vues_box)
        
        # Favoris
        favoris_box = MDBoxLayout(orientation='vertical', spacing=dp(5))
        self.stats_favoris = MDLabel(
            text='0',
            font_style='H4',
            bold=True,
            halign='center',
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1)
        )
        favoris_box.add_widget(self.stats_favoris)
        favoris_box.add_widget(MDLabel(
            text='Favoris',
            font_style='Caption',
            halign='center',
            theme_text_color='Secondary'
        ))
        stats_card.add_widget(favoris_box)
        
        conteneur.add_widget(stats_card)
        
        # ===== 3. INFORMATIONS PERSONNELLES =====
        info_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(15),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(15), dp(15), dp(15), dp(15)],
            elevation=2
        )
        info_card.bind(minimum_height=info_card.setter('height'))
        
        # Titre
        info_card.add_widget(MDLabel(
            text="📋 Mes informations",
            font_style='H6',
            bold=True,
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(40)
        ))
        
        # Pays
        pays_layout = MDBoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        pays_layout.add_widget(MDIconButton(
            icon='map-marker',
            disabled=True,
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            size_hint_x=0.2
        ))
        self.pays_label = MDLabel(
            text='France',
            font_style='Subtitle1',
            size_hint_x=0.8
        )
        pays_layout.add_widget(self.pays_label)
        info_card.add_widget(pays_layout)
        
        # Téléphone
        telephone_layout = MDBoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        telephone_layout.add_widget(MDIconButton(
            icon='phone',
            disabled=True,
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            size_hint_x=0.2
        ))
        self.telephone_label = MDLabel(
            text='Non renseigné',
            font_style='Subtitle1',
            size_hint_x=0.8
        )
        telephone_layout.add_widget(self.telephone_label)
        info_card.add_widget(telephone_layout)
        
        # Membre depuis
        membre_layout = MDBoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        membre_layout.add_widget(MDIconButton(
            icon='calendar',
            disabled=True,
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            size_hint_x=0.2
        ))
        self.membre_label = MDLabel(
            text='Membre depuis 2026',
            font_style='Subtitle1',
            size_hint_x=0.8
        )
        membre_layout.add_widget(self.membre_label)
        info_card.add_widget(membre_layout)
        
        conteneur.add_widget(info_card)
        
        # ===== 4. BOUTON DÉCONNEXION =====
        logout_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            padding=dp(15),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(15), dp(15), dp(15), dp(15)],
            elevation=2
        )
        
        btn_logout = MDRaisedButton(
            text='🚪 SE DÉCONNECTER',
            size_hint=(1, 1),
            md_bg_color=(0, 0, 0, 1),
            font_size=16,
            on_release=self.confirm_logout
        )
        logout_card.add_widget(btn_logout)
        
        conteneur.add_widget(logout_card)
        
        # ===== 5. BOUTON RETOUR ACCUEIL =====
        home_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            padding=dp(15),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(15), dp(15), dp(15), dp(15)],
            elevation=2
        )
        
        btn_home = MDRaisedButton(
            text='🏠 RETOUR À L\'ACCUEIL',
            size_hint=(1, 1),
            md_bg_color=(0, 0.8, 0.8, 1),
            font_size=16,
            on_release=lambda x: self.go_back()
        )
        home_card.add_widget(btn_home)
        
        conteneur.add_widget(home_card)
        
        # ===== 6. MESSAGE SI NON CONNECTÉ =====
        self.not_logged_card = MDCard(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            padding=dp(20),
            md_bg_color=(1, 1, 1, 1),
            radius=[dp(20), dp(20), dp(20), dp(20)],
            elevation=4
        )
        
        self.not_logged_card.add_widget(MDIconButton(
            icon='account-question',
            icon_size='64sp',
            disabled=True,
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            size_hint_y=0.5
        ))
        
        self.not_logged_card.add_widget(MDLabel(
            text="Vous n'êtes pas connecté",
            font_style='H6',
            bold=True,
            halign='center',
            size_hint_y=0.2
        ))
        
        self.not_logged_card.add_widget(MDLabel(
            text="Connectez-vous pour voir votre profil",
            font_style='Subtitle2',
            halign='center',
            theme_text_color='Secondary',
            size_hint_y=0.15
        ))
        
        btn_login = MDRaisedButton(
            text='SE CONNECTER',
            size_hint=(0.8, None),
            height=dp(40),
            pos_hint={'center_x': 0.5},
            md_bg_color=(0, 0.8, 0.8, 1),
            on_release=lambda x: self.go_login(),
            size_hint_y=0.15
        )
        self.not_logged_card.add_widget(btn_login)
        
        conteneur.add_widget(self.not_logged_card)
        
        scroll.add_widget(conteneur)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        
        # Cacher la carte non-connecté par défaut
        self.not_logged_card.opacity = 0
    
    def on_enter(self):
        """Chargement des données utilisateur"""
        self.load_user_data()
    
    def load_user_data(self):
        """Charger les données de l'utilisateur"""
        app = MDApp.get_running_app()
        
        if app.user:
            # Utilisateur connecté - afficher les infos
            self.not_logged_card.opacity = 0
            self.avatar.source = app.user.get('avatar_url', 'https://i.pravatar.cc/150?u=' + app.user['username'])
            self.username_label.text = app.user['username']
            self.email_label.text = app.user.get('email', 'email@exemple.com')
            self.telephone_label.text = app.user.get('telephone', 'Non renseigné')
            self.pays_label.text = app.user.get('pays', 'France')
            
            # Date d'inscription
            date = app.user.get('date_inscription', '')
            if date:
                self.membre_label.text = f"Membre depuis {date[:10]}"
            
            # Statistiques
            stats = app.db.get_statistiques_utilisateur(app.user['id'])
            self.stats_annonces.text = str(stats['nb_annonces'])
            self.stats_vues.text = str(stats['nb_vues'])
            self.stats_favoris.text = str(stats['nb_favoris_recus'])
        else:
            # Utilisateur non connecté - afficher message
            self.not_logged_card.opacity = 1
            self.avatar.source = 'https://i.pravatar.cc/150?u=default'
            self.username_label.text = 'Invité'
            self.email_label.text = 'Non connecté'
            self.telephone_label.text = '-'
            self.pays_label.text = '-'
            self.membre_label.text = '-'
            self.stats_annonces.text = '0'
            self.stats_vues.text = '0'
            self.stats_favoris.text = '0'
    
    def confirm_logout(self, *args):
        """Confirmer la déconnexion"""
        app = MDApp.get_running_app()
        
        if not app.user:
            self.go_back()
            return
        
        self.dialog = MDDialog(
            title="🚪 Déconnexion",
            text="Êtes-vous sûr de vouloir vous déconnecter ?",
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    theme_text_color='Custom',
                    text_color=(0, 0.8, 0.8, 1),
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SE DÉCONNECTER",
                    md_bg_color=(0, 0, 0, 1),
                    on_release=lambda x: self.logout()
                ),
            ]
        )
        self.dialog.open()
    
    def logout(self, *args):
        """Déconnexion"""
        self.dialog.dismiss()
        app = MDApp.get_running_app()
        app.logout_user()
        self.load_user_data()
    
    def go_back(self):
        """Retour à l'accueil"""
        MDApp.get_running_app().sm.current = 'home'
    
    def go_login(self):
        """Aller à la page de connexion"""
        MDApp.get_running_app().sm.current = 'login'