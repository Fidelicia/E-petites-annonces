from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from widgets.annonce_card import AnnonceCard
from widgets.navbar import Navbar

class FavorisScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar
        self.toolbar = MDTopAppBar(
            title="Mes favoris",
            elevation=4,
            md_bg_color=(0, 0.8, 0.8, 1),
            specific_text_color=(1, 1, 1, 1),
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        layout.add_widget(self.toolbar)
        
        # Titre
        title = MDLabel(
            text='❤️ Annonces favorites',
            font_style='H5',
            size_hint_y=0.1,
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            halign='center'
        )
        layout.add_widget(title)
        
        # Liste
        scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=10, padding=15, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        layout.add_widget(scroll)
        
        # Message vide
        self.empty_label = MDLabel(
            text="Aucun favori",
            halign='center',
            theme_text_color='Secondary'
        )
        layout.add_widget(self.empty_label)
        
        # Navbar
        layout.add_widget(Navbar())
        
        self.add_widget(layout)
    
    def on_enter(self):
        self.load_favoris()
    
    def load_favoris(self):
        self.grid.clear_widgets()
        app = MDApp.get_running_app()
        
        if not app.user:
            self.go_back()
            return
        
        favoris = app.db.get_favoris(app.user['id'])
        
        if favoris:
            self.empty_label.opacity = 0
            for a in favoris:
                card = AnnonceCard(
                    annonce_id=a['id'],
                    titre=a['titre'],
                    prix=str(a['prix']) if a['prix'] else 'Prix non spécifié',
                    image_url=a['image_urls'][0],
                    ville=a['ville']
                )
                # Forcer l'icône cœur à être rempli
                card.btn_favori.icon = 'heart'
                card.est_favori = True
                self.grid.add_widget(card)
        else:
            self.empty_label.opacity = 1
    
    def go_back(self):
        MDApp.get_running_app().sm.current = 'home'