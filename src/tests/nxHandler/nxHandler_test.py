from src.modules.nXHandler import getnxFromProtocolFile
from src.modules.parser import parseFromFile
from src.protocole.Protocol import Protocol

from unittest import TestCase
import networkx as nx
import os


class nxHandler_test(TestCase):
    # list of list of dependencies (1 list for each kind of dep)
    Graph = nx.Graph()

    def setUp(self):
        t = os.getcwd().split('/')
        if t[len(t) - 1] == "Cyclos":
            path = "./src/tests/parser/protocolForTests"
        else:
            path = "../parser/protocolForTests"
        self.Graph = getnxFromProtocolFile(path)

    def tearDown(self):
        self.Graph = nx.Graph()

    def test_cycles(self):
        TestCase.assertTrue(self, nx.is_directed_acyclic_graph(self.Graph))
