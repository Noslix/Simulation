import pandas as pd
from Bot import bot
from typing import List
from collections import deque

# NOTE : Créer une classe de Simulation qui permet de créer un objet definissant le type de courbe. exemple 'APPL'
    

# Permet de simuler le systeme dans un envirronement donné en apportant les parametres d'un bot
# Parametre 1 : Achat (Struct sur le Temps de prise en compte et le % de Baisse et remontée)
# achat.temps, achat.baisse_p100 achat_delta
# Parametre 2 : Revente (Struct sur le % de deficit et de gain)
# 
# Parametres :
# achat_delta - Temps passé prit en compte pour le calcul (en heures)
# achat_deficit_p100 - % de deficit avant remontée (entre le delta t et le point le plus bas dans le delta)
# achat_rehausse_p100 - % de gain depuis rehausse (entre point le plus bas et l'instant t)
# vente_deficit_p100 - Vente si deficit atteint % (doit t-il s'adapter? si oui, gain % n'a pas d'interet)
# vente_gain_p100 - Vente si gain atteint % 

class Simulation:

    # CONSTRUCTEUR
    def __init__(self, Actions : List[float]):
        # contenu qui defini l'attribut des données en Bourses en fonction du symbole (ex APPL)
        
        
        self.donneesBoursieres = Actions
        self.montant_achat = 50
        self.portefeuille = 0
        self.prix_action_achat = 0


        # FAIRE QUE LE FICHIER AILLE DANS LE BON NOM PAR EXEMPLE APPL.txt
        # SELECTION DE LA COLONNE ?!? COMMENT ??
        '''
        actions = []
        with open('donnees_random.txt', 'r') as file:
            for line in file:
                actions.append(float(line.strip()))  # Convertir les valeurs en float et les ajouter à la liste
        '''

    def simulate_trading(self, bot_choisi : bot):
        
        # On defini les parametres du bot
        achat_delta = bot_choisi.GetAchat_delta()
        self.achat_deficit_p100 = bot_choisi.GetAchat_deficit_p100()
        self.achat_rehausse_p100 = bot_choisi.GetAchat_rehausse_p100()
        vente_deficitMax = bot_choisi.GetVente_deficitMax_p100()
        vente_gainMax = bot_choisi.GetVente_gainMax_p100()
        self.pourcent_ajustement = bot_choisi.GetPourcent_ajustement()
        self.portefeuille = bot_choisi.GetGain_USD()

        self.prix_action_achat = 0
        delta_actions = deque()
        self.portefeuille_initial = 100  # Montant initial
        self.portefeuille = self.portefeuille_initial
        self.portefeuille_history = [self.portefeuille]       

        

        for prix_actuel in self.donneesBoursieres :
            
            

            delta_actions = self.maj_delta_achat(delta_actions, achat_delta, prix_actuel)
            autorisationAchat = self.analyse_achat(delta_actions)

            difference_p100 = self.Resultat_Gain_p100(prix_actuel)

            # ACHAT
            if (self.prix_action_achat == 0) and autorisationAchat  :  
                self.montant_achat = self.portefeuille
                self.Achat_Action(prix_actuel)
                
            # REVENTE GAIN
            elif (difference_p100 >= vente_gainMax) and (self.prix_action_achat != 0) :
                self.Revente_Action(prix_actuel)

            # REVENTE DEFICIT
            elif (difference_p100 <= vente_deficitMax) and (self.prix_action_achat != 0) :
                self.Revente_Action(prix_actuel)
                
            self.portefeuille_history.append(self.portefeuille)

        self.portefeuille_history.pop() # La derniere valeur est en trop
        bot_choisi.SetGain_USD(self.portefeuille)
        bot_choisi.SetPortefeuilleHistory(self.portefeuille_history)

        return bot_choisi

    # On adapte le delta d'achat
    def maj_delta_achat(self, delta_actions, achat_delta, prix_actuel) :
        delta_actions.append(prix_actuel)
        if len(delta_actions) == achat_delta :
            delta_actions.popleft

        return delta_actions

    # On determine le taux de deficit et de gain à partir du niveau le plus bas selon le delta temps défini
    def analyse_achat(self, delta_actions) :
        pic_bas = self.Get_picBas_valeur(delta_actions)
        achat_deficit_p100_reel = round(pic_bas/delta_actions[0],2)-1
        achat_rehausse_p100_reel = round(delta_actions[-1]/pic_bas,2)-1

        deficitOK = self.EstProche(achat_deficit_p100_reel,
                              self.achat_deficit_p100,
                              self.pourcent_ajustement)
        
        rehausseOK = self.EstProche(achat_rehausse_p100_reel,
                              self.achat_rehausse_p100,
                              self.pourcent_ajustement)

        validAchat = deficitOK and rehausseOK

        return validAchat

    # Determine la valeur du pic le plus bas du delta temps
    def Get_picBas_valeur(self, delta_actions) :
        pic_bas = delta_actions[0]
        for delta_action in delta_actions :
            if delta_action <= pic_bas:
                pic_bas = delta_action
        return pic_bas

    def Montant_revente(self, prix_actuel : float) :
        return self.montant_achat * (prix_actuel / self.prix_action_achat)    
        
    def Achat_Action(self, prix_actuel):
        self.portefeuille -= self.montant_achat
        self.prix_action_achat = prix_actuel

    def Revente_Action(self, prix_actuel):
        self.portefeuille += self.montant_achat * (prix_actuel / self.prix_action_achat)
        self.prix_action_achat = 0

    # Défini le resultat du gain en % positif ou négatif
    def Resultat_Gain_p100(self, prix_actuel : float):
        if (self.prix_action_achat != 0) :
            val = ((prix_actuel / self.prix_action_achat)-1)*100
        else :
            val = 0
        return val
    '''
    def EstProche(self, val1_p100 : float, val2_p100 : float, tolerance_p100):
        val = abs(val1_p100 - val2_p100) <= tolerance_p100
        return val
    '''



    def EstProche(self, val1, val2, tolerance):
        if val1 == 0 and val2 == 0:
            resultat = True  # Les deux valeurs sont exactement zéro, donc elles sont proches
        elif val1 == 0 or val2 == 0:
            resultat = False  # L'une des valeurs est zéro mais pas l'autre, donc elles ne sont pas proches
        else :
            # Calculer la différence relative en pourcentage
            difference = abs(val1 - val2)
            avg = (val1 + val2) / 2
            relative_difference_percent = (difference / avg)
            resultat = relative_difference_percent <= tolerance

        return resultat

