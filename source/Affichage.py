import numpy as np
import matplotlib.pyplot as plt
from typing import List
from Bot import bot
'''

'''


def Affichage(Nom_Action : str, courbe_boursiere : List[float], population : List[bot]) :
    
    longueur = len(population[0].GetPortefeuilleHistory())

    # Créer des données factices
    temps = np.linspace(0, longueur, longueur)  # Temps de 0 à 10
    portefeuille_personne1 = population[0].GetPortefeuilleHistory()
    portefeuille_personne2 = population[1].GetPortefeuilleHistory()
    #courbe_boursiere = np.sin(temps) * 50 + 300

    # Créer le graphique
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Temps (Jours)')

    '''
    # Tracer les courbes pour le portefeuille des personnes
    ax1.set_ylabel('Valeur du Portefeuille (USD)', color='tab:blue')
    limite_superieure_ax1 = max(portefeuille_personne1) * 1.1  # +10 pour une petite marge, ajustez selon vos besoins
    ax1.set_ylim(bottom=0, top=limite_superieure_ax1)
    ax1.plot(temps, portefeuille_personne1, label='Personne 1', color='tab:blue')
    ax1.plot(temps, portefeuille_personne2, label='Personne 2', color='tab:orange')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.legend(loc='upper left')
    '''

    # Tableau de couleurs (vous pouvez ajouter plus de couleurs si nécessaire)
    #couleurs = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

    ax1.set_ylabel('Valeur du Portefeuille (USD)', color='tab:blue')

    population_portefeuille = []
    for i in range(len(population)):
        population_portefeuille.append(population[i].GetPortefeuilleHistory())

    # Calcul de la limite supérieure pour ax1
    limite_superieure_ax1 = max([max(p) for p in population_portefeuille]) * 1.5
    limite_inferieure_ax1 = min([min(p) for p in population_portefeuille]) * 0.9
    ax1.set_ylim(bottom=0, top=limite_superieure_ax1)

    # Dessiner les courbes
    for i, portefeuille in enumerate(population_portefeuille):
        ax1.plot(temps, portefeuille, label=f'Bot {i + 1}', color='tab:blue', alpha=0.5)
    
    #couleur = couleurs[i % len(couleurs)]  # Prendre une couleur du tableau de couleurs

    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.legend(loc='upper left')




    # Créer un deuxième axe des ordonnées pour la courbe boursière
    ax2 = ax1.twinx()
    ax2.set_ylabel('Valeur Boursière (USD)', color='tab:green')
    limite_superieure_ax2 = max(courbe_boursiere) *1.1  # +10 pour une petite marge, ajustez selon vos besoins
    ax2.set_ylim(bottom=0, top=limite_superieure_ax2)
    ax2.plot(temps, courbe_boursiere, label='Courbe Boursière', color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:green')
    ax2.legend(loc='upper right')

    generation = population[0].GetGeneration()

    ax1.set_title(Nom_Action + " , Génération " + str(generation))

    # Afficher le graphique
    plt.show()
