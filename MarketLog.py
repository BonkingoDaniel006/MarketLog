import sys, os
import tkinter as tk
from PIL import Image, ImageTk
import csv

# -------------------------
# Fonction pour PyInstaller
# -------------------------
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# -------------------------
# Données (valeurs par défaut si pas de CSV)
# -------------------------
produits = [
    {"code": "AV26022026", "nom": "AVOCAT", "prix": 1500, "stock": 350},
    {"code": "MG13052003", "nom": "MANGUE", "prix": 500, "stock": 433},
    {"code": "BB16062009", "nom": "BANANE", "prix": 700, "stock": 628},
    {"code": "PO26022006", "nom": "POMME", "prix": 500, "stock": 150},
    {"code": "OR24041972", "nom": "ORANGE", "prix": 650, "stock": 212},
]

# -------------------------
# Gestion CSV
# -------------------------
def charger_produits():
    if not os.path.exists("produits.csv"):
        sauvegarder_produits()
        return

    produits.clear()
    with open("produits.csv", "r", newline="", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        for ligne in lecteur:
            produits.append({
                "code": ligne["code"],
                "nom": ligne["nom"],
                "prix": int(ligne["prix"]),
                "stock": int(ligne["stock"])
            })

def sauvegarder_produits():
    with open("produits.csv", "w", newline="", encoding="utf-8") as f:
        champs = ["code", "nom", "prix", "stock"]
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        for p in produits:
            writer.writerow(p)

# -------------------------
# Application
# -------------------------
root = tk.Tk()
root.title("MarketLog")
root.geometry("800x600")

# -------------------------
# Image de fond
# -------------------------
img = Image.open(resource_path("Background.jpg"))
bg = ImageTk.PhotoImage(img)

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")

color = "#A7D3E8"
# -------------------------
# Gestion des écrans
# -------------------------
frames = {}

def afficher_frame(nom):
    """Affiche un écran et cache les autres."""
    for f in frames.values():
        f.place_forget()
    frames[nom].place(x=50, y=400)

# -------------------------
# Menu principal
# -------------------------
def creer_menu_principal():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["menu"] = frame

    tk.Label(frame, text="Bonjour, quelle opération souhaitez-vous effectuer ?",
             font=("Arial", 12), fg="white", bg=color).pack(pady=10)

    tk.Button(frame, text="1. Vendre un produit", font=("Arial", 12),
              command=lambda: afficher_frame("vente_code")).pack(pady=5)

    tk.Button(frame, text="2. Réapprovisionner un stock", font=("Arial", 12),
              command=lambda: afficher_frame("ajout_code")).pack(pady=5)

    tk.Button(frame, text="3. Voir le stock disponible", font=("Arial", 12),
              command=lambda: afficher_frame("stock")).pack(pady=5)

    tk.Button(frame, text="4. Voir le prix d'un produit", font=("Arial", 12),
              command=lambda: afficher_frame("prix_code")).pack(pady=5)

    tk.Button(frame, text="5. Quitter", font=("Arial", 12),
              command=root.quit).pack(pady=5)

# -------------------------
# Ajout produit : Code
# -------------------------
def creer_ecran_code():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["ajout_code"] = frame

    tk.Label(frame, text="Entrez le code du produit :", font=("Arial", 12),
             fg="white", bg=color).pack(pady=10)

    entry = tk.Entry(frame)
    entry.pack()

    def valider():
        code = entry.get().strip()
        if code == "":
            return
        nouveau_produit["code"] = code
        afficher_frame("ajout_nom")

    tk.Button(frame, text="Valider", command=valider).pack(pady=20)
    tk.Button(frame, text="Retour", command=lambda: afficher_frame("menu")).pack()

# -------------------------
# Ajout produit : Nom
# -------------------------
def creer_ecran_nom():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["ajout_nom"] = frame

    tk.Label(frame, text="Entrez le nom du produit :", font=("Arial", 12),
             fg="white", bg=color).pack(pady=10)

    entry = tk.Entry(frame)
    entry.pack()

    def valider():
        nom = entry.get().strip()
        if nom == "":
            return
        nouveau_produit["nom"] = nom
        afficher_frame("ajout_prix")

    tk.Button(frame, text="Valider", command=valider).pack(pady=20)

# -------------------------
# Ajout produit : Prix
# -------------------------
def creer_ecran_prix():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["ajout_prix"] = frame

    tk.Label(frame, text="Prix du produit (FC) :", font=("Arial", 12),
             fg="white", bg=color).pack(pady=10)

    entry = tk.Entry(frame)
    entry.pack()

    def valider():
        try:
            prix = int(entry.get())
        except:
            return
        nouveau_produit["prix"] = prix
        afficher_frame("ajout_stock")

    tk.Button(frame, text="Valider", command=valider).pack(pady=20)

# -------------------------
# Ajout produit : Stock
# -------------------------
def creer_ecran_stock_ajout():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["ajout_stock"] = frame

    tk.Label(frame, text="Quantité en stock :", font=("Arial", 12),
             fg="white", bg=color).pack(pady=10)

    entry = tk.Entry(frame)
    entry.pack()

    def valider():
        try:
            stock = int(entry.get())
        except:
            return
        nouveau_produit["stock"] = stock
        produits.append(nouveau_produit.copy())
        sauvegarder_produits()
        afficher_frame("confirmation")

    tk.Button(frame, text="Valider", command=valider).pack(pady=20)

# -------------------------
# Ajout produit : Confirmation
# -------------------------
def creer_ecran_confirmation():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["confirmation"] = frame

    tk.Label(frame, text="Produit ajouté avec succès !",
             font=("Arial", 14), fg="white", bg=color).pack(pady=20)

    tk.Button(frame, text="Retour au menu",
              command=lambda: afficher_frame("menu")).pack()

# ============================================================
# =====================  VENTE PRODUIT  =======================
# ============================================================

def creer_ecran_vente_code():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["vente_code"] = frame

    tk.Label(frame, text="Code du produit à vendre :", font=("Arial", 12),
             fg="white", bg=color).pack(pady=10)

    entry = tk.Entry(frame)
    entry.pack()

    def valider():
        code = entry.get().strip()
        if code == "":
            return

        for p in produits:
            if p["code"] == code:
                vente_produit["produit"] = p
                afficher_frame("vente_quantite")
                return

        tk.Label(frame, text="Code introuvable !", fg="red", bg=color).pack()

    tk.Button(frame, text="Valider", command=valider).pack(pady=20)
    tk.Button(frame, text="Retour", command=lambda: afficher_frame("menu")).pack()

def creer_ecran_vente_quantite():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["vente_quantite"] = frame

    tk.Label(frame, text="Quantité à vendre :", font=("Arial", 12),
             fg="white", bg=color).pack(pady=10)

    entry = tk.Entry(frame)
    entry.pack()

    def valider():
        try:
            qte = int(entry.get())
        except:
            return

        produit = vente_produit["produit"]

        if qte > produit["stock"]:
            tk.Label(frame, text="Stock insuffisant !", fg="red", bg=color).pack()
            return

        produit["stock"] -= qte
        sauvegarder_produits()
        afficher_frame("vente_confirmation")

    tk.Button(frame, text="Valider", command=valider).pack(pady=20)

def creer_ecran_vente_confirmation():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["vente_confirmation"] = frame

    tk.Label(frame, text="Vente effectuée avec succès !",
             font=("Arial", 14), fg="white", bg=color).pack(pady=20)

    tk.Button(frame, text="Retour au menu",
              command=lambda: afficher_frame("menu")).pack()

# ============================================================
# =====================  VOIR LE STOCK  =======================
# ============================================================

def creer_ecran_stock():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["stock"] = frame

    def rafraichir(event=None):
        for widget in frame.winfo_children():
            widget.destroy()

        tk.Label(frame, text="Stock disponible :", font=("Arial", 14),
                 fg="white", bg=color).pack(pady=10)

        zone = tk.Frame(frame, bg="white")
        zone.pack(pady=10)

        for p in produits:
            ligne = f"{p['code']} - {p['nom']} | Prix: {p['prix']} FC | Stock: {p['stock']}"
            tk.Label(zone, text=ligne, font=("Arial", 11), bg="white").pack(anchor="w")

        tk.Button(frame, text="Retour au menu",
                  command=lambda: afficher_frame("menu")).pack(pady=20)

    frame.bind("<Visibility>", rafraichir)

# ============================================================
# =====================  VOIR LE PRIX  ========================
# ============================================================

def creer_ecran_prix_code():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["prix_code"] = frame

    tk.Label(frame, text="Entrez le code du produit :", font=("Arial", 12),
             fg="white", bg=color).pack(pady=10)

    entry = tk.Entry(frame)
    entry.pack()

    def valider():
        code = entry.get().strip()
        if code == "":
            return

        for p in produits:
            if p["code"] == code:
                prix_produit["produit"] = p
                afficher_frame("prix_affichage")
                return

        tk.Label(frame, text="Produit introuvable !", fg="red", bg=color).pack()

    tk.Button(frame, text="Valider", command=valider).pack(pady=20)
    tk.Button(frame, text="Retour", command=lambda: afficher_frame("menu")).pack()

def creer_ecran_prix_affichage():
    frame = tk.Frame(root, bg=color, width=400, height=500)
    frames["prix_affichage"] = frame

    def rafraichir(event=None):
        for widget in frame.winfo_children():
            widget.destroy()

        p = prix_produit.get("produit")

        if p:
            texte = f"Produit : {p['nom']}\nPrix : {p['prix']} FC"
        else:
            texte = "Aucun produit sélectionné."

        tk.Label(frame, text=texte, font=("Arial", 14),
                 fg="white", bg=color).pack(pady=20)

        tk.Button(frame, text="Retour au menu",
                  command=lambda: afficher_frame("menu")).pack()

    frame.bind("<Visibility>", rafraichir)

# -------------------------
# Initialisation
# -------------------------
nouveau_produit = {}
vente_produit = {}
prix_produit = {}

# Charger les produits depuis le CSV (ou créer le CSV si absent)
charger_produits()

creer_menu_principal()
creer_ecran_code()
creer_ecran_nom()
creer_ecran_prix()
creer_ecran_stock_ajout()
creer_ecran_confirmation()

creer_ecran_vente_code()
creer_ecran_vente_quantite()
creer_ecran_vente_confirmation()

creer_ecran_stock()

creer_ecran_prix_code()
creer_ecran_prix_affichage()

afficher_frame("menu")

root.mainloop()