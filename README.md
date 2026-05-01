# 🚗 Detection-Plaques-Parking

> Système intelligent de contrôle d'accès à un parking par reconnaissance automatique de plaques d'immatriculation — **Filière ADIA**

---

## 👥 Réalisé par

| Nom | Filière |
|-----|---------|
| Fatima Tildi | ADIA |
| Ichraq Majid | ADIA |
| Abdessamad Rekhami | ADIA |

---

## 📌 Description du projet

Ce projet implémente un **système de contrôle d'accès automatique** pour un parking, basé sur la reconnaissance des plaques d'immatriculation en temps réel.

Le système détecte la plaque d'un véhicule via une caméra, lit les caractères grâce à l'OCR, puis vérifie si le véhicule est autorisé en consultant une base de données d'employés. Si la plaque est reconnue, la barrière s'ouvre automatiquement.

---

## 🛠️ Technologies utilisées

| Outil | Rôle |
|-------|------|
| **YOLOv8** | Détection de la plaque dans l'image |
| **EasyOCR** | Lecture des caractères de la plaque |
| **OpenCV** | Capture et affichage vidéo |
| **SQLite** | Base de données des employés autorisés |
| **Python** | Langage principal |

---

## 📁 Structure du projet

```
Detection-Plaques-Parking/
│
├── SCRIPT.py              # Contrôle d'accès en temps réel (webcam)
├── SCRIPT2_VIDEO.py       # Contrôle d'accès sur vidéo préenregistrée
├── parking.py             # Création de la base de données SQLite
├── ajouter_employee.py    # Ajout d'un employé dans la base de données
├── best.pt                # Modèle YOLOv8 entraîné sur les plaques
├── Yolo_Training.ipynb    # Notebook d'entraînement du modèle YOLO
└── README.md
```

---

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/fatimatil/Detection-Plaques-Parking.git
cd Detection-Plaques-Parking
```

### 2. Installer les dépendances
```bash
pip install ultralytics easyocr opencv-python
```

### 3. Créer la base de données
```bash
python parking.py
```

### 4. Ajouter des employés autorisés
```bash
python ajouter_employee.py
```

---

## ▶️ Utilisation

### Mode webcam (temps réel)
```bash
python SCRIPT.py
```

### Mode vidéo
```bash
python SCRIPT2_VIDEO.py
```

> Le système affiche en vert **"BARRIERE OUVERTE"** si la plaque est reconnue, en rouge **"ACCES REFUSE"** sinon.

---

## 🔄 Fonctionnement

```
Caméra → Détection YOLO → Extraction ROI → OCR EasyOCR → Vérification SQLite → Résultat
```

1. La caméra capture le flux vidéo en temps réel
2. YOLOv8 détecte et localise la plaque dans l'image
3. EasyOCR lit les caractères alphanumériques de la plaque
4. La plaque est comparée à la base de données des employés
5. Le résultat est affiché avec un retour visuel coloré

---

## 📊 Performances du modèle

| Métrique | Valeur |
|----------|--------|
| mAP@0.5 | 0.87 |
| Précision | 0.84 |
| Rappel | 0.91 |
| FPS (GPU) | ~27 FPS |
| FPS (CPU) | ~5 FPS |

---

## 📄 Licence

Projet académique — Filière ADIA — 2025
