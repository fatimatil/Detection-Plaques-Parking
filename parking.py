import sqlite3

# Connexion (si le fichier n'existe pas, il le crée automatiquement)
conn = sqlite3.connect('parking2.db')
cursor = conn.cursor()

# Création de la table
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    plaque TEXT UNIQUE NOT NULL,
    poste TEXT
)
''')

# Ajouter ta plaque de test
try:
    cursor.execute("INSERT INTO employees (nom, plaque, poste) VALUES (?, ?, ?)", 
                   ('Michel', '415K7467', 'Maintenance'))
    conn.commit()
    print("✅ Base SQLite créée et plaque 415K7467 ajoutée !")
except sqlite3.IntegrityError:
    print("La plaque existe déjà dans la base.")

conn.close()