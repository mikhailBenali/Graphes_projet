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
    predecesseurs[-1].remove(sommets[-1]) # On retire omega de la liste des prédécesseurs d'omega

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

    return sommets, duree, successeurs, predecesseurs

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

    with open("E3_traces.txt", "a") as f:
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
    matrice_valeurs = [[None for i in range(len(sommets))] for j in range(len(sommets))]

    for i in range(len(sommets)):
        for j in range(len(sommets)):
            matrice_valeurs[i][j] = duree[i] if j in successeurs[i] else "*"

    return matrice_valeurs

def afficher_matrice(matrice):
    print(pd.DataFrame(matrice))
    with open("E3_traces.txt", "a") as f:
        f.write("II. Creation de la matrice des valeurs \n\n")
        f.write(pd.DataFrame(matrice).to_string())
        f.write("\n\n")

# ETAPE 3 : Vérification des propriétés pour valider le graphe d'ordonnancement

def verifier_arcs_negatifs(matrice):
    # Renvoi False s'il y a des arcs à valeurs négatives, True sinon
    # Vérifier s'il y a des arcs à valeurs négatives
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            if type(matrice[i][j]) == int: # Si l'arc contient un nombre
                if matrice[i][j] < 0: # Si la valeur de l'arc est négative
                    return False
    return True

def verifier_circuit(matrice, affichage = False):
    with open("E3_traces.txt", "a") as f:
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
        
        #Si une colonne ne contient que des * on retire la ligne et la colonne correspondante
        # On effectue ceci jusqu'à ce que la matrice soit vide ou qu'il n'y ait plus de colonne nulle
        def retirer_colonne_nulle(matrice):
            if len(matrice) == 0:
                return True
            else:
                for colonne in range(len(matrice)):
                    if all(matrice[ligne][colonne] == "*" for ligne in range(len(matrice))):
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
                            sommets.pop(colonne) # On retire le sommet de la liste des sommets
                            
                        matrice = [ligne[:colonne] + ligne[colonne+1:] for ligne in matrice] # On retire la colonne de la matrice
                        matrice = matrice[:colonne] + matrice[colonne+1:] # On retire la ligne de la matrice
                        return matrice # Si on retire une ligne et une colonne on renvoie la nouvelle matrice
                return False # Si on ne retire pas de ligne et colonne on renvoie False
        
        #Appel de la fonction retirer_colonne_nulle de manière récursive
        while type(copie_matrice) != bool:
            copie_matrice = retirer_colonne_nulle(copie_matrice)
        
        return copie_matrice

def verifier_graphe(matrice):
    with open("E3_traces.txt", "a") as f:
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

def calculer_rangs(matrice,pred):
        rangs = [0]*len(matrice)
        copie_rangs = []
        
        def rang(sommet):
            if pred[sommet] is not None:
                return max(rangs[i] for i in pred[sommet]) + 1
            else:
                return 0
        
        while rangs != copie_rangs:
            copie_rangs = rangs.copy()
            for i in range(1,len(rangs)):
                rangs[i] = rang(i)
        
        return rangs

def afficher_rangs(rangs):
    with open("E3_traces.txt", "a") as f:
        print("\n IV. Calcul du rang :\n")
        f.write("\n\nIV. Calcul du rang :\n\n")
        for i, rang in enumerate(rangs):
            print(f"Sommet {i}, rang = {rang}")
            f.write(f"Sommet {i}, rang = {rang}\n")

# ETAPE 5 : Calcul des dates au plus tôt/tard et marge

def calendrier_plus_tot(rangs, predecesseurs, duree):
    print("\n\n V. a) Calendrier au plus tot :\n")
    date_au_plus_tot = [0] * len(rangs)
    pred_date_plus_tot = {}  # Dictionnaire pour stocker les prédécesseurs à l'origine de chaque date au plus tôt

    for i in range(max(rangs) + 1):
        for j in range(len(rangs)):
            if j == 0:
                date_au_plus_tot[j] = 0
            elif rangs[j] == i:
                for k in predecesseurs[j]:
                    if date_au_plus_tot[j] <= date_au_plus_tot[k] + duree[k]:
                        date_au_plus_tot[j] = date_au_plus_tot[k] + duree[k]
                        if j in pred_date_plus_tot:
                            pred_date_plus_tot[j].append(k)  # Ajouter le prédécesseur à la liste existante
                        else:
                            pred_date_plus_tot[j] = [k]  # Créer une nouvelle liste pour les prédécesseurs

    with open("E3_traces.txt", "a") as f:
        f.write("\n\n V. a) Calendrier au plus tot :\n")

        for i, date in enumerate(date_au_plus_tot):
            print(f"Sommet {i}, date au plus tôt = {date}")
            f.write(f"\nSommet {i}, date au plus tôt = {date}")

    return date_au_plus_tot, pred_date_plus_tot


