from unittest import TestCase
from src.modules.parser import parse, parseFromFile
from src.protocole.Protocol import Protocol
from src.protocole.Type import Type
from src.protocole.EGreekCharacters import EGreekCharacters
import os


class parser_test(TestCase):
    res = Protocol()

    def setUp(self):
        t = os.getcwd().split('/')
        if t[len(t) - 1] == "Cyclos":
            self.res = parseFromFile("./src/tests/parser/protocolForTests")
        else:
            self.res = parseFromFile("./protocolForTests")

    def tearDown(self):
        self.res = Protocol()

    def test_publicDeclarations(self):
        a = self.res.getVarInlist("a")
        TestCase.assertNotEqual(self, a, None)
        TestCase.assertNotEqual(self, self.res.getVarInlist("b"), None)
        TestCase.assertNotEqual(self, self.res.getVarInlist("c"), None)

        typea = self.res.getTypeInlist("typea")
        TestCase.assertNotEqual(self, typea, None)
        TestCase.assertNotEqual(self, self.res.getTypeInlist("typeb"), None)
        TestCase.assertNotEqual(self, self.res.getTypeInlist("typec"), None)

        TestCase.assertFalse(self, a.onTheFly)
        TestCase.assertEqual(self, a.type, typea)
        TestCase.assertTrue(self, typea.public)
        TestCase.assertFalse(self, typea.honest)

    def test_privateDeclarations(self):
        ska = self.res.getVarInlist("ska")
        k0 = self.res.getVarInlist("k0")
        n1 = self.res.getVarInlist("n1")
        TestCase.assertNotEqual(self, ska, None)
        TestCase.assertNotEqual(self, self.res.getVarInlist("skb"), None)
        TestCase.assertNotEqual(self, self.res.getVarInlist("skc"), None)
        TestCase.assertNotEqual(self, k0, None)
        TestCase.assertNotEqual(self, n1, None)

        noncem = self.res.getTypeInlist("noncem")
        kaenca = self.res.getTypeInlist("kaenca")
        noncek = self.res.getTypeInlist("noncek")
        TestCase.assertNotEqual(self, noncem, None)
        TestCase.assertNotEqual(self, kaenca, None)
        TestCase.assertNotEqual(self, self.res.getTypeInlist("kaencb"), None)
        TestCase.assertNotEqual(self, self.res.getTypeInlist("kaencc"), None)
        TestCase.assertNotEqual(self, noncek, None)

        TestCase.assertFalse(self, k0.onTheFly)
        TestCase.assertFalse(self, n1.onTheFly)
        TestCase.assertFalse(self, ska.onTheFly)
        TestCase.assertEqual(self, ska.type, kaenca)
        TestCase.assertEqual(self, k0.type, noncek)
        TestCase.assertEqual(self, n1.type, noncem)

        TestCase.assertFalse(self, noncem.public)
        TestCase.assertFalse(self, kaenca.public)
        TestCase.assertFalse(self, noncek.public)
        TestCase.assertFalse(self, noncem.honest)
        TestCase.assertTrue(self, kaenca.honest)
        TestCase.assertFalse(self, noncek.honest)

    def test_onTheFlyDeclarations(self):
        xb = self.res.getVarInlist("xb")
        xa0 = self.res.getVarInlist("xa0")
        TestCase.assertNotEqual(self, xb, None)
        TestCase.assertNotEqual(self, xa0, None)

        noncem = self.res.getTypeInlist("noncem")
        noncek = self.res.getTypeInlist("noncek")
        TestCase.assertNotEqual(self, noncem, None)
        TestCase.assertNotEqual(self, noncek, None)

        TestCase.assertTrue(self, xb.onTheFly)
        TestCase.assertTrue(self, xa0.onTheFly)
        TestCase.assertEqual(self, xb.type, noncek)
        TestCase.assertEqual(self, xa0.type, noncem)

        TestCase.assertFalse(self, noncem.public)
        TestCase.assertFalse(self, noncek.public)
        TestCase.assertFalse(self, noncem.honest)
        TestCase.assertFalse(self, noncek.honest)

    def test_transaction0(self):
        trans0 = self.res.listTransactions[0]
        TestCase.assertFalse(self, trans0.actions[0].type)  # out
        TestCase.assertEqual(self, trans0.actions[0].channel, 0)
        TestCase.assertEqual(self, trans0.actions[0].label, EGreekCharacters.ALPHA.__str__ + "0out")
        TestCase.assertEqual(self, trans0.actions[0].rootTerm.name, "concat")
        TestCase.assertEqual(self, trans0.actions[0].rootTerm.arguments[0].name, "pub")
        TestCase.assertEqual(self, trans0.actions[0].rootTerm.arguments[1].name, "pub")

        ska = self.res.getVarInlist("ska")
        skb = self.res.getVarInlist("skb")

        TestCase.assertEqual(self, trans0.actions[0].rootTerm.arguments[0].arguments[0], ska)
        TestCase.assertEqual(self, trans0.actions[0].rootTerm.arguments[1].arguments[0], skb)

        kaenca = self.res.getTypeInlist("kaenca")
        kaencb = self.res.getTypeInlist("kaencb")

        TestCase.assertEqual(self, ska.type, kaenca)
        TestCase.assertEqual(self, skb.type, kaencb)

    def test_transaction3(self):
        trans3 = self.res.listTransactions[3]
        # action 0
        TestCase.assertFalse(self, trans3.actions[0].type)  # out
        TestCase.assertEqual(self, trans3.actions[0].channel, 3)
        TestCase.assertEqual(self, trans3.actions[0].label, EGreekCharacters.DELTA.__str__ + "0out")
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.name, "aenc")
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[0].name, "sign")
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[1].name, "pub")
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[0].arguments[0].name, "concat")

        a = self.res.getVarInlist("a")
        c = self.res.getVarInlist("c")
        k1 = self.res.getVarInlist("k1")
        ska = self.res.getVarInlist("ska")
        skc = self.res.getVarInlist("skc")

        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[0].arguments[0].arguments[0], a)
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[0].arguments[0].arguments[1], c)
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[0].arguments[0].arguments[2], k1)
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[0].arguments[1], ska)
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[1].arguments[0], skc)

        typea = self.res.getTypeInlist("typea")
        typec = self.res.getTypeInlist("typec")
        noncek = self.res.getTypeInlist("noncek")
        kaenca = self.res.getTypeInlist("kaenca")
        kaencc = self.res.getTypeInlist("kaencc")

        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[0].arguments[0].arguments[0].type, typea)
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[0].arguments[0].arguments[1].type, typec)
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[0].arguments[0].arguments[2].type, noncek)
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[0].arguments[1].type, kaenca)
        TestCase.assertEqual(self, trans3.actions[0].rootTerm.arguments[1].arguments[0].type, kaencc)

        # action 1
        TestCase.assertTrue(self, trans3.actions[1].type)  # in
        TestCase.assertEqual(self, trans3.actions[1].channel, 3)
        TestCase.assertEqual(self, trans3.actions[1].label, EGreekCharacters.DELTA.__str__ + "1in")
        TestCase.assertEqual(self, trans3.actions[1].rootTerm.name, "senc")
        xa1 = self.res.getVarInlist("xa1")

        TestCase.assertEqual(self, trans3.actions[1].rootTerm.arguments[0], xa1)
        TestCase.assertEqual(self, trans3.actions[1].rootTerm.arguments[1], k1)

        noncem = self.res.getTypeInlist("noncem")
        TestCase.assertEqual(self, trans3.actions[1].rootTerm.arguments[0].type, noncem)
        TestCase.assertEqual(self, trans3.actions[1].rootTerm.arguments[1].type, noncek)
