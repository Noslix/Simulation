'''import unittest
from Simulation import Get_picBas_valeur, analyse_achat, maj_delta_achat
from GeneticAlgo import croisement, mutation 

#, mutation, selection_meilleurs_bots


delta_test=[9,8,7,6,5,4,5,6] # pic bas à 4

parent1 = (10,20)
parent2 = (30,40)

class TestFonctions(unittest.TestCase):
    def test_Get_picBas_valeur(self):
        self.assertEqual(Get_picBas_valeur(delta_test), 4)

    def test_analyse_achat(self):
        deficit, rehausse = analyse_achat(delta_test)
        self.assertEqual(deficit, -0.56)
        self.assertEqual(rehausse, 0.5)

    #def test_maj_delta_achat(self):
    #   self.assertEqual(maj_delta_achat(delta_test),-0.55,0.5)

    #def test_croisement(self):
    #   enfant1, enfant2 = croisement((10,20),(30,40))
    #   self.assertEqual(enfant1, (10,40))
    #   self.assertEqual(enfant2, (30,20)) 

   # def mutation(self)
        

if __name__ == '__main__':
    unittest.main()

    '''