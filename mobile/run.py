#!/usr/bin/env python3
"""
Script de lancement de l'application mobile E-petites annonces
"""

import os
import sys
from pathlib import Path

# Ajouter le dossier courant au path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == '__main__':
    from main import EpetitesAnnoncesApp
    EpetitesAnnoncesApp().run()