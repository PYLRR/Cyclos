import unittest
from src.protocole.Type import Type
from src.protocole.Action import Action
from src.protocole.primitive.pub import pub
from src.protocole.primitive.concat import concat
from src.protocole.primitive.sign import sign
from src.protocole.primitive.aenc import aenc
from src.protocole.Variable import Variable
from src.protocole.EGreekCharacters import EGreekCharacters


class RhoOutTest(unittest.TestCase):

    def setUp(self):
        typea = Type("typea", False, True)
        a = Variable("a", False, typea)
        typeb = Type("typeb", False, True)
        b = Variable("b", False, typeb)
        noncek = Type("noncek", False, False)
        k0 = Variable("k0", False, noncek)
        kaenca = Type("kaenca", True, False)
        ska = Variable("ska", False, kaenca)
        kaencb = Type("kaencb", True, False)
        skb = Variable("skb", False, kaencb)
        pub_kaencb = pub([skb])
        conca = concat([a, b, k0])
        signat = sign([conca, ska])
        self.aencryption = aenc([signat, pub_kaencb])

        self.action = Action(False, 1, EGreekCharacters.ALPHA, "0", self.aencryption)

    def test_rho_out(self):
        rho = self.action.rho()
        print(rho)
        self.assertEqual(rho, [[[self.aencryption, 0], [0, 0]]])
