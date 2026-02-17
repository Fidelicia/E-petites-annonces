from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from widgets.annonce_card import AnnonceCard
from widgets.navbar import Navbar

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', spacing=0, padding=0)
        
        # ===== TOOLBAR AVEC PROFIL =====
        self.toolbar = MDTopAppBar(
            title="E-petites annonces",
            elevation=4,
            md_bg_color=(0, 0.8, 0.8, 1),
            specific_text_color=(1, 1, 1, 1),
            size_hint_y=0.1,
            right_action_items=[
                ["magnify", lambda x: self.go_to_recherche()],
                ["account-circle", lambda x: self.go_to_profil()]  # 👤 PROFIL ICI !
            ]
        )
        layout.add_widget(self.toolbar)
        
        # ===== TITRE =====
        title = MDLabel(
            text='Annonces récentes',
            font_style='H5',
            size_hint_y=0.08,
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1),
            halign='left',
            padding=[15, 0]
        )
        layout.add_widget(title)
        
        # ===== SCROLLVIEW =====
        scroll = ScrollView(
            size_hint_y=0.72,
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=5
        )
        self.grid = GridLayout(
            cols=1,
            spacing=10,
            padding=[15, 10, 15, 10],
            size_hint_y=None
        )
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        layout.add_widget(scroll)
        
        # ===== NAVBAR =====
        layout.add_widget(Navbar())
        
        self.add_widget(layout)
    
    def on_enter(self):
        self.load_annonces()
    
    def load_annonces(self):
        self.grid.clear_widgets()
        app = MDApp.get_running_app()
        annonces = app.db.get_annonces_recentes()
        
        for annonce in annonces[:10]:
            try:
                card = AnnonceCard(
                    annonce_id=annonce['id'],
                    titre=annonce['titre'],
                    prix=str(annonce['prix']) if annonce['prix'] else 'Prix non spécifié',
                    image_url=annonce['image_urls'][0],
                    ville=annonce['ville']
                )
                self.grid.add_widget(card)
            except:
                pass
    
    def go_to_recherche(self):
        MDApp.get_running_app().sm.current = 'recherche'
    
    def go_to_profil(self):
        app = MDApp.get_running_app()
        if app.user:
            app.sm.get_screen('profil').load_user_data()
            app.sm.current = 'profil'
        else:
            app.sm.current = 'login'