import unittest
from src.protocole.Type import Type
from src.protocole.Action import Action
from src.protocole.primitive.senc import senc
from src.protocole.Variable import Variable
from src.protocole.EGreekCharacters import EGreekCharacters


class RhoInTest(unittest.TestCase):

    def setUp(self):
        self.noncem = Type("noncem", False, False)
        self.noncek = Type("noncek", False, False)
        self.n1 = Variable("n1", False, self.noncem)
        self.k0 = Variable("k0", False, self.noncek)
        self.sencryption = senc([self.n1, self.k0])

        self.action = Action(True, 1, EGreekCharacters.ALPHA, "1", self.sencryption)

    def test_rho_in(self):
        rho = self.action.rho()
        print(rho)
        self.assertEqual(rho, [self.sencryption, self.noncem, self.noncek])
