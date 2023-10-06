#import Simulation
import GeneticAlgo
import matplotlib.pyplot as plt


'''
vente_deficitMax = 0.1  # 10% de perte maximale
vente_gainMax = 0.01  # 15% de profit avant revente
achat_delta = 10 # Temps en Heure prise en compte
achat_diffA = 10 #% de Baisse
achat_diffB = 10 #% de Rehausse 
'''

#final_portefeuille, portefeuille_history = Simulation.simulate_trading(actions, 10, -3, 6, vente_deficitMax, vente_gainMax, 10)

nom_action = "BTC"

GeneticAlgo.demarrage(nom_action, 1, 10)

'''
# Afficher la courbe de l'évolution du solde
#plt.plot(range(len(actions)), actions, label='Bourse', color='blue')
plt.plot(range(len(portefeuille_history)), portefeuille_history, label='actions_detenues', color='red')
plt.xlabel('Jours')
plt.ylabel('Solde')
plt.title('Évolution du solde au fil du temps')
plt.grid(True)
'''

# Sauvegarder la courbe dans un fichier
#plt.savefig('solde_evolution.png')

# Afficher la courbe
plt.show()