import pandas as pd
import os, os.path

# ETAPE 1 : Lecture du fichier et stockage des données

def lire_fichier_contraintes(file_name):
    sommets, duree, predecesseurs = [], [], []

    with open(file_name, 'r') as f:
        for ligne in f:
            ligne = ligne.replace("\n", "")
            ligne = ligne.strip()
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

    # Affichage des données stockées (test)
    """print(f"Sommets: {sommets}")
    print(f"Durée: {duree}")
    print(f"Prédécesseurs: {predecesseurs}")
    print(f"Successeurs: {successeurs}\n")"""

    return sommets, duree, successeurs

# Etape 2 : Affichage du graphe d'ordonnancement
def afficher_graphe(sommets, successeurs, duree):
    print("I. Graphe d'ordonnancement : \n\n")
    nb_sommets = len(sommets)
    nb_arcs = sum(len(succ) for succ in successeurs[:-1]) # On exclut le dernier sommet (oméga n'a pas de sucesseur)
    print(f"Nombre de sommets : {nb_sommets}")
    print(f"Nombre d'arcs : {nb_arcs}")

    for i in range(len(successeurs)):
        for succ in successeurs[i]:
            print(f"{i} -> {succ} = {duree[i]}")

    # TRACE

    with open("traces.txt", "a") as f:
        f.write("\nI. Graphe d'ordonnancement : \n\n")
        f.write(f"Nombre de sommets : {nb_sommets}\n")
        f.write(f"Nombre d'arcs : {nb_arcs}\n")
        for i in range(len(successeurs)):
            for succ in successeurs[i]:
                f.write(f"{i} -> {succ} = {duree[i]}\n")
        f.write("\n\n")


# ETAPE 2 : Création de la matrice des valeurs
def creer_matrice_valeurs(sommets, successeurs, duree):
    print("\nII. Création de la matrice des valeurs \n\n")

    # On initialise la matrice à -1 en ajoutant 2 sommets pour alpha et omega
    matrice_valeurs = [[-1 for i in range(len(sommets))] for j in range(len(sommets))]

    for i in range(len(sommets)):
        for j in range(len(sommets)):
            matrice_valeurs[i][j] = duree[i] if j in successeurs[i] else -1

    return matrice_valeurs

def afficher_matrice(matrice):
    print(pd.DataFrame(matrice))
    with open("traces.txt", "a") as f:
        f.write("II. Creation de la matrice des valeurs \n\n")
        f.write(pd.DataFrame(matrice).to_string())
        f.write("\n\n")

# ETAPE 3 : Vérification des propriétés pour valider le graphe d'ordonnancement

def verifier_arcs_negatifs(matrice):
    # Renvoi False s'il y a des arcs à valeurs négatives, True sinon
    # Vérifier s'il y a des arcs à valeurs négatives
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if matrice[i][j] < -1: # S'il y a une valeur inférieure à -1
                return False # Il y a un arc à valeur négative
    return True

def verifier_circuit(matrice, affichage = False):
    with open("traces.txt", "a") as f:
        if affichage:
            f.write("\nIII. Verification des proprietes du graphe d'ordonnancement : \n\n")
        
        # Renvoie True s'il n'y a pas de circuit, False s'il y en a un
        copie_matrice = matrice.copy()
        if affichage:
            print("Détection de circuit :")
            print("Méhode d'élimination des points d'entrée: ")
            
            f.write("Detection de circuit : \n\n")
            f.write("Methode d'elimination des points d'entree: \n")
        
        sommets = [i for i in range(len(copie_matrice))]
        
        #Si une colonne ne contient que des -1 on retire la ligne et la colonne correspondante
        # On effectue ceci jusqu'à ce que la matrice soit vide ou qu'il n'y ait plus de colonne nulle
        def retirer_colonne_nulle(matrice):
            if len(matrice) == 0:
                return True
            else:
                for colonne in range(len(matrice)):
                    if all(matrice[ligne][colonne] == -1 for ligne in range(len(matrice))):
                        
                        if affichage:
                            print(f"Point d'entrée : {sommets[colonne]}")
                            f.write(f"Point d'entree : {sommets[colonne]}\n")
                            sommets.pop(colonne)
                            if sommets != []:
                                print(f"Sommets restants : ",end="")
                                f.write("Sommets restants : ")
                                for sommet in sommets:
                                    print(sommet, end=" ")
                                    f.write(f"{sommet} ")
                                print("\n")
                                f.write("\n")
                            else:
                                print("\nIl n'y a plus aucun sommets restants\n")
                                f.write("\nIl n'y a plus aucun sommets restants\n")
                        else:
                            sommets.pop(colonne)
                            
                        matrice = [ligne[:colonne] + ligne[colonne+1:] for ligne in matrice] # On retire la colonne
                        matrice = matrice[:colonne] + matrice[colonne+1:] # On retire la ligne
                        return matrice # Si on retire une ligne et une colonne on renvoie la nouvelle matrice
                return False # Si on ne retire pas de ligne et colonne on renvoie la matrice telle quelle
        
        #Appel de la fonction retirer_colonne_nulle de manière récursive
        while type(copie_matrice) != bool:
            copie_matrice = retirer_colonne_nulle(copie_matrice)
        
        return copie_matrice

def verifier_graphe(matrice):
    with open("traces.txt", "a") as f:
        print("\nIII. Vérification des propriétés du graphe d'ordonnancement : \n")
        
        if not verifier_arcs_negatifs(matrice):
            print("Le graphe d'ordonnancement contient des arcs à valeurs négatives.")
            f.write("\nLe graphe d'ordonnancement contient des arcs a valeurs negatives.\n")
        else:
            print("Le graphe d'ordonnancement ne contient pas d'arcs à valeurs négatives.")
            f.write("\nLe graphe d'ordonnancement ne contient pas d'arcs a valeurs negatives.\n")
        
        if not verifier_circuit(matrice,affichage=True):
            print("Le graphe d'ordonnancement contient un circuit.")
            f.write("\nLe graphe d'ordonnancement contient un circuit.\n")
        else:
            print("Le graphe d'ordonnancement ne contient pas de circuit.")
            f.write("\nLe graphe d'ordonnancement ne contient pas de circuit.\n")
        
        if verifier_arcs_negatifs(matrice) and verifier_circuit(matrice):
            return True # On peut continuer

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
        if rangs != anciens_rangs:
            break
    return rangs

def afficher_rangs(rangs):
    with open("traces.txt", "a") as f:
        print("\n IV. Calcul du rang :\n")
        f.write("\nIV. Calcul du rang :\n\n")
        for i, rang in enumerate(rangs):
            print(f"Sommet {i}, rang = {rang}")
            f.write(f"Sommet {i}, rang = {rang}\n")

def decoration_affichage(message):
    print("\n" + "#"*50 + "\n")
    print(message)
