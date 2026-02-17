from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from widgets.annonce_card import AnnonceCard
from kivymd.uix.toolbar import MDTopAppBar

class MesAnnoncesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        self.toolbar = MDTopAppBar(
            title="Mes annonces",
            elevation=4,
            md_bg_color=(0, 0.8, 0.8, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            right_action_items=[["plus", lambda x: self.go_to_publier()]]
        )
        layout.add_widget(self.toolbar)
        
        # Statistiques
        self.stats_layout = MDBoxLayout(
            size_hint_y=0.15,
            spacing=10,
            padding=10
        )
        layout.add_widget(self.stats_layout)
        
        # ScrollView pour les annonces
        scroll = MDScrollView()
        self.grid = GridLayout(
            cols=1,
            spacing=10,
            padding=10,
            size_hint_y=None
        )
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        layout.add_widget(scroll)
        
        # Message vide
        self.empty_label = MDLabel(
            text="Vous n'avez pas encore publié d'annonce",
            halign='center',
            theme_text_color='Secondary',
            size_hint_y=0.85
        )
        self.empty_label.opacity = 0
        layout.add_widget(self.empty_label)
        
        self.add_widget(layout)
    
    def on_enter(self):
        self.load_mes_annonces()
    
    def load_mes_annonces(self):
        app = MDApp.get_running_app()
        if not app.user:
            self.go_back()
            return
        
        # Statistiques
        stats = app.db.get_statistiques_utilisateur(app.user['id'])
        self.stats_layout.clear_widgets()
        
        stats_cards = [
            {'value': stats['nb_annonces'], 'label': 'Annonces', 'icon': 'format-list-bulleted'},
            {'value': stats['nb_vues'], 'label': 'Vues', 'icon': 'eye'},
            {'value': stats['nb_favoris_recus'], 'label': 'Favoris', 'icon': 'heart'},
        ]
        
        for stat in stats_cards:
            card = MDBoxLayout(
                orientation='vertical',
                size_hint_x=0.33,
                padding=10,
                md_bg_color=(0.95, 0.95, 0.95, 1),
                radius=[10,]
            )
            icon = MDIconButton(icon=stat['icon'], theme_text_color='Custom',
                              text_color=(0,0.8,0.8,1), size_hint_y=0.5)
            icon.disabled = True
            card.add_widget(icon)
            card.add_widget(MDLabel(text=str(stat['value']), halign='center',
                                  font_style='H5', size_hint_y=0.25))
            card.add_widget(MDLabel(text=stat['label'], halign='center',
                                  font_style='Caption', size_hint_y=0.25))
            self.stats_layout.add_widget(card)
        
        # Annonces
        self.grid.clear_widgets()
        annonces = app.db.get_annonces_par_utilisateur(app.user['id'])
        
        if annonces:
            self.grid.opacity = 1
            self.empty_label.opacity = 0
            for annonce in annonces:
                card = AnnonceCard(
                    annonce_id=annonce['id'],
                    titre=annonce['titre'],
                    prix=str(annonce['prix']) if annonce['prix'] else 'Prix non spécifié',
                    image_url=annonce['image_urls'][0] if annonce['image_urls'] else 'https://img.icons8.com/ios/100/no-image.png',
                    ville=annonce['ville']
                )
                self.grid.add_widget(card)
        else:
            self.grid.opacity = 0
            self.empty_label.opacity = 1
    
    def go_to_publier(self):
        MDApp.get_running_app().sm.current = 'publier'
    
    def go_back(self):
        MDApp.get_running_app().sm.current = 'home'