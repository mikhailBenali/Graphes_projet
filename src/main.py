import pandas as pd

sommets, longueurs, predecesseurs = [], [], []
# Lecture du fichier et stockage des données

with open('graphes/test.txt', 'r') as f:
    for ligne in f:
        ligne = ligne.replace("\n", "")
        ligne = ligne.split(" ")
        sommets.append(int(ligne[0]))
        longueurs.append(int(ligne[1]))
        if ligne[2:] == []:
            predecesseurs.append([0])
        else:
            predecesseurs.append([int(i) for i in ligne[2:]])

# Ajout d'alpha
sommets.insert(0, 0) 
longueurs.insert(0, 0)
predecesseurs.insert(0, None)
# Ajout d'omega
sommets.append(sommets[-1]+1)
longueurs.append(0)

allpreds = [] # Liste de tous les sommets étant prédécesseurs
for i in range(len(predecesseurs)):
    if predecesseurs[i] is not None:
        for elt in predecesseurs[i]:
            allpreds.append(elt)
allpreds = set(allpreds)

predecesseurs.append([i for i in sommets if i not in allpreds])

successeurs = [[] for i in range(len(sommets))]

for i in range(1,len(predecesseurs)):
    for elt in predecesseurs[i]:
        successeurs[elt].append(i)
successeurs[-1] = [] # Omega n'a pas de successeur

"""
"""

print(f"Sommets: {sommets}")
print(f"Longueurs: {longueurs}")
print(f"Prédécesseurs: {predecesseurs}")
print(f"Successeurs: {successeurs}")
# Création de la matrice des valeurs

# On initialise la matrice à -1 en ajoutant 2 sommets pour alpha et omega

matrice_adjacence = [[-1 for i in range(len(sommets))] for j in range(len(sommets))]

for i in range(len(sommets)):
    for j in range(len(sommets)):
        matrice_adjacence[i][j] = longueurs[i] if j in successeurs[i] else -1

def afficher_matrice(matrice):
        print(pd.DataFrame(matrice))

afficher_matrice(matrice_adjacence)