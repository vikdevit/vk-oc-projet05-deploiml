import bcrypt
import json
from pathlib import Path

# mot de passe de test
password = b"Test123!"

# génération du hash bcrypt
hashed = bcrypt.hashpw(password, bcrypt.gensalt(12)).decode()

# structure utilisateur
user_data = {
    "username": "admin",
    "password_hash": hashed
}

# chemin du fichier à créer
output_path = Path("data/user.json")
output_path.parent.mkdir(exist_ok=True)

# écriture dans le fichier
with open(output_path, "w") as f:
    json.dump(user_data, f, indent=2)

print("user.json généré avec succès")
