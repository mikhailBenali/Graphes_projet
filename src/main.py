import os

file_folder = os.getcwd()
graphes_folder = file_folder + "\\graphes\\"

sommets = []
durees = []
contraintes = []

with open(graphes_folder + "test.txt", "r") as file:
    for line in file:

        # Traitement de la ligne et stockage en mémoire
        line = line.split(" ")
        line[-1] = line[-1].replace("\n", "") #On retire les \n
        sommets.append(line[0]) #On ajoute les sommets
        durees.append(line[1]) #On ajoute les durées
        contraintes.append(line[2:]) #On ajoute les contraintes

print(sommets)
print(durees)
print(contraintes)


