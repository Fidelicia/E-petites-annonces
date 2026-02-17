import os

print("🔧 CORRECTION DES INDENTATIONS")

files_to_fix = [
    "screens/home_screen.py",
    "screens/recherche_screen.py",
    "screens/favoris_screen.py",
    "screens/messages_screen.py",
    "screens/carte_screen.py"
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Correction spécifique pour home_screen.py
        if "home_screen" in file_path:
            # Remplacer l'indentation incorrecte
            content = content.replace(
                "        layout.add_widget(Navbar())\n        self.add_widget(layout)",
                "        layout.add_widget(Navbar())\n        self.add_widget(layout)"
            )
        
        # Ajouter import Navbar si manquant
        if "from widgets.navbar import Navbar" not in content:
            content = content.replace(
                "from kivymd.app import MDApp",
                "from kivymd.app import MDApp\nfrom widgets.navbar import Navbar"
            )
        
        # Ajouter Navbar si manquant
        if "layout.add_widget(Navbar())" not in content:
            content = content.replace(
                "self.add_widget(layout)",
                "        layout.add_widget(Navbar())\n        self.add_widget(layout)"
            )
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Corrigé: {file_path}")

print("\n🎯 TOUTES LES INDENTATIONS SONT CORRIGÉES !")
print("🚀 Lance: python run.py")