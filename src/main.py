from fonction import *
 
while True:
    decoration_affichage("MENU PRINCIPAL :")
    print("1. Tester un tableau de contrainte")
    print("2. Quitter")

    choix = input("Entrez votre choix : ")

    if choix == "1":
        num_graphe = int(input("Entrer le n° de tableau de contrainte à tester (entre 1 et 14) : "))
        if 1 <= num_graphe <= 14:
            decoration_affichage(f"Calculs sur le graphe {num_graphe}: \n")
            file_name = f'graphes/table {num_graphe}.txt'
            sommets, duree, successeurs = lire_fichier_contraintes(file_name)
            afficher_graphe(sommets, successeurs, duree)
            matrice_valeurs = creer_matrice_valeurs(sommets, successeurs, duree)
            afficher_matrice(matrice_valeurs)
            if verifier_graphe(matrice_valeurs):
                rangs = calculer_rangs(matrice_valeurs)
                afficher_rangs(rangs)
        else:
            print("Numéro de table invalide. Veuillez entrer un numéro entre 1 et 14.")
    elif choix == "2":
        print("Au revoir !")
        break
    else:
        print("Choix invalide. Veuillez entrer 1 ou 2.")
