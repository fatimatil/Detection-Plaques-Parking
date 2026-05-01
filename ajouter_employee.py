import sqlite3

def ajouter_nouveau_personnel():
    print("--- AJOUT D'UN NOUVEL EMPLOYÉ AU PARKING ---")
    
    # 1. Saisie des informations
    nom = input("Nom complet de l'employé : ").strip()
    plaque = input("Numéro de plaque (ex: 415K7467) : ").strip().upper().replace(" ", "")
    poste = input("Poste ou Département : ").strip()

    if not nom or not plaque:
        print("Erreur : Le nom et la plaque sont obligatoires.")
        return

    # 2. Connexion et insertion
    try:
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO employees (nom, plaque, poste) 
            VALUES (?, ?, ?)
        """, (nom, plaque, poste))
        
        conn.commit()
        print(f"\n Succès ! {nom} a été ajouté avec la plaque {plaque}.")
        
    except sqlite3.IntegrityError:
        print(f"\n Erreur : La plaque '{plaque}' existe déjà dans la base de données.")
    except sqlite3.Error as e:
        print(f"\n Une erreur SQLite est survenue : {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    while True:
        ajouter_nouveau_personnel()
        continuer = input("\n Voulez-vous ajouter un autre employé ? (o/n) : ").lower()
        if continuer != 'o':
            break
    print("Fermeture du programme de gestion.")