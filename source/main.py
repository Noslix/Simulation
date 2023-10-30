#import Simulation
import GeneticAlgo
import matplotlib.pyplot as plt

'''
# Lecture des valeurs de l'action depuis un fichier
actions = []
with open('donnees_random.txt', 'r') as file:
    for line in file:
        actions.append(float(line.strip()))  # Convertir les valeurs en float et les ajouter à la liste
'''
'''
vente_deficitMax = 0.1  # 10% de perte maximale
vente_gainMax = 0.01  # 15% de profit avant revente
achat_delta = 10 # Temps en Heure prise en compte
achat_diffA = 10 #% de Baisse
achat_diffB = 10 #% de Rehausse 
'''

#final_portefeuille, portefeuille_history = Simulation.simulate_trading(actions, 10, -3, 6, vente_deficitMax, vente_gainMax, 10)

actions = 'AAPL'
nb_generation = 100
Population_taille = 50



#Faire en sorte que le action fasse un appel au lieu de garder toutes les données dans la variable
GeneticAlgo.demarrage(actions, nb_generation, Population_taille)

# Sauvegarder la courbe dans un fichier
#plt.savefig('solde_evolution.png')

# Afficher la courbe
#plt.show()