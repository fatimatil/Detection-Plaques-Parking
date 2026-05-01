import cv2
import numpy as np
import easyocr
from ultralytics import YOLO
import sqlite3
import time


print("Système prêt. Connexion à la base de données...")
yolo_model = YOLO('best.pt')
reader = easyocr.Reader(['en'])

def clean_plate_text(text):
    return "".join([c for c in text if c.isalnum()]).upper()

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

# --- 2. LECTURE VIDÉO ---
cap = cv2.VideoCapture(0)
acces_valide = False # Variable pour contrôler la fermeture

while True:
    ret, frame = cap.read()
    if not ret: break

    results = yolo_model(frame, stream=True)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            plate_roi = frame[y1:y2, x1:x2]
            
            if plate_roi.size == 0: continue

            ocr_results = reader.readtext(plate_roi, detail=0)
            raw_text = "".join(ocr_results)
            clean_text = clean_plate_text(raw_text)

            nom_employe = verifier_acces_db(clean_text)

            if nom_employe:
                status = f"AUTORISE : {nom_employe}"
                color = (0, 255, 0)
                barrier_msg = "BARRIERE OUVERTE"
                acces_valide = True # On marque l'accès comme validé
            else:
                status = f"INCONNU : {clean_text}"
                color = (0, 0, 255)
                barrier_msg = "ACCES REFUSE"

            # Dessin des infos
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, status, (x1, y1 - 15), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.rectangle(frame, (0, 0), (640, 50), (0, 0, 0), -1)
            cv2.putText(frame, barrier_msg, (150, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.imshow("Controle Acces Parking - Mode SQLite Direct", frame)

    if acces_valide:
        print(f"Accès confirmé. Fermeture dans 3 secondes...")
        cv2.waitKey(3000) # Attendre 3000ms (3 secondes) pour que l'employé voie le message
        break # Sortir de la boucle while et fermer la fenêtre

    if cv2.waitKey(1) == 27: break

cap.release()
cv2.destroyAllWindows()
print("Programme terminé et barrière actionnée.")