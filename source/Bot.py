import uuid

class bot:

    # CONSTRUCTEUR
    def __init__(self, generation, parametres = None ):


        if parametres is None:
            parametres = []
        else :
            self._achat_delta_temps = parametres[0]
            self._achat_deficit_p100 = parametres[1]
            self._achat_rehausse_p100 = parametres[2]
            self._vente_deficitMax_p100 = parametres[3]
            self._vente_gainMax_p100 = parametres[4]
            self._pourcent_ajustement = parametres[5]

            #NOTE : A INTEGRER
            #self._prendreProfitExiste = parametres[6]
            #self._SuiveurArretDeficitExiste = parametres[7]

        self.generation = generation  # Numero de la génération
        self.parametres = parametres  # Liste des parametres du bot

        self.unique_id = uuid.uuid4()
        self.gains = 0  # Liste des gains associés aux parametres

        

        self.portefeuille_history = []
        

    
    # INFORMATIONS GENERALES

    def GetGain_USD(self):
        return self.gains
    
    def SetGain_USD(self, value):
        self.gains = value

    def SetPortefeuilleHistory(self, history) :
        self.portefeuille_history = history

    def GetPortefeuilleHistory(self) :
        return self.portefeuille_history

    def GetGeneration(self):
        return self.generation
    
    def GetID(self):
        self.unique_id

    # GESTION DES PARAMETRES

    def GetParametres(self):
        return [self._achat_delta_temps, self._achat_deficit_p100, self._achat_rehausse_p100, self._vente_deficitMax_p100, self._vente_gainMax_p100, self._pourcent_ajustement]

    def SetParametres(self, param_list):
        self._achat_delta_temps = param_list[0]
        self._achat_deficit_p100 = param_list[1]
        self._achat_rehausse_p100 = param_list[2]
        self._vente_deficitMax_p100 = param_list[3]
        self._vente_gainMax_p100 = param_list[4]
        self._pourcent_ajustement = param_list[5]
        
    def GetAchat_delta(self):
        return self._achat_delta_temps
    
    def GetAchat_deficit_p100(self):
        if(self._achat_deficit_p100 > 0) :
            print("ERREUR VALEUR ACHAT DEFICIT EST UNE VALEUR POSITIVE !!!")
        return self._achat_deficit_p100
    
    def GetAchat_rehausse_p100(self):
        return self._achat_rehausse_p100
    
    def GetVente_deficitMax_p100(self):
        if(self._vente_deficitMax_p100 > 0) :
            print("ERREUR VALEUR VENTE DEFICIT EST UNE VALEUR POSITIVE !!!")
        return self._vente_deficitMax_p100
        
            
        
    def GetVente_gainMax_p100(self):
        return self._vente_gainMax_p100
    
    def GetPourcent_ajustement(self):
        return self._pourcent_ajustement
    
    def SetAchat_delta_temps(self, value):
        self._achat_delta_temps = value
    
    def SetAchat_deficit_p100(self, value : float):
        self._achat_deficit_p100 = value
    
    def SetAchat_rehausse_p100(self, value : float):
        self._achat_rehausse_p100 = value
    
    def SetVente_deficitMax_p100(self, value : float):
        self._vente_deficitMax_p100 = value
    
    def SetVente_gainMax_p100(self, value : float):
        self._vente_gainMax_p100 = value
    
    def SetPourcent_ajustement(self, value : float):
        self._pourcent_ajustement = value

    def __str__(self):
        return f"bot {self.unique_id} - Parametres: {self.parametres}, Gains: {self.gains}"
