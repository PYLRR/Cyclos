# -*- coding: utf-8 -*-

from src.modules.parser import parseFromFile
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
import networkx as nx
import re
from itertools import islice, count

dataDepColor = 'red'
keyDepColor = 'purple'
seqDepColor = 'green'

# currently used to determine the size of the nodes
windowSize = 12

# used to determine the max nb of cycles displayed
maxCycles = 50

# handles the creation of a graph with dependencies, its display and the search of cycles
class nxHandler:
    # to get a nxHandler, use global function getnxFromDependencies or getnxFromProtocolFile
    def __init__(self, G):
        self.G = G
        self.layout = self.__getCustomLayout()  # layout that we have to keep unchanged as it defines the nodes pos
        self.drawSeq = True  #  these 3 attributes allow to draw specific dependencies
        self.drawData = True
        self.drawKey = True
        self.drawCycles = False
        self.figure = None
        self.numCycleToDraw = 0  # number of the cycle that will be shown if drawCycle is true

    # loads old draw specifications
    def setOldAttributesDraw(self, oldgraph):
        self.drawSeq = oldgraph.drawSeq
        self.drawData = oldgraph.drawData
        self.drawKey = oldgraph.drawKey
        self.drawCycles = oldgraph.drawCycles

    # draw the graph according to what booleans specify, with matplotlib. Can be used with console, qt, and other things
    def draw(self):
        plt.clf()
        if self.figure is not None:
            plt.close(self.figure)
        self.figure = plt.figure(frameon=True)
        self._drawNodes()
        if self.drawSeq: self.__drawSeqDep()
        if self.drawData: self.__drawDataDep()
        if self.drawKey: self.__drawKeyDep()
        return self.figure

    # saves the graph somewhere in png format
    def saveGraph(self, path):
        plt.savefig(path)

    # prints the graph in console if possible
    def printGraph(self):
        plt.show()

    # returns true if the graph is acyclic, false otherwise
    def isAcyclic(self):
        return nx.is_directed_acyclic_graph(self.G)

    # returns the number of cycles that the graph has, minoring at 50 if there are more
    def getCyclesNumber(self):
        n=0
        cycles = nx.simple_cycles(self.G)
        for x in cycles:
            if n>=maxCycles:
                return maxCycles
            n+=1
        return sum(1 for x in nx.simple_cycles(self.G))

    # increases the variable numCycleToDraw so that next time a cycle is drawn, it will be the next one in the list
    def nextCycle(self):
        self.numCycleToDraw += 1
        if self.numCycleToDraw >= self.getCyclesNumber():  # exceeding number of cycles, let's do a loop
            self.numCycleToDraw = 0

    # decreases the variable numCycleToDraw so that next time a cycle is drawn, it will be the previous one in the list
    def previousCycle(self):
        self.numCycleToDraw -= 1
        if self.numCycleToDraw < 0:  # going under 0, let's do a loop
            self.numCycleToDraw = self.getCyclesNumber() - 1

    # private function used to draw the nodes only
    def _drawNodes(self):
        self.__drawnxGraph(self.__getGraphByEdgeColor(None))

    # private function used to draw sequence dependencies only
    def __drawSeqDep(self):
        self.__drawnxGraph(self.__getGraphByEdgeColor(seqDepColor))

    # private function used to draw data dependencies only
    def __drawDataDep(self):
        self.__drawnxGraph(self.__getGraphByEdgeColor(dataDepColor))

    # private function used to draw key dependencies only
    def __drawKeyDep(self):
        self.__drawnxGraph(self.__getGraphByEdgeColor(keyDepColor))

    # creates a graph clone only containing the edges with the given color. Keeps only color and label attributes
    # used to draw seperatly key, data and seq dependencies
    def __getGraphByEdgeColor(self, value):
        G2 = nx.create_empty_copy(self.G)
        for u in self.G.nodes():
            adj = self.G.edges._adjdict[u]
            for v in self.G.nodes():
                if v in adj:
                    for edge in adj[v]:  # we search edges corresponding to the given attribute value
                        if adj[v][edge]['color'] == value:
                            if 'label' in adj[v][edge]:
                                G2.add_edge(u, v, color=value, label=adj[v][edge]['label'])
                            else:
                                G2.add_edge(u, v, color=value)
        return G2

    # computes a layout organizing sequential dependencies on straight vertical lines
    def __getCustomLayout(self):
        # let's create a graph with only squential dependencies to find connex components for a vertical display of them
        G2 = self.__getGraphByEdgeColor(seqDepColor)
        G2 = G2.to_undirected()
        groupsGenerator = nx.connected_components(G2)
        groups = []
        for group in groupsGenerator:
            groups.append(sorted(group, key=lambda nod: -int(re.search(r"\d+", nod).group())))
        # let's find the position of each node
        pos = {}
        for i in range(len(groups)):
            x = (1 + i) * (2 / (len(groups) + 1)) - 1  # spreading of sequential convex groups from -1 to 1
            group = groups[i]
            for j in range(len(group)):
                y = (1 + j) * (2 / (len(group) + 1)) - 1  # spreading of nodes from the same group from -1 to 1
                node = group[j]
                pos[node] = [x, y]
        return pos

    # draws the given subgraph (nodes, edges, labels), highlighting cycles if the corresponding boolean is set to True
    def __drawnxGraph(self, subG):
        # first of all, we collect the edges belonging to cycles
        cycleEdgesList = []
        if self.drawCycles:
            cycles = nx.simple_cycles(self.G)
            if self.getCyclesNumber() > 0:
                # next line gets the good cycle, but as cycles is a generator and not a list we need islice()
                cycle = next(islice(cycles, self.numCycleToDraw, None))
                for i in range(len(cycle) - 1):  # applied for each node but the last one, so we go from 0 to n-2
                    cycleEdgesList.append((cycle[i], cycle[i + 1]))
                cycleEdgesList.append((cycle[len(cycle) - 1], cycle[0]))  # finishing the loop : from last to 1st

        # let's separate sequential dependencies from other edges (the display will not be the same)
        seqEdges = []  # the 4 next variables are used to split seq/nonseq to draw one linear and the other curved
        seqColors = []
        otherEdges = []
        otherColors = []
        cycleSeqEdges = []  # equivalents to the previous 4 variables but belonging to cycles
        cycleSeqColors = []
        cycleOtherEdges = []
        cycleOtherColors = []
        dataEdges = []  # the 4 next variables are used to draw colorized labels, splitting data/key
        keyEdges = []
        dataEdge_labels = {}
        keyEdge_labels = {}
        for u in subG.nodes():
            adj = subG.edges._adjdict[u]
            for v in subG.nodes():
                if v in adj:
                    for edge in adj[v]:
                        if adj[v][edge]['color'] == seqDepColor:  # sequential dependency
                            seqEdges.append((u, v))
                            seqColors.append(seqDepColor)
                            if (u, v) in cycleEdgesList:  # this edge belongs to a cycle
                                cycleSeqEdges.append((u, v))
                                cycleSeqColors.append(seqDepColor)
                        else:  # other dependency
                            otherEdges.append((u, v))
                            otherColors.append(adj[v][edge]['color'])
                            if (u, v) in cycleEdgesList:  # this edge belongs to a cycle
                                cycleOtherEdges.append((u, v))
                                cycleOtherColors.append(adj[v][edge]['color'])
                            if adj[v][edge]['color'] == dataDepColor:  # data dependency
                                dataEdges.append((u, v))
                                dataEdge_labels[(u, v)] = adj[v][edge]['label']
                            else:  # key dependency
                                keyEdges.append((u, v))
                                keyEdge_labels[(u, v)] = adj[v][edge]['label']

        # sequential dependency
        nx.draw(subG, self.layout, edgelist=seqEdges, edge_color=seqColors, with_labels=True,
                node_size=windowSize * 200)

        # data dependency labels
        nx.draw_networkx_edge_labels(subG, self.layout, edgelist=dataEdges, edge_labels=dataEdge_labels,
                                     font_weight='bold', font_size=8,
                                     label_pos=0.6, clip_on=False, node_size=windowSize * 200, font_color=dataDepColor)
        # key dependency labels
        nx.draw_networkx_edge_labels(subG, self.layout, edgelist=keyEdges, edge_labels=keyEdge_labels,
                                     font_weight='bold', font_size=8,
                                     label_pos=0.6, clip_on=False, node_size=windowSize * 200, font_color=keyDepColor)

        # non sequential dependency
        nx.draw(subG, self.layout, edgelist=otherEdges, edge_color=otherColors, with_labels=True,
                node_size=windowSize * 200,
                font_color='w', font_weight='bold', connectionstyle='Arc3, rad=0.1')

        # sequential dependency belonging go a cycle
        nx.draw(subG, self.layout, edgelist=cycleSeqEdges, edge_color=cycleSeqColors, with_labels=True,
                node_size=windowSize * 200, arrowsize=15, width=4)

        # non sequential dependency belonging to a cycle
        nx.draw(subG, self.layout, edgelist=cycleOtherEdges, edge_color=cycleOtherColors, with_labels=True,
                node_size=windowSize * 200,
                font_color='w', font_weight='bold', connectionstyle='Arc3, rad=0.1', arrowsize=15, width=4)


