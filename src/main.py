sommets, arretes, predecesseurs = [], [], []

# Lecture du fichier et stockage des données

with open('graphes/test.txt', 'r') as f:
    for ligne in f:
        ligne = ligne.replace("\n", "")
        ligne = ligne.split(" ")
        sommets.append(ligne[0])
        arretes.append(ligne[1])
        predecesseurs.append(ligne[2:])

# Création de la matrice des valeurs

matrice_adjacence = [[-1 for i in range(len(sommets)+2)] for j in range(len(sommets)+2)] # On initialise la matrice à -1 en ajoutant 2 sommets pour alpha et omega


def afficher_matrice(matrice):
        for ligne in matrice:
            print(ligne)

