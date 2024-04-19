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

    # Affichage des données stockées
    print(f"Sommets: {sommets}")
    print(f"Durée: {duree}")
    print(f"Prédécesseurs: {predecesseurs}")
    print(f"Successeurs: {successeurs}\n")

    return sommets, duree, successeurs, predecesseurs

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
    matrice_valeurs = [[-1 for i in range(len(sommets))] for j in range(len(sommets))]

    for i in range(len(sommets)):
        for j in range(len(sommets)):
            matrice_valeurs[i][j] = duree[i] if j in successeurs[i] else -1

    return matrice_valeurs

def afficher_matrice(matrice):
            print(pd.DataFrame(matrice))

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
    # Renvoie True s'il n'y a pas de circuit, False s'il y en a un
    copie_matrice = matrice.copy()
    if affichage:
        print("Détection de circuit :")
        print("Méhode d'élimination des points d'entrée: ")
    
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
                        sommets.pop(colonne)
                        if sommets != []:
                            print(f"Sommets restants : ",end="")
                            for sommet in sommets:
                                print(sommet, end=" ")
                            print("\n")
                        else:
                            print("\nIl n'y a plus aucun sommets restants\n")
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
    print("\nIII. Vérification des propriétés du graphe d'ordonnancement : \n")
    
    if not verifier_arcs_negatifs(matrice):
        print("Le graphe d'ordonnancement contient des arcs à valeurs négatives.")
    else:
        print("Le graphe d'ordonnancement ne contient pas d'arcs à valeurs négatives.")
    
    if not verifier_circuit(matrice,affichage=True):
        print("Le graphe d'ordonnancement contient un circuit.")
    else:
        print("Le graphe d'ordonnancement ne contient pas de circuit.")
    
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
    print("\n IV. Calcul du rang :\n")
    for i, rang in enumerate(rangs):
        print(f"Sommet {i}, rang = {rang}")

# ETAPE 5 : Calcul des dates au plus tôt/tard et marge

def calendrier_plus_tot(rangs,predecesseurs,duree) :
    print("\n V. a) Calendrier au plus tot :\n")
    date_au_plus_tot=[0]*len(rangs)
    for i in range(max(rangs)+1) :
        for j in range(len(rangs)) :
            if j==0 :
                date_au_plus_tot[j]=0
            else :
                if rangs[j]==i :
                        for k in predecesseurs[j]:
                            #k = prédecesseurs de j
                            if (date_au_plus_tot[j] <= date_au_plus_tot[k]+duree[k]) :
                                date_au_plus_tot[j] = date_au_plus_tot[k]+duree[k]
    for i, date in enumerate(date_au_plus_tot):
        print(f"Sommet {i}, date au plus tôt = {date}")
    return(date_au_plus_tot)

def calendrier_plus_tard(rangs,successeurs,duree,date_plus_tot) :
    print("\n V. b) Calendrier au plus tard :\n")
    date_au_plus_tard=[9999]*len(rangs)
    for i in range(max(rangs)+1) :
        i = max(rangs)-i
        for j in range(len(rangs)) :
            j= len(rangs)-j-1
            if j==len(rangs)-1 :
                date_au_plus_tard[j]=date_plus_tot[-1]
            else :
                if rangs[j]==i :
                        for k in successeurs[j]:
                            #k = successeurs de j
                            if (date_au_plus_tard[j] >= date_au_plus_tard[k]-duree[j]) :
                                date_au_plus_tard[j] = date_au_plus_tard[k]-duree[j]
    for i, date in enumerate(date_au_plus_tard):
        print(f"Sommet {i}, date au plus tard = {date}")

    return(date_au_plus_tard)

def marge(date_plus_tot,date_plus_tard):
    print("\n V. c) Calendrier au plus tot :\n")
    marge=[0]*len(date_plus_tard)
    for i in range(len(date_plus_tard)):
        marge[i]=date_plus_tard[i]-date_plus_tot[i]
    for i, marge in enumerate(marge):
        print(f"Sommet {i}, marge = {marge}")

def decoration_affichage(message):
    print("\n" + "#"*50 + "\n")
    print(message)
