import random
import Simulation
import Affichage
import Donnees

from typing import List
from Bot import bot
from Simulation import Simulation


#actions = [1,2,3,4,5,6,7,8,9,8,7,5,3,1,1,3,4,6,7,9]
taux_mutation = 1.2 #test temporaire


# Fonction de création d'une population initiale
def creation_population(population_taille : int) -> List[bot]:
    population = []
    for i in range(population_taille):
        nouveau_bot = bot(0)
        nouveau_bot.SetAchat_delta_temps(random.uniform(1, 100))
        nouveau_bot.SetAchat_deficit_p100(random.uniform(-0.01, -100))
        nouveau_bot.SetAchat_rehausse_p100(random.uniform(0.01, 100))
        nouveau_bot.SetVente_deficitMax_p100(random.uniform(-0.01, -100))  # Valeurs aléatoires pour StopLoss entre 1% et 100%
        nouveau_bot.SetVente_gainMax_p100(random.uniform(0.01, 100))  # Valeurs aléatoires pour TakeProfit entre 1% et 100%
        nouveau_bot.SetPourcent_ajustement(random.uniform(0.01, 1))
        population.append(nouveau_bot)

    return population


# Fonction de sélection des meilleurs bots
# La clé permet de savoir le critere de selection voir fonction evaluation_bot()
def selection_meilleurs_bots(population : List[bot], nb_meilleurs : int) -> List[bot]:
    population_triee = sorted(population, key=lambda bot: bot.GetGain_USD(), reverse=True)
    return population_triee[:nb_meilleurs]


# Fonction de croisement (croisement)
def croisement(parent1, parent2):
    generation = parent1.GetGeneration()
    param_parent1 = parent1.GetParametres()
    param_parent2 = parent2.GetParametres() 
    croisement_point = random.randint(1, len(param_parent1) - 1) #choisi le point de croisement
    param_enfant1 = param_parent1[:croisement_point] + param_parent2[croisement_point:]
    param_enfant2 = param_parent2[:croisement_point] + param_parent1[croisement_point:]
    enfant1 = bot(generation+1, param_enfant1)
    enfant2 = bot(generation+1, param_enfant2)

    return enfant1, enfant2

# Fonction de mutation
def mutation(bot_choisi: bot):
    taux_mutation = 0.1
    param_bot = bot_choisi.GetParametres()
    generation = bot_choisi.GetGeneration()
    mutation_param_bot = list(param_bot)
    for i in range(len(param_bot)):
        if random.random() < taux_mutation:
            # Conserver le signe de la valeur originale
            sign = 1 if param_bot[i] >= 0 else -1
            mutation_value = random.uniform(0.01, 0.2) if i == 0 else random.uniform(0.05, 0.3)
            mutation_param_bot[i] = mutation_value * sign

    mutation_bot = bot(generation, tuple(mutation_param_bot))
    return mutation_bot



#Permet de generer les enfants depuis 2 parents selectionnés par roulette de selection
def Incubation(bot_parent1, bot_parent2):
    bot_enfant1, bot_enfant2 = croisement(bot_parent1, bot_parent2)
    bot_enfant1 = mutation(bot_enfant1)
    bot_enfant2 = mutation(bot_enfant2)
    return bot_enfant1, bot_enfant2
    


# Paramètres de l'algorithme génétique
#population_taille = 100
#nb_generations = 50
nb_meilleurs_bots = 50
#taux_mutation = 0.1


'''
Permet le lancement de l'algorithme genetique.
'''

def demarrage(actions : str, nb_generations : int, population_taille : int):

    donneeBoursieres = Donnees.GetDonneesFromFile("AAPL")

    # Création de la population initiale
    population = creation_population(population_taille)

    maSimulation = Simulation(donneeBoursieres)

    # Boucle d'évolution sur plusieurs générations
    for generation in range(nb_generations):

        for i in range(len(population)) :
            population[i] = maSimulation.simulate_trading(population[i])

        if( generation == nb_generations-1):
            Affichage.Affichage(actions, donneeBoursieres, population)
            

        #NOTE : DEFINIR METHODE DE SELECTIONe
        meilleurs_bots = selection_meilleurs_bots(population, nb_meilleurs_bots)
        #random.shuffle(meilleurs_bots) ???
        nouvelle_population = [] #meilleurs_bots.copy()
        print("---------------------------")
        print("Gain : ", meilleurs_bots[0].GetGain_USD())
        print("Vente Deficit : ", meilleurs_bots[0].GetVente_deficitMax_p100())
        print("Vente Gain : ", meilleurs_bots[0].GetVente_gainMax_p100())

        # Prend des paires de parents pour créer des enfants
        for i in range(0, len(meilleurs_bots), 2):
            if i + 1 < len(meilleurs_bots):
                parent1 = meilleurs_bots[i]
                parent2 = meilleurs_bots[i + 1]
                enfant1, enfant2 = Incubation(parent1, parent2)
                nouvelle_population.extend([enfant1, enfant2])

        population = nouvelle_population




        

    


    # Sélection du meilleur bot final
    #NOTE : retourner les resultats 

    #meilleur_bot = selection_meilleurs_bots(population, 1)[0]
    #meilleur_vente_deficitMax, meilleur_vente_gainMax = meilleur_bot
    #meilleur_portefeuille_final = Simulation.simulate_trading(actions, 10, -3, 6, meilleur_vente_deficitMax, meilleur_vente_gainMax, 10)

    #print(f"Meilleur StopLoss : {meilleur_vente_deficitMax:.4f}")
    #print(f"Meilleur TakeProfit : {meilleur_vente_gainMax:.4f}")
    #print("Solde final avec meilleurs paramètres : {}".format(meilleur_portefeuille_final[0]))
