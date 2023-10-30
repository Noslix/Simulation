import pandas as pd
from typing import List

def GetDonneesFromFile(action : str) -> List[float] :
    NomFichier = 'stock_data_' + action + '.csv'
    CheminFichier = 'Courbes/'

    dataframe = pd.read_csv(CheminFichier+NomFichier)
    date = dataframe['Date']
    ouverture = dataframe['Open'].astype(float)
    fermeture = dataframe['Close'].astype(float)
    volume = dataframe['Volume'].astype(float)
    print(ouverture)

    donnees = ouverture.tolist()

    return donnees