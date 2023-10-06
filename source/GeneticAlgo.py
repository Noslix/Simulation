import random
import Simulation

from typing import List
from Bot import bot


actions = [1,2,3,4,5,6,7,8,9,8,7,5,3,1,1,3,4,6,7,9]
taux_mutation = 1.1 #test temporaire

# Fonction d'évaluation d'un bot
def evaluation_bot(bot):
    vente_deficitMax, vente_gainMax = bot
    portefeuille_final = Simulation.simulate_trading(actions, 10, -3, 6, vente_deficitMax, vente_gainMax, 10)
    return portefeuille_final

# Fonction de création d'une population initiale
def creation_population(population_taille : int) -> List[bot]:
    population = []
    for _ in range(population_taille):
        vente_deficitMax = random.uniform(0.01, 0.2)  # Valeurs aléatoires pour StopLoss entre 1% et 20%
        vente_gainMax = random.uniform(0.05, 0.3)  # Valeurs aléatoires pour TakeProfit entre 5% et 30%
        bot = (vente_deficitMax, vente_gainMax)
        population.append(bot)
    return population


# Fonction de sélection des meilleurs bots
# La clé permet de savoir le critere de selection voir fonction evaluation_bot()
def selection_meilleurs_bots(population : List[bot], nb_meilleurs : int) -> List[bot]:
    population_triee = sorted(population, key=lambda bot: bot.GetGain(), reverse=True)
    return population_triee[:nb_meilleurs]


# Fonction de croisement (croisement)
def croisement(parent1: bot, parent2: bot):
    param_parent1 = parent1.GetParametres()
    param_parent2 = parent1.GetParametres()
    croisement_point = random.randint(1, len(parent1.GetParametres()) - 1) #choisi le point de croisement
    param_enfant1 = param_parent1[:croisement_point] + param_parent2[croisement_point:]
    param_enfant2 = param_parent2[:croisement_point] + param_parent1[croisement_point:]
    enfant1 = bot(0, param_enfant1)
    enfant2 = bot(0, param_enfant2)

    return enfant1, enfant2

# Fonction de mutation
def mutation(bot_choisi: bot):
    taux_mutation = 0.1
    param_bot = bot_choisi.GetParametres()
    mutation_param_bot = list(param_bot)
    for i in range(len(param_bot)):
        if random.random() < taux_mutation:
            mutation_param_bot[i] = random.uniform(0.01, 0.2) if i == 0 else random.uniform(0.05, 0.3)

    mutation_bot = bot(0, tuple(mutation_param_bot))
    return mutation_bot


#Permet de generer les enfants depuis 2 parents selectionnés par roulette de selection
def Incubation(bot_parent1, bot_parent2):
    bot_enfant1, bot_enfant2 = croisement(bot_parent1, bot_parent2)
    bot_enfant1 = mutation(bot_enfant1)
    bot_enfant2 = mutation(bot_enfant2)
    return bot_enfant1, bot_enfant2
    


# Paramètres de l'algorithme génétique
population_taille = 100
nb_generations = 50
nb_meilleurs_bots = 10
taux_mutation = 0.1


def demarrage(self, actions : str, nb_generations : int, population_taille : int):
    # Création de la population initiale
    population = creation_population(population_taille)

    # Boucle d'évolution sur plusieurs générations
    for generation in range(nb_generations):

        # Mise en Situation des bots
        for i in range(len(population)) :
            population[i] = Simulation.simulate_trading(actions, population[i])

        # Sélection des meilleurs bots
        meilleurs_bots = selection_meilleurs_bots(population, nb_meilleurs_bots)

        # Création de la nouvelle génération par croisement et mutation
        nouvelle_population = meilleurs_bots.copy()

        while len(nouvelle_population) < population_taille:
            parent1, parent2 = random.choices(meilleurs_bots, k=2)
            enfant1, enfant2 = Incubation(parent1, parent2)
            nouvelle_population.extend([enfant1, enfant2])

        # Remplacement de l'ancienne population par la nouvelle
        population = nouvelle_population


    # Sélection du meilleur bot final
    #NOTE : retourner les resultats 

    #meilleur_bot = selection_meilleurs_bots(population, 1)[0]
    #meilleur_vente_deficitMax, meilleur_vente_gainMax = meilleur_bot
    #meilleur_portefeuille_final = Simulation.simulate_trading(actions, 10, -3, 6, meilleur_vente_deficitMax, meilleur_vente_gainMax, 10)

    #print(f"Meilleur StopLoss : {meilleur_vente_deficitMax:.4f}")
    #print(f"Meilleur TakeProfit : {meilleur_vente_gainMax:.4f}")
    #print("Solde final avec meilleurs paramètres : {}".format(meilleur_portefeuille_final[0]))
