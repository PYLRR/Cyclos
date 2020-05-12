from src.modules import nXHandler
import networkx as nx
import sys


if len(sys.argv) == 1: # no arg
    path = "src/tests/parser/protocolForTests"
else:  # at least 1 arg : we assume it is the protocol path
    path = sys.argv[1]

Graph = nXHandler.getnxFromProtocolFile(path)

Graph.draw()

Graph.saveGraph("res.png")

print("\nThe graph was saved to ./res.png")

if Graph.isAcyclic():
    print("The dependency graph is acyclic")
else:
    print("The dependency graph is not acyclic")
