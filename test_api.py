
import os
import sys

# Ensure repository root is on sys.path so "scripts" package can be imported
root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(root, "..")))

from scripts.api import buscar_carta

carta = buscar_carta("Charizard ex")

print(carta)