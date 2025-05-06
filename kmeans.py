# -*- coding: utf-8 -*-
"""
Script de segmentation des clients d'un supermarché avec K-means.
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# ======================================================================
# Étape 1 : Chargement et exploration des données
# ======================================================================
# Lire le fichier CSV
data = pd.read_csv("donnees_clients.csv")

# Afficher les 5 premières lignes pour vérification
print("=== Aperçu des données ===")
print(data.head())

# Statistiques descriptives
print("\n=== Statistiques descriptives ===")
print(data.describe())

# ======================================================================
# Étape 2 : Prétraitement des données
# ======================================================================
# Vérifier les valeurs manquantes
print("\n=== Valeurs manquantes ===")
print(data.isnull().sum())

# Normalisation des données (K-means est sensible aux échelles)
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data[["Montant_Mensuel", "Frequence_Visites"]])

# ======================================================================
# Étape 3 : Détermination du nombre optimal de clusters (K)
# ======================================================================
# Méthode du coude (Elbow Method)
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_scaled)
    inertia.append(kmeans.inertia_)

# Visualisation de la méthode du coude
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), inertia, marker="o", linestyle="--")
plt.xlabel("Nombre de clusters (K)")
plt.ylabel("Inertie")
plt.title("Méthode du Coude pour Déterminer K Optimal")
plt.grid()
plt.show()

# ======================================================================
# Étape 4 : Application de K-means avec K=3
# ======================================================================
kmeans = KMeans(n_clusters=3, random_state=42)
data["Cluster"] = kmeans.fit_predict(data_scaled)

# Afficher les résultats par cluster
print("\n=== Résultats par Cluster ===")
print(data.groupby("Cluster").mean())

# ======================================================================
# Étape 5 : Visualisation des clusters
# ======================================================================
plt.figure(figsize=(10, 6))
plt.scatter(
    data["Frequence_Visites"],
    data["Montant_Mensuel"],
    c=data["Cluster"],
    cmap="viridis",
    s=100,
    alpha=0.7,
)
plt.xlabel("Fréquence des Visites (fois/mois)", fontsize=12)
plt.ylabel("Montant Dépensé (€)", fontsize=12)
plt.title("Segmentation des Clients avec K-means", fontsize=14)
plt.colorbar(label="Cluster")
plt.grid(True)
plt.show()

# ======================================================================
# Étape 6 : Export des résultats (optionnel)
# ======================================================================
data.to_csv("resultats_clusters.csv", index=False)
print("\n=== Résultats exportés dans 'resultats_clusters.csv' ===")