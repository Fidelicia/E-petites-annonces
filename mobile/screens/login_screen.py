from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton, MDTextButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu

class LoginScreen(Screen):
    """Écran de connexion/inscription avec BDD"""
    
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.pays_selectionne = 'France'
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=[40, 50, 40, 50],
            size_hint=(1, 1)
        )
        
        # Logo
        logo = AsyncImage(
            source='https://cdn-icons-png.flaticon.com/512/3132/3132693.png',
            size_hint=(1, 0.25)
        )
        layout.add_widget(logo)
        
        # Titre
        title = MDLabel(
            text='E-petites annonces',
            halign='center',
            font_style='H4',
            size_hint=(1, 0.1),
            theme_text_color='Custom',
            text_color=(0, 0.8, 0.8, 1)
        )
        layout.add_widget(title)
        
        # Sous-titre
        subtitle = MDLabel(
            text='France & Madagascar',
            halign='center',
            font_style='Subtitle1',
            size_hint=(1, 0.05),
            theme_text_color='Secondary'
        )
        layout.add_widget(subtitle)
        
        # Champ username
        self.username_input = MDTextField(
            hint_text='Nom d\'utilisateur',
            icon_right='account',
            size_hint=(1, None),
            height=50,
            mode='rectangle'
        )
        layout.add_widget(self.username_input)
        
        # Champ password
        self.password_input = MDTextField(
            hint_text='Mot de passe',
            icon_right='lock',
            password=True,
            size_hint=(1, None),
            height=50,
            mode='rectangle'
        )
        layout.add_widget(self.password_input)
        
        # Bouton connexion
        btn_login = MDRaisedButton(
            text='SE CONNECTER',
            size_hint=(1, None),
            height=50,
            md_bg_color=(0, 0.8, 0.8, 1),
            font_size=16,
            on_release=self.login
        )
        layout.add_widget(btn_login)
        
        # Bouton inscription
        btn_register = MDRaisedButton(
            text='S\'INSCRIRE',
            size_hint=(1, None),
            height=50,
            md_bg_color=(0, 0, 0, 1),
            font_size=16,
            on_release=self.show_register_dialog
        )
        layout.add_widget(btn_register)
        
        # Bouton test (connexion rapide)
        # btn_test = MDTextButton(
        #     text='Mode démo (utilisateur test)',
        #     halign='center',
        #     size_hint=(1, None),
        #     height=30,
        #     theme_text_color='Custom',
        #     text_color=(0.5, 0.5, 0.5, 1),
        #     on_release=self.demo_login
        # )
        # layout.add_widget(btn_test)
        
        self.add_widget(layout)
    
    def login(self, *args):
        """Connexion avec vérification BDD"""
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if not username or not password:
            self.show_dialog("Erreur", "Veuillez remplir tous les champs")
            return
        
        app = MDApp.get_running_app()
        if app.login_user(username, password):
            self.username_input.text = ''
            self.password_input.text = ''
        else:
            self.show_dialog("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
    
    def demo_login(self, *args):
        """Connexion rapide avec compte de test"""
        app = MDApp.get_running_app()
        if app.login_user('test', 'test123'):
            self.username_input.text = ''
            self.password_input.text = ''
    
    def show_register_dialog(self, *args):
        """Afficher le dialogue d'inscription"""
        if not self.dialog:
            content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
            content.height = 300
            
            self.reg_username = MDTextField(
                hint_text="Nom d'utilisateur *",
                mode='rectangle'
            )
            content.add_widget(self.reg_username)
            
            self.reg_password = MDTextField(
                hint_text="Mot de passe *",
                password=True,
                mode='rectangle'
            )
            content.add_widget(self.reg_password)
            
            self.reg_email = MDTextField(
                hint_text="Email",
                mode='rectangle'
            )
            content.add_widget(self.reg_email)
            
            self.reg_telephone = MDTextField(
                hint_text="Téléphone",
                mode='rectangle'
            )
            content.add_widget(self.reg_telephone)
            
            # Sélecteur de pays
            pays_layout = BoxLayout(size_hint_y=None, height=50)
            self.reg_pays = MDTextField(
                hint_text="Pays",
                text="France",
                mode='rectangle',
                size_hint_x=0.7,
                on_focus=self.open_pays_menu
            )
            pays_layout.add_widget(self.reg_pays)
            
            content.add_widget(pays_layout)
            
            self.dialog = MDDialog(
                title="Créer un compte",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="ANNULER",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="S'INSCRIRE",
                        md_bg_color=(0, 0.8, 0.8, 1),
                        on_release=self.register
                    ),
                ],
            )
        
        self.dialog.open()
    
    def open_pays_menu(self, instance, value):
        """Ouvrir le menu de sélection du pays"""
        if value:
            menu_items = [
                {
                    "text": "France",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x="France": self.set_pays(x),
                },
                {
                    "text": "Madagascar",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x="Madagascar": self.set_pays(x),
                },
            ]
            self.menu = MDDropdownMenu(
                caller=instance,
                items=menu_items,
                width_mult=4,
            )
            self.menu.open()
    
    def set_pays(self, pays):
        """Définir le pays sélectionné"""
        self.reg_pays.text = pays
        self.pays_selectionne = pays
        self.menu.dismiss()
    
    def register(self, *args):
        """Inscription d'un nouvel utilisateur"""
        username = self.reg_username.text.strip()
        password = self.reg_password.text.strip()
        
        if not username or not password:
            self.show_dialog("Erreur", "Nom d'utilisateur et mot de passe requis")
            return
        
        app = MDApp.get_running_app()
        if app.register_user(
            username, 
            password, 
            self.reg_email.text.strip() or None,
            self.reg_telephone.text.strip() or None,
            self.reg_pays.text
        ):
            self.dialog.dismiss()
            self.show_dialog("Succès", "Compte créé avec succès !")
            self.username_input.text = username
            self.password_input.text = password
        else:
            self.show_dialog("Erreur", "Ce nom d'utilisateur existe déjà")
    
    def show_dialog(self, title, text):
        """Afficher une boîte de dialogue"""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()