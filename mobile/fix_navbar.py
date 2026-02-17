import os
import shutil

print("🔧 CORRECTION DE LA NAVBAR - ULTIME")

# 1. SAUVEGARDER L'ANCIENNE NAVBAR
if os.path.exists("widgets/navbar.py"):
    shutil.copy("widgets/navbar.py", "widgets/navbar_backup.py")
    print("✅ Sauvegarde créée: widgets/navbar_backup.py")

# 2. LISTE DES ÉCRANS À CORRIGER
screens = [
    "home_screen.py",
    "recherche_screen.py", 
    "favoris_screen.py",
    "messages_screen.py",
    "carte_screen.py"
]

for screen in screens:
    path = f"screens/{screen}"
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
        
        # Ajouter import Navbar si manquant
        if "from widgets.navbar import Navbar" not in content:
            if "from kivymd.app import MDApp" in content:
                content = content.replace(
                    "from kivymd.app import MDApp",
                    "from kivymd.app import MDApp\nfrom widgets.navbar import Navbar"
                )
            elif "import MDApp" in content:
                content = content.replace(
                    "import MDApp",
                    "import MDApp\nfrom widgets.navbar import Navbar"
                )
        
        # Ajouter Navbar dans build_ui
        if "layout.add_widget(Navbar())" not in content:
            if "self.add_widget(layout)" in content:
                content = content.replace(
                    "self.add_widget(layout)",
                    "        layout.add_widget(Navbar())\n        self.add_widget(layout)"
                )
        
        with open(path, "w") as f:
            f.write(content)
        print(f"✅ Corrigé: {screen}")

print("\n🎯 TOUS LES ÉCRANS SONT CORRIGÉS !")
print("🚀 Lance: python run.py")