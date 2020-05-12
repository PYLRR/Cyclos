import os
import unittest

from src.modules.parser import parseFromFile
from src.protocole.Type import Type
from src.protocole.Action import Action
from src.protocole.primitive.pub import pub
from src.protocole.primitive.concat import concat
from src.protocole.primitive.sign import sign
from src.protocole.primitive.aenc import aenc
from src.protocole.primitive.senc import senc
from src.protocole.Transaction import Transaction
from src.protocole.Protocol import Protocol
from src.protocole.Variable import Variable
# import networkx
# import numpy
# import matplotlib.pyplot as plt
# import re
from src.protocole.EGreekCharacters import EGreekCharacters


class DependenciesTest(unittest.TestCase):

    def initProtocol(self, name):
        t = os.getcwd().split('/')
        if t[len(t) - 1] == "Cyclos":
            res = parseFromFile("./src/tests/parser/"+name)
        else:
            res = parseFromFile("../parser/"+name)

        matrices = res.build_dependencies()
        return matrices

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
        mat_verif_data7 = ['2', '-1', '-1', '-1', '-1', '112;113', '-1', '-1', '-1']
        mat_verif_data8 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data = [mat_verif_data0, mat_verif_data1, mat_verif_data2, mat_verif_data3, mat_verif_data4,
                          mat_verif_data5, mat_verif_data6, mat_verif_data7, mat_verif_data8]

        mat_data = matrices[1]

        res = len(mat_verif_data)
        if len(mat_data) == len(mat_verif_data):
            for i in range(len(mat_data)):
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
        mat_verif_data2 = ['1', '-1', '-1', '-1', '-1', '0', '-1', '12', '-1', '-1', '-1', '12;13', '-1']
        mat_verif_data3 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data4 = ['2', '0', '-1', '-1', '-1', '-1', '-1', '12', '-1', '-1', '-1', '13', '-1']
        mat_verif_data5 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data6 = ['2', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '12', '-1', '12', '-1']
        mat_verif_data7 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data8 = ['1', '-1', '-1', '-1', '-1', '-1', '-1', '11;12', '-1', '11', '-1', '13', '-1']
        mat_verif_data9 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data10 = ['2', '-1', '-1', '-1', '-1', '-1', '-1', '12', '-1', '-1', '-1', '11;13', '-1']
        mat_verif_data11 = ['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1']
        mat_verif_data12 = ['2', '-1', '-1', '0', '-1', '-1', '-1', '-1', '-1', '12', '-1', '12', '-1']
        mat_verif_data = [mat_verif_data0, mat_verif_data1, mat_verif_data2, mat_verif_data3, mat_verif_data4,
                          mat_verif_data5, mat_verif_data6, mat_verif_data7, mat_verif_data8, mat_verif_data9,
                          mat_verif_data10, mat_verif_data11, mat_verif_data12]

        mat_data = matrices[1]

        res = len(mat_verif_data)
        if len(mat_data) == len(mat_verif_data):
            for i in range(len(mat_data)):
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
                         mat_verif_key5,mat_verif_key6, mat_verif_key7, mat_verif_key8, mat_verif_key9,
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
                         mat_verif_seq5,mat_verif_seq6, mat_verif_seq7, mat_verif_seq8, mat_verif_seq9,
                         mat_verif_seq10, mat_verif_seq11, mat_verif_seq12, mat_verif_seq13, mat_verif_seq14]

        mat_seq = matrices[0]

        res = True
        for i in range(len(mat_seq)):
            if not mat_seq[i] == mat_verif_seq[i]:
                res = False

        self.assertEqual(True, res)

    '''
    def test_dep_data_ds_sc(self):
        matrices = self.initProtocol("ds-sc.txt")

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

        res = True
        for i in range(len(mat_data)):
            if not mat_data[i] == mat_verif_data[i]:
                res = False

        self.assertEqual(True, res)
'''