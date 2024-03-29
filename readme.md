# Projet d'ordonnancement

---
**Consignes:** 

Fonctions à mettre en oeuvre (pour avoir au moins 10, il faut que les points 1-4 soient opérationnels)
Déroulement du programme
Mettre en place un programme qui exécute les actions suivantes préalables à l’ordonnancement :
1. Lecture d’un tableau de contraintes donné dans un fichier texte ( .txt) et stockage en mémoire
2. Affichage du graphe correspondant sous forme matricielle (matrice des valeurs). Attention : cet affichage doit se faire à partir du contenu mémoire, et non pas directement en lisant le fichier. Ce graphe doit incorporer les deux sommets fictifs alpha et omega (notés 0 et N+1 où N est le nombre de tâches).
3. Vérification des propriétés nécessaires du graphe pour qu’il puisse servir d’un graphe d’ordonnancement :
- pas de circuit, - pas d’arcs à valeur négative. Si la réponse à la question 3 est « Oui », procéder au calcul des calendriers :
4. Calculer les rangs de tous les sommets du graphe.
5. Calculer le calendrier au plus tôt, le calendrier au plus tard et les marges.
Pour le calcul du calendrier au plus tard, considérez que la date au plus tard de fin de projet est égale à sa date au plus tôt.
6. Calculer le(s) chemin(s) critique(s) et les afficher