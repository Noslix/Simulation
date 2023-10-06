# Lecture des valeurs de l'action depuis un fichier
actions = []
with open('donnees_random.txt', 'r') as file:
    for line in file:
        actions.append(float(line.strip()))  # Convertir les valeurs en float et les ajouter à la liste





class FileReader:
    def __init__(self, filename):
        self.filename = filename
        self.values = []

    def read_file(self):
        try:
            with open(self.filename, 'r') as file:
                # Lire chaque ligne du fichier
                for line in file:
                    # Convertir la ligne en valeur (en supprimant les espaces et les sauts de ligne)
                    value = line.strip()
                    # Ajouter la valeur au tableau
                    self.values.append(value)
        except FileNotFoundError:
            print(f"Le fichier '{self.filename}' n'a pas été trouvé.")

    def get_values(self):
        return self.values

'''
# Exemple d'utilisation
file_reader = FileReader('exemple.txt')
file_reader.read_file()
values = file_reader.get_values()
print('Valeurs lues depuis le fichier :', values)
'''