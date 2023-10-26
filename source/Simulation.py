import pandas as pd
from Bot import bot
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
    def __init__(self, Action : 'str'):
        # contenu qui defini l'attribut des données en Bourses en fonction du symbole (ex APPL)
        
        NomFichier = 'stock_data_' + Action + '.csv'
        CheminFichier = 'Courbes/'

        dataframe = pd.read_csv(CheminFichier+NomFichier)
        self.date = dataframe['Date']
        self.ouverture = dataframe['Open'].astype(float)
        self.fermeture = dataframe['Close'].astype(float)
        self.volume = dataframe['Volume'].astype(float)

        print(self.volume)

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
        achat_deficit_p100 = bot_choisi.GetAchat_deficit_p100()
        achat_rehausse_p100 = bot_choisi.GetAchat_rehausse_p100()
        vente_deficitMax = bot_choisi.GetVente_deficitMax()
        vente_gainMax = bot_choisi.GetVente_gainMax()
        pourcent_ajustement = bot_choisi.GetPourcent_ajustement()
        portefeuille = bot_choisi.GetGain()

        
        actions_detenues = 0
        prix_action = 1 #defaut 1€ 
        delta_actions = deque()
        portefeuille_initial = 10000  # Montant initial
        portefeuille = portefeuille_initial
        #portefeuille_history = [portefeuille]       

        valeursActions = self.volume

        for prix_actuel in valeursActions :
            
            delta_actions = self.maj_delta_achat(delta_actions, achat_delta, prix_actuel)
            achat_deficit_p100, achat_rehausse_p100 = self.analyse_achat(delta_actions)

            # Si nous n'avons pas d'actions, achetons si le prix est bas
            if actions_detenues == 0:  
                self.Achat_Action(portefeuille, actions_detenues, prix_actuel)
                
            # Si le prix a augmenté suffisamment, vendons
            if (prix_actuel - prix_action) / prix_action >= vente_gainMax:  
                self.Revente_Action_Deficit(portefeuille, actions_detenues, prix_actuel)

            # Si le prix a baissé trop, vendons pour limiter les pertes
            if (prix_action - prix_actuel) / prix_action >= vente_deficitMax:  
                self.Revente_Action_Gain(portefeuille, actions_detenues, prix_actuel)
            
            #portefeuille_history.append(portefeuille)  # Ajouter le solde actuel à l'historique
            print({portefeuille})

        # NOTE : Dois s'arreter avant la fin et non revendre par défaut a nimporte quel moment.
        # Vendre toutes les actions restantes à la fin de la simulation
        portefeuille += actions_detenues * valeursActions[-1]
        actions_detenues = 0
        #portefeuille_history.append(portefeuille)  # Ajouter le solde final à l'historique

        bot_choisi.SetGain(portefeuille)

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
        achat_deficit_p100 = round(pic_bas/delta_actions[0],2)-1
        achat_rehausse_p100 = round(delta_actions[-1]/pic_bas,2)-1

        return achat_deficit_p100, achat_rehausse_p100

    # Determine la valeur du pic le plus bas du delta temps
    def Get_picBas_valeur(self, delta_actions) :
        pic_bas = delta_actions[0]
        for delta_action in delta_actions :
            if delta_action <= pic_bas:
                pic_bas = delta_action
        return pic_bas
        
    def Achat_Action(self, portefeuille, actions_detenues, prix_actuel):
        prix_action = prix_actuel
        nb_actions_a_acheter = 10#int(portefeuille / prix_action)
        portefeuille -= nb_actions_a_acheter * prix_action
        actions_detenues += nb_actions_a_acheter

    def Revente_Action_Deficit(self, portefeuille, actions_detenues, prix_actuel):
        portefeuille += actions_detenues * prix_actuel
        actions_detenues = 0

    def Revente_Action_Gain(self, portefeuille, actions_detenues, prix_actuel):
        portefeuille += actions_detenues * prix_actuel
        actions_detenues = 0