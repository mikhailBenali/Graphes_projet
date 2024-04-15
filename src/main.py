import pandas as pd

# ETAPE 1 : Lecture du fichier et stockage des données

def lire_fichier_contraintes(file_name):
    sommets, duree, predecesseurs = [], [], []

    with open('graphes/test.txt', 'r') as f:
        for ligne in f:
            ligne = ligne.replace("\n", "")
            ligne = ligne.split(" ")
            sommets.append(int(ligne[0]))
            duree.append(int(ligne[1]))
            if ligne[2:] == []:
                predecesseurs.append([0])
            else:
                predecesseurs.append([int(i) for i in ligne[2:]])

    # Ajout d'alpha
    sommets.insert(0, 0) 
    duree.insert(0, 0)
    predecesseurs.insert(0, None)
    # Ajout d'omega
    sommets.append(sommets[-1]+1)
    duree.append(0)

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

    # Affichage des données stockées
    print(f"Sommets: {sommets}")
    print(f"Durée: {duree}")
    print(f"Prédécesseurs: {predecesseurs}")
    print(f"Successeurs: {successeurs}\n")

    return sommets, duree, predecesseurs, successeurs

# Etape 2 : Affichage du graphe d'ordonnancement
def afficher_graphe(sommets, successeurs, duree):
    print("I. Graphe d'ordonnancement : \n")
    nb_sommets = len(sommets)
    nb_arcs = sum(len(succ) for succ in successeurs[:-1]) # On exclut le dernier sommet (oméga n'a pas de sucesseur)
    print(f"Nombre de sommets : {nb_sommets}")
    print(f"Nombre d'arcs : {nb_arcs}")

    for i in range(len(successeurs)):
        for succ in successeurs[i]:
            print(f"{i} -> {succ} = {duree[i]}")


# ETAPE 2 : Création de la matrice des valeurs
def creer_matrice_valeurs(sommets, successeurs, duree):
    print("\nII. Création de la matrice des valeurs \n")

    # On initialise la matrice à -1 en ajoutant 2 sommets pour alpha et omega
    matrice_adjacence = [[-1 for i in range(len(sommets))] for j in range(len(sommets))]

    for i in range(len(sommets)):
        for j in range(len(sommets)):
            matrice_adjacence[i][j] = duree[i] if j in successeurs[i] else -1

    def afficher_matrice(matrice):
            print(pd.DataFrame(matrice))

    afficher_matrice(matrice_adjacence)

    return matrice_adjacence

# ETAPE 3 : Vérification des propriétés pour valider le graphe d'ordonnancement
""" 

"""

# ETAPE 4 : Calcul des rangs des sommets à partir de la matrice des valeurs

def calculer_rangs(matrice):
    nb_sommets = len(matrice)
    rangs = [0] * nb_sommets

    while True:
        anciens_rangs = rangs.copy()

        for i in range(nb_sommets):
            # Si le sommet i a des prédécesseurs
            if any(matrice[j][i] != -1 for j in range(nb_sommets)):
                rangs[i] = max(rangs[j] + 1 for j in range(nb_sommets) if matrice[j][i] != -1)

        # Vérifier s'il y a eu un changement dans les rangs
        if rangs == anciens_rangs:
            break

    return rangs

def afficher_rangs(rangs):
    print("\n IV. Calcul du rang :\n")
    for i, rang in enumerate(rangs):
        print(f"Sommet {i}, rang = {rang}")
    
# MAIN : Exécution des fonctions :

if __name__ == "__main__":
    file_name = 'graphes/test.txt'
    sommets, duree, predecesseurs, successeurs = lire_fichier_contraintes(file_name)
    afficher_graphe(sommets, successeurs, duree)
    matrice_adjacence = creer_matrice_valeurs(sommets, successeurs, duree)
    rangs = calculer_rangs(matrice_adjacence)
    afficher_rangs(rangs)