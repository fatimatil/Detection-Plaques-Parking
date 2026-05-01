import cv2
import numpy as np
import easyocr
from ultralytics import YOLO
import sqlite3
import time

print("Système prêt. Connexion à la base de données...")

# Chargement des modèles
yolo_model = YOLO('best.pt')
reader = easyocr.Reader(['en'])

# Nettoyage texte OCR
def clean_plate_text(text):
    return "".join([c for c in text if c.isalnum()]).upper()

# Vérification base de données
def verifier_acces_db(plaque_detectee):
    try:
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nom FROM employees WHERE plaque = ?", (plaque_detectee,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
        return None

# --- LECTURE VIDÉO ---
VIDEO_PATH = "Download(1).mp4"
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("Erreur : impossible d'ouvrir la vidéo")
    exit()

# ──────────────────────────────────────────────────────────
# 🛠️ CORRECTION DE LA FENÊTRE D'AFFICHAGE
# ──────────────────────────────────────────────────────────
# On crée une fenêtre nommée "Parking" qui peut être redimensionnée
cv2.namedWindow("Parking", cv2.WINDOW_NORMAL) 
# On lui donne une taille initiale raisonnable (800x600 par exemple)
cv2.resizeWindow("Parking", 600, 600) 

acces_valide = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Fin de la vidéo.")
        break

    results = yolo_model(frame, stream=True)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Extraire la plaque
            plate_roi = frame[y1:y2, x1:x2]
            if plate_roi.size == 0:
                continue

            # OCR
            ocr_results = reader.readtext(plate_roi, detail=0)
            raw_text = "".join(ocr_results)
            clean_text = clean_plate_text(raw_text)

            # Vérification accès
            nom_employe = verifier_acces_db(clean_text)

            if nom_employe:
                status = f"AUTORISE : {nom_employe}"
                color = (0, 255, 0)
                barrier_msg = "BARRIERE OUVERTE"
                acces_valide = True
            else:
                status = f"INCONNU : {clean_text}"
                color = (0, 0, 255)
                barrier_msg = "ACCES REFUSE"

            # Dessin rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Texte plaque
            cv2.putText(frame, status, (x1, y1 - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Bandeau en haut (adapté à la largeur réelle de la vidéo)
            largeur_video = frame.shape[1]
            cv2.rectangle(frame, (0, 0), (largeur_video, 60), (0, 0, 0), -1)
            cv2.putText(frame, barrier_msg, (int(largeur_video/3), 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    # ──────────────────────────────────────────────────────────
    # 📺 AFFICHAGE
    # ──────────────────────────────────────────────────────────
    cv2.imshow("Parking", frame)

    if acces_valide:
        print("Accès confirmé. Fermeture dans 3 secondes...")
        # On force un dernier rafraîchissement pour que l'utilisateur voie le message vert
        cv2.imshow("Parking", frame)
        cv2.waitKey(3000)
        break

    # waitKey(30) permet une lecture fluide de la vidéo
    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("Programme terminé.")