def calendrier_plus_tard(rangs, successeurs, duree, date_plus_tot):
    print("\n\n V. b) Calendrier au plus tard :\n")
    date_au_plus_tard = [9999] * len(rangs)
    pred_date_plus_tard = {}  # Dictionnaire pour stocker les prédécesseurs à l'origine de chaque date au plus tard

    for i in range(max(rangs) + 1):
        i = max(rangs) - i
        for j in range(len(rangs)):
            j = len(rangs) - j - 1
            if j == len(rangs) - 1:
                date_au_plus_tard[j] = date_plus_tot[-1]
            elif rangs[j] == i:
                for k in successeurs[j]:
                    if date_au_plus_tard[j] >= date_au_plus_tard[k] - duree[j]:
                        date_au_plus_tard[j] = date_au_plus_tard[k] - duree[j]
                        if j in pred_date_plus_tard:
                            pred_date_plus_tard[j].append(k)  # Ajouter le prédécesseur à la liste existante
                        else:
                            pred_date_plus_tard[j] = [k]  # Créer une nouvelle liste pour les prédécesseurs

    with open("E3_traces.txt", "a") as f:
        f.write("\n\n\n V. b) Calendrier au plus tard :\n")

        for i, date in enumerate(date_au_plus_tard):
            print(f"Sommet {i}, date au plus tard = {date}")
            f.write(f"\nSommet {i}, date au plus tard = {date}")

    return date_au_plus_tard, pred_date_plus_tard



def marge(date_plus_tot, date_plus_tard):

    print("\n\n V. c) Marges des sommetes:\n")
    marge = [0] * len(date_plus_tard)
    for i in range(len(date_plus_tard)):
        marge[i] = date_plus_tard[i] - date_plus_tot[i]

    with open("E3_traces.txt", "a") as f:
        f.write("\n\n\n V. c) Calendrier des marges :\n")

        for i, marge_val in enumerate(marge):
            print(f"Sommet {i}, marge = {marge_val}")
            f.write(f"\nSommet {i}, marge = {marge_val}")

def chemin_critique_recursive(sommet, pred_date_plus_tot, chemin_actuel, chemins_critiques):
    chemin_actuel.append(sommet)
    if sommet not in pred_date_plus_tot:
        chemins_critiques.append(chemin_actuel.copy())
    else:
        for pred in pred_date_plus_tot[sommet]:
            chemin_critique_recursive(pred, pred_date_plus_tot, chemin_actuel, chemins_critiques)
    chemin_actuel.pop()


def chemin_critique(pred_date_plus_tot,date_plus_tot, duree):
    chemins_critiques = []

    for sommet in pred_date_plus_tot.keys():
        if sommet not in pred_date_plus_tot.values():
            chemin_critique_recursive(sommet, pred_date_plus_tot, [], chemins_critiques)
    with open("E3_traces.txt", "a") as f:
        f.write("\n\n\n VI. Chemin(s) critique(s):\n\n")
        print("\n\n VI. Chemin(s) critique(s):\n")

        for chemin in chemins_critiques:
            if chemin[0] == len(date_plus_tot) - 1:
                if somme_durees_sommets(chemin, duree) == date_plus_tot[len(date_plus_tot) - 1]:
                    inverse_chemin = list(reversed(chemin))
                    format_chemin = ' -> '.join(map(str, inverse_chemin))
                    print(format_chemin)
                    f.write(format_chemin+"\n")

    return chemins_critiques

def somme_durees_sommets(liste_sommets, duree):
    somme_durees = 0
    for sommet in liste_sommets:
        somme_durees += duree[sommet]
    return somme_durees

def decoration_affichage(message):
    print("\n" + "#"*50 + "\n")
    print(message)