# function used to create a NetworkX graph from a list of list of dependencies (a list for each of the 3 dep kind)
def getnxFromDependencies(protocol, dependencies):
    # matrix describing sequence dependencies
    matSeq = dependencies[0]
    # matrix describing data dependencies
    matData = dependencies[1]
    # matrix describing key dependencies
    matKey = dependencies[2]

    # number of nodes (= number of actions)
    n = len(matSeq)  # = len(numpyMatData) = len(numpyMatKey)
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(0, n))

    # building the graph's edges
    for i in range(0, n):
        for j in range(0, n):
            if matData[i][j] != '-1':
                G.add_edge(i, j, label=matData[i][j], color=dataDepColor)
            if matKey[i][j] != '-1':
                G.add_edge(i, j, label=matKey[i][j], color=keyDepColor)
            if matSeq[i][j] == '1':
                G.add_edge(i, j, label=matSeq[i][j], color=seqDepColor)

    # labeling node with names like "alpha1In"
    for i in range(0, n):
        G = nx.relabel_nodes(G, {i: protocol.getAction(i).label})

    return nxHandler(G)


# function used to create a NetworkX graph from a protocol defined in a txt file
def getnxFromProtocolFile(protocol_path):
    res = parseFromFile(protocol_path)
    return getnxFromDependencies(res, res.build_dependencies())
