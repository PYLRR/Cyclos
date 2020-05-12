import os
import unittest

from src.modules.parser import parseFromFile
from src.protocole.Action import Action
from src.protocole.Protocol import Protocol
from src.protocole.Transaction import Transaction
from src.protocole.Type import Type
from src.protocole.Variable import Variable
from src.protocole.primitive.concat import concat
from src.protocole.primitive.senc import senc
from src.protocole.EGreekCharacters import EGreekCharacters


class RefiningTest(unittest.TestCase):

    def setUp(self):
        typea = Type("typea", False, False)
        typeb = Type("typeb", False, False)
        kaenca = Type("kaenca", False, True)

        ska = Variable("ska", False, kaenca)
        a = Variable("a", False, typea)
        x = Variable("a", True, typea)
        b = Variable("b", False, typeb)

        # creation gamma0
        self.gamma0 = a

        # creation gamma1
        self.gamma1 = x

        # creation alpha0
        conca = concat([a, b])
        self.alpha0 = senc([conca, ska])

        # creation alpha1
        conca = concat([a, b])
        self.alpha1 = senc([conca, ska])

        action1 = Action(True, 1, EGreekCharacters.GAMMA, "1", self.gamma0)
        action2 = Action(False, 1, EGreekCharacters.GAMMA, "2", self.gamma1)

        action3 = Action(True, 1, EGreekCharacters.ALPHA, "1", self.alpha0)
        action4 = Action(False, 1, EGreekCharacters.ALPHA, "2", self.alpha1)

        trans1 = Transaction("gamma", [action1, action2])
        trans2 = Transaction("alpha", [action3, action4])

        self.protocol1 = Protocol([], [trans1, trans2])

        # mini protocol for refining first criteria
        # a: agent
        # in(x : agent)
        # out(a)

        agent = Type("agent", False, True)
        a = Variable("a", False, agent)
        x = Variable("x", True, agent)

        self.alpha11 = x
        self.alpha22 = a

        action11 = Action(True, 1, EGreekCharacters.ALPHA, "1", self.alpha11)
        action22 = Action(False, 1, EGreekCharacters.ALPHA, "2", self.alpha22)

        trans11 = Transaction("alpha", [action11, action22])

        self.protocol11 = Protocol([], [trans11])

        # mini protocol for refining second criteria
        # in( senc(msg, nonceb), kab)
        # out( senc( rep, nonceb), kab)

        nonceb = Type("nonceb", True, False)
        msg = Type("msg", True, False)
        rep = Type("rep", True, False)
        kab = Type("kab", False, False)

        n = Variable("n", False, nonceb)
        msg = Variable("msg", False, msg)
        rep = Variable("rep", False, rep)
        kab = Variable("kab", False, kab)

        conca1 = concat([msg, n])
        self.alpha111 = senc([conca1, kab])
        conca2 = concat([rep, n])
        self.alpha222 = senc([conca2, kab])

        action111 = Action(True, 1, EGreekCharacters.ALPHA, "1", self.alpha111)
        action222 = Action(False, 1, EGreekCharacters.ALPHA, "2", self.alpha222)

        trans111 = Transaction("alpha", [action111, action222])

        self.protocol111 = Protocol([], [trans111])

    def initProtocol(self, name):
        t = os.getcwd().split('/')
        if t[len(t) - 1] == "Cyclos":
            res = parseFromFile("./src/tests/parser/" + name)
        else:
            res = parseFromFile("../parser/" + name)

        matrices = res.refining()
        return matrices

    def test_refining(self):
        # self.protocol111.marking_first_criteria([])
        self.protocol1.marking_second_criteria([])
        # question pour stéphanie : est ce que dans ce cas le second critère doit marquer aussi le truc de gamma ? c'est  normal ?

    def test_refining_first_criteria(self):
        t = os.getcwd().split('/')
        if t[len(t) - 1] == "Cyclos":
            res = parseFromFile("./src/tests/parser/protocolForTests")
        else:
            res = parseFromFile("../parser/protocolForTests")
        marking = res.marking_first_criteria([])

        # self.assertEqual(len(marking), 5)

    def test_refining_one(self):
        self.protocol11.refining()

    def test_refining_second(self):
        self.protocol111.refining()

    def test_dep_seq_protocolForTests(self):
        matrices = self.initProtocol("protocolForTests")

        mat_verif_seq0 = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq1 = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq2 = ['0', '1', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq3 = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq4 = ['0', '0', '0', '1', '0', '0', '0', '0', '0']
        mat_verif_seq5 = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq6 = ['0', '0', '0', '0', '0', '1', '0', '0', '0']
        mat_verif_seq7 = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq8 = ['0', '0', '0', '0', '0', '0', '0', '1', '0']
        mat_verif_seq = [mat_verif_seq0, mat_verif_seq1, mat_verif_seq2, mat_verif_seq3, mat_verif_seq4,
                         mat_verif_seq5,
                         mat_verif_seq6, mat_verif_seq7, mat_verif_seq8]

        mat_seq = matrices[0]

        res = len(mat_verif_seq)
        if len(mat_seq) == len(mat_verif_seq):
            for i in range(len(mat_seq)):
                if mat_seq[i] == mat_verif_seq[i]:
                    res = res - 1
        self.assertEqual(0, res)

    def test_dep_data_protocolForTests(self):
        matrices = self.initProtocol("protocolForTests")

        mat_verif_data0 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data1 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data2 = ['-1', '-1', '-1', '-1', '0;1', '113', '-1', '-1', '0;1']
        mat_verif_data3 = ['2', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data4 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data5 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data6 = ['-1', '-1', '-1', '-1', '0;1', '113', '-1', '-1', '0;1']
        #mat_verif_data7 = ['2', '-1', '-1', '-1', '-1', '112;113', '-1', '-1', '-1']
        mat_verif_data7 = ['2', '-1', '-1', '-1', '-1', '113', '-1', '-1', '-1']
        mat_verif_data8 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data = [mat_verif_data0, mat_verif_data1, mat_verif_data2, mat_verif_data3, mat_verif_data4,
                          mat_verif_data5, mat_verif_data6, mat_verif_data7, mat_verif_data8]

        mat_data = matrices[1]

        res = len(mat_verif_data)
        if len(mat_data) == len(mat_verif_data):
            for i in range(len(mat_data)):
                #print(mat_data[i])
                if mat_data[i] == mat_verif_data[i]:
                    res = res - 1
        self.assertEqual(0, res)

    def test_dep_key_protocolForTests(self):
        matrices = self.initProtocol("protocolForTests")

        mat_verif_key0 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key1 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key2 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key3 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key4 = ['-1', '-1', '-1', '-1', '-1', '113', '-1', '-1', '-1']
        mat_verif_key5 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key6 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key7 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key8 = ['-1', '-1', '-1', '-1', '-1', '113', '-1', '-1', '-1']
        mat_verif_key = [mat_verif_key0, mat_verif_key1, mat_verif_key2, mat_verif_key3, mat_verif_key4,
                         mat_verif_key5,
                         mat_verif_key6, mat_verif_key7, mat_verif_key8]

        mat_key = matrices[2]

        res = len(mat_verif_key)
        if len(mat_key) == len(mat_verif_key):
            for i in range(len(mat_key)):
                if mat_key[i] == mat_verif_key[i]:
                    res = res - 1
        self.assertEqual(0, res)


    def test_dep_seq_NLSprotocol(self):
        matrices = self.initProtocol("NLSprotocol")

        mat_verif_seq0 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq1 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq2 = ['0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq3 = ['0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq4 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq5 = ['0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq6 = ['0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq7 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq8 = ['0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0']
        mat_verif_seq9 = ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0']
        mat_verif_seq10 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq11 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0']
        mat_verif_seq12 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0']
        mat_verif_seq = [mat_verif_seq0, mat_verif_seq1, mat_verif_seq2, mat_verif_seq3, mat_verif_seq4,
                         mat_verif_seq5, mat_verif_seq6, mat_verif_seq7, mat_verif_seq8, mat_verif_seq9,
                         mat_verif_seq10, mat_verif_seq11, mat_verif_seq12]

        mat_seq = matrices[0]

        res = len(mat_verif_seq)
        if len(mat_seq) == len(mat_verif_seq):
            for i in range(len(mat_seq)):
                if mat_seq[i] == mat_verif_seq[i]:
                    res = res - 1
        self.assertEqual(0, res)

    def test_dep_data_NLSprotocol(self):
        matrices = self.initProtocol("NLSprotocol")

        mat_verif_data0 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data1 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        #mat_verif_data2 = ['1', '-1', '-1', '-1', '-1', '0', '-1', '12', '-1', '-1', '-1', '12;13', '-1']
        mat_verif_data2 = ['1', '-1', '-1', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '12', '-1']
        mat_verif_data3 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        #mat_verif_data4 = ['2', '0', '-1', '-1', '-1', '-1', '-1', '12', '-1', '-1', '-1', '13', '-1']
        mat_verif_data4 = ['2', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data5 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        #mat_verif_data6 = ['2', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '12', '-1', '12', '-1']
        mat_verif_data6 = ['2', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '12', '-1']
        mat_verif_data7 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        #mat_verif_data8 = ['1', '-1', '-1', '-1', '-1', '-1', '-1', '11;12', '-1', '11', '-1', '13', '-1']
        mat_verif_data8 = ['1', '-1', '-1', '-1', '-1', '-1', '-1', '11', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data9 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        #mat_verif_data10 = ['2', '-1', '-1', '-1', '-1', '-1', '-1', '12', '-1', '-1', '-1', '11;13', '-1']
        mat_verif_data10 = ['2', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data11 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        #mat_verif_data12 = ['2', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '12', '-1', '12', '-1']
        mat_verif_data12 = ['2', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '12', '-1']

        mat_verif_data = [mat_verif_data0, mat_verif_data1, mat_verif_data2, mat_verif_data3, mat_verif_data4,
                          mat_verif_data5, mat_verif_data6, mat_verif_data7, mat_verif_data8, mat_verif_data9,
                          mat_verif_data10, mat_verif_data11, mat_verif_data12]

        mat_data = matrices[1]

        res = len(mat_verif_data)
        if len(mat_data) == len(mat_verif_data):
            for i in range(len(mat_data)):
                print(mat_data[i])
                if mat_data[i] == mat_verif_data[i]:
                    res = res - 1
        self.assertEqual(0, res)

    def test_dep_key_NLSprotocol(self):
        matrices = self.initProtocol("NLSprotocol")

        mat_verif_key0 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key1 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key2 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key3 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key4 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key5 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key6 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key7 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key8 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key9 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key10 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key11 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key12 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key = [mat_verif_key0, mat_verif_key1, mat_verif_key2, mat_verif_key3, mat_verif_key4,
                         mat_verif_key5, mat_verif_key6, mat_verif_key7, mat_verif_key8, mat_verif_key9,
                         mat_verif_key10, mat_verif_key11, mat_verif_key12]

        mat_key = matrices[2]

        res = len(mat_verif_key)
        if len(mat_key) == len(mat_verif_key):
            for i in range(len(mat_key)):
                if mat_key[i] == mat_verif_key[i]:
                    res = res - 1
        self.assertEqual(0, res)


    def test_dep_seq_ds_sc(self):
        matrices = self.initProtocol("ds-sc.txt")

        mat_verif_seq0 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq1 = ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq2 = ['0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq3 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq4 = ['0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq5 = ['0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq6 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq7 = ['0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq8 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq9 = ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0']
        mat_verif_seq10 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq11 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0']
        mat_verif_seq12 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq13 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0']
        mat_verif_seq14 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq = [mat_verif_seq0, mat_verif_seq1, mat_verif_seq2, mat_verif_seq3, mat_verif_seq4,
                         mat_verif_seq5, mat_verif_seq6, mat_verif_seq7, mat_verif_seq8, mat_verif_seq9,
                         mat_verif_seq10, mat_verif_seq11, mat_verif_seq12, mat_verif_seq13, mat_verif_seq14]

        mat_seq = matrices[0]

        res = len(mat_verif_seq)
        if len(mat_seq) == len(mat_verif_seq):
            for i in range(len(mat_seq)):
                if mat_seq[i] == mat_verif_seq[i]:
                    res = res - 1
        self.assertEqual(0, res)

    def test_dep_data_ds_sc(self):
        """matrices = self.initProtocol("ds-sc.txt")

        mat_verif_data0 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data1 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data2 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data3 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data4 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data5 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data6 = ['0', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data7 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data8 = ['0', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data9 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data10 = ['0', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data11 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data12 = ['-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data13 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data14 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '12', '-1', '-1', '-1']
        mat_verif_data = [mat_verif_data0, mat_verif_data1, mat_verif_data2, mat_verif_data3, mat_verif_data4,
                          mat_verif_data5, mat_verif_data6, mat_verif_data7, mat_verif_data8, mat_verif_data9,
                          mat_verif_data10, mat_verif_data11, mat_verif_data12, mat_verif_data13, mat_verif_data14]

        mat_data = matrices[1]

        res = len(mat_verif_data)
        if len(mat_data) == len(mat_verif_data):
            for i in range(len(mat_data)):
                # print(mat_data[i])
                if mat_data[i] == mat_verif_data[i]:
                    res = res - 1
        self.assertEqual(0, res)"""

    def test_dep_key_ds_sc(self):
        matrices = self.initProtocol("ds-sc.txt")

        mat_verif_key0 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key1 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key2 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key3 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key4 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key5 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key6 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key7 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key8 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key9 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key10 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key11 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key12 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key13 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key14 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key = [mat_verif_key0, mat_verif_key1, mat_verif_key2, mat_verif_key3, mat_verif_key4,
                         mat_verif_key5, mat_verif_key6, mat_verif_key7, mat_verif_key8, mat_verif_key9,
                         mat_verif_key10, mat_verif_key11, mat_verif_key12, mat_verif_key13, mat_verif_key14]

        mat_key = matrices[2]

        res = len(mat_verif_key)
        if len(mat_key) == len(mat_verif_key):
            for i in range(len(mat_key)):
                if mat_key[i] == mat_verif_key[i]:
                    res = res - 1
        self.assertEqual(0, res)


    def test_dep_seq_ns_sc(self):
        matrices = self.initProtocol("ns-sc.txt")

        mat_verif_seq0 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq1 = ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq2 = ['0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq3 = ['0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq4 = ['0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

        mat_verif_seq5 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq6 = ['0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

        mat_verif_seq7 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq8 = ['0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq9 = ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq10 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']

        mat_verif_seq11 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq12 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq13 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq14 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq15 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0']

        mat_verif_seq16 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq17 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0']

        mat_verif_seq18 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq19 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0']

        mat_verif_seq20 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        mat_verif_seq21 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0']
        mat_verif_seq22 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0']

        mat_verif_seq = [mat_verif_seq0, mat_verif_seq1, mat_verif_seq2, mat_verif_seq3, mat_verif_seq4,
                         mat_verif_seq5,mat_verif_seq6, mat_verif_seq7, mat_verif_seq8, mat_verif_seq9,
                         mat_verif_seq10, mat_verif_seq11, mat_verif_seq12, mat_verif_seq13, mat_verif_seq14,
                         mat_verif_seq15, mat_verif_seq16, mat_verif_seq17, mat_verif_seq18, mat_verif_seq19,
                         mat_verif_seq20, mat_verif_seq21, mat_verif_seq22]

        mat_seq = matrices[0]

        res = len(mat_verif_seq)
        if len(mat_seq) == len(mat_verif_seq):
            for i in range(len(mat_seq)):
                if mat_seq[i] == mat_verif_seq[i]:
                    res = res - 1
        self.assertEqual(0, res)

    def test_dep_data_ns_sc(self):
        """matrices = self.initProtocol("ns-sc.txt")

        mat_verif_data0 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data1 = ['-1', '-1', '-1', '-1', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data2 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data3 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '0;1;12', '-1', '-1', '-1', '-1', '12',
                           '-1', '-1', '-1', '-1', '-1', '112', '-1', '0;1;12', '-1']
        mat_verif_data4 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        mat_verif_data5 = ['0;1;2', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '2', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data6 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        mat_verif_data7 = ['-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data8 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data9 = ['-1', '-1', '-1', '-1', '0;1', '-1', '-1', '-1', '12', '-1', '-1', '-1', '-1', '12', '-1',
                           '0;1', '-1', '-1', '-1', '112', '-1', '12', '-1']
        mat_verif_data10 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                            '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        mat_verif_data11 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                            '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data12 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                            '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data13 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                            '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data14 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '0;1;12', '-1', '-1', '-1', '-1', '12',
                            '-1', '-1', '-1', '-1', '-1', '112', '-1', '0;1;12', '-1']
        mat_verif_data15 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                            '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        mat_verif_data16 = ['2', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '0;1;2', '-1', '-1', '-1',
                            '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data17 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                            '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        mat_verif_data18 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                            '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data19 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                            '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        mat_verif_data20 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                            '-1', '-1', '-1', '-1', '12', '-1', '-1', '-1']
        mat_verif_data21 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                            '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data22 = ['-1', '-1', '-1', '-1', '0;1', '-1', '-1', '-1', '12', '-1', '-1', '-1', '-1', '12', '-1',
                            '0;1', '-1', '-1', '-1', '112', '-1', '12', '-1']

        mat_verif_data = [mat_verif_data0, mat_verif_data1, mat_verif_data2, mat_verif_data3, mat_verif_data4,
                          mat_verif_data5, mat_verif_data6, mat_verif_data7, mat_verif_data8, mat_verif_data9,
                          mat_verif_data10, mat_verif_data11, mat_verif_data12, mat_verif_data13, mat_verif_data14,
                          mat_verif_data15, mat_verif_data16, mat_verif_data17, mat_verif_data18, mat_verif_data19,
                          mat_verif_data20, mat_verif_data21, mat_verif_data22]

        mat_data = matrices[1]

        res = len(mat_verif_data)
        if len(mat_data) == len(mat_verif_data):
            for i in range(len(mat_data)):
                # print(mat_data[i])
                if mat_data[i] == mat_verif_data[i]:
                    res = res - 1
        self.assertEqual(0, res)"""

    def test_dep_key_ns_sc(self):
        """matrices = self.initProtocol("ns-sc.txt")

        mat_verif_key0 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                          '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key1 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                          '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key2 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                          '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key3 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                          '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key4 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '12', '-1',
                          '-1', '-1', '-1', '-1', '112', '-1', '-1', '-1']

        mat_verif_key5 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                          '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key6 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                          '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        mat_verif_key7 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                          '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key8 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '12', '-1',
                          '-1', '-1', '-1', '-1', '112', '-1', '-1', '-1']
        mat_verif_key9 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                          '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key10 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '12', '-1',
                           '-1', '-1', '-1', '-1', '112', '-1', '-1', '-1']

        mat_verif_key11 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key12 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key13 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key14 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key15 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '112', '-1', '-1', '-1']

        mat_verif_key16 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key17 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        mat_verif_key18 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key19 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        mat_verif_key20 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_key21 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '12', '-1',
                           '-1', '-1', '-1', '-1', '112', '-1', '-1', '-1']
        mat_verif_key22 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1',
                           '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']

        mat_verif_key = [mat_verif_key0, mat_verif_key1, mat_verif_key2, mat_verif_key3, mat_verif_key4,
                         mat_verif_key5, mat_verif_key6, mat_verif_key7, mat_verif_key8, mat_verif_key9,
                         mat_verif_key10, mat_verif_key11, mat_verif_key12, mat_verif_key13, mat_verif_key14,
                         mat_verif_key15, mat_verif_key16, mat_verif_key17, mat_verif_key18, mat_verif_key19,
                         mat_verif_key20, mat_verif_key21, mat_verif_key22]

        mat_key = matrices[2]

        res = len(mat_verif_key)
        if len(mat_key) == len(mat_verif_key):
            for i in range(len(mat_key)):
                if mat_key[i] == mat_verif_key[i]:
                    res = res - 1
        self.assertEqual(0, res)"""
        
    def test_toy_ex2(self):
        matrices = self.initProtocol("toy-ex2.txt")
        mat_data = matrices[1]

        for i in range(len(mat_data)):
            print(mat_data[i])

    def test_toy_ex1d(self):

        matrices = self.initProtocol("toy-ex1e.txt")

        mat_data = matrices[1]
        mat_seq = matrices[0]
        mat_key = matrices[2]

        for i in range(len(mat_data)):
            print(mat_seq[i])

        print('-------------------')

        for i in range(len(mat_data)):
            print(mat_data[i])

        print('-------------------')

        for i in range(len(mat_data)):
            print(mat_key[i])


