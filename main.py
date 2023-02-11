#!/usr/bin/env python3
"""
Graph - Matrix Project
~~~~~~~~~~~~~~~~~~~~~~

Does some cool operations with Incidence/Adjacency Matrix <-> Graph
Basic usages:

    ┬─[amjoshaghani@Charon:~/P/MatrixGraph]─[11:47:15 PM]
    ╰─>$ python main.py
    Please enter incidence matrix row and column count (ex: 2 2):	4 6
    Now, enter the matrix itself row by row:
1 0 0 1 0 0
1 1 0 0 1 1
0 1 1 0 0 0
0 0 1 1 1 1
    Enter your desired command to do with matrix ('help <command>' for commands and help):
    :> dictized
    {'A': ['e1', 'e4'], 'B': ['e1', 'e2', 'e5', 'e6'], 'C': ['e2', 'e3'], 'D': ['e3', 'e4', 'e5', 'e6']}
    :> adjy
    [[0, 1, 0, 1], [1, 0, 1, 2], [0, 1, 0, 1], [1, 2, 1, 0]]


available commands:
    ~> dictized
    ~> help
    ~> adjy
    ~> deg
    ~> rev_edg
    ~> add_edg
    ~> rev_node
    ~> add_node
    ~> plot
    ~> exit


To see more about commands, type:
    :> help <command name>


:copyright: (c) 2023 by AMJoshaghani [at] amjoshaghani.ir.
:license: MIT, see LICENSE for more details.
"""
import i18n
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

I18n = i18n.I18n()


class Graph:
    def __init__(self, matrix) -> None:
        self.matrix = matrix
        self.incidentDict = {}
        self.dictized()
        self.vertices = self.incidentDict.keys()
        self.edges_l = len(self.matrix[0])

    def dictized(self) -> dict:
        """
            Return a dictized matrix which is a Vertx: [*Edges] Dictionary made out of the matrix stored in
        self.matrix which is a 2D list.
        :return: dict
        """
        G = {}
        if not self.incidentDict:
            i = int(ord("A"))
            for r in self.matrix:
                if chr(i) not in G:
                    G[chr(i)] = []
                for j, c in enumerate(r, start=1):
                    if c == 1:
                        G[chr(i)].append(f"e{j}")
                i += 1
            self.incidentDict = G
            return G
        else:
            return self.incidentDict

    def adjy(self) -> list:
        """
            Return an adjacency matrix out of given incident matrix
        Sample adjacency matrix pattern is shown below:
        *   A    B    C    D
        A ⌈ 0    1    1    0 ⌉
        B | 1    0    0    0 |
        C | 0    1    0    1 |
        D ⌊ 0    0    1    0 ⌋
        :return: 2D list
        """
        G = []
        i = self.incidentDict
        for v1 in self.incidentDict:
            r = []
            for v2 in self.incidentDict:
                if v2 != v1:
                    intsec = len(set(i[v1]) & set(i[v2]))
                    r.append(intsec)
                else:
                    r.append(0)
            G.append(r)
        return G

    def deg(self) -> dict:
        """
            Return Degree of a vertex which is number of edges by which it is connected to other vertices.
        :return: dict
        """
        G = {}
        i = self.incidentDict
        for k in i:
            G[k] = len(i[k])
        return G

    def add_edg(self, v1, v2) -> bool:
        """
            Add an edge between two vertices.
        :param v1: initial vertex
        :param v2: final vertex
        :return: boolean True/False by which user can acknowledge success or failure of addition
        """
        edg_i = self.edges_l + 1
        G = {}
        for k in self.incidentDict:
            r = self.incidentDict[k].copy()
            if k in [v1, v2]:
                r.append(f"e{edg_i}")
            G[k] = r
        if self.incidentDict == G:
            return False
        else:
            self.incidentDict = G
            self.edges_l = edg_i
            return True

    def rev_edg(self, edge_no) -> bool:
        """
            Remove an edge from the whole graph.
        :param edge_no: corresponding number to the intended edge
        :return: boolean True/False by which user can acknowledge success or failure of removal
        """
        G = {}
        for k in self.incidentDict:
            r = []
            for v in self.incidentDict[k]:
                if v != f"e{edge_no}":
                    r.append(v)
            G[k] = r
        if self.incidentDict == G:
            return False
        else:
            self.incidentDict = G
            return True

    def add_node(self, name) -> bool:
        """
            Add a vertex to the graph.
        :param name: dedicated name to the vertex (which must be unique)
        :return: boolean True/False by which user can acknowledge success or failure of addition
        """
        if name not in self.incidentDict:
            self.incidentDict[name] = []
            return True
        else:
            return False

    def rev_node(self, name) -> bool:
        """
            Remove a vertex from the graph.
        :param name: vertex name which must be removed
        :return: boolean True/False by which user can acknowledge success or failure of removal
        """
        if name in self.incidentDict:
            edges = self.incidentDict[name].copy()
            for v in self.incidentDict:
                for e in edges:
                    v2_edges = self.incidentDict[v]
                    if e in v2_edges:
                        v2_edges.remove(e)
            del self.incidentDict[name]
            return True
        else:
            return False

    def _node_node(self) -> dict:
        """
            Return a Node: [*Nodes] dictionary.
        :return: dict
        """
        b = self.incidentDict
        r = {}
        nodes = list(b.keys())
        for node1 in nodes:
            for node2 in nodes:
                if node2 != node1:
                    if set(b[node2]) & set(b[node1]):
                        if r.get(node1):
                            r[node1] += node2
                        else:
                            r[node1] = [node2]
        return r

    def shortest(self, v1, v2) -> str:
        """
            Return shortest way between node v1 and node v2.
        :param v1: initial vertex name
        :param v2: final vertex name
        :return: shortest way between nodes in node-node style or a warning
        """
        graph = self._node_node()
        nodes = list(self.incidentDict.keys())
        if v1 not in nodes:
            I18n.raise_(ValueError, "E04", v1)
        elif v2 not in nodes:
            I18n.raise_(ValueError, "E04", v2)
        elif v1 == v2:
            return I18n.warn_("W02")

        explored = []
        queue = [[v1]]
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node not in explored:
                neighbours = graph[node]
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    if neighbour == v2:
                        str_ = ""
                        for N in new_path:
                            str_ += N
                        return str_
                explored.append(node)

        return I18n.warn_("W03")

    def plot(self) -> bool:
        """
            Plot the resultant graph out of the given matrix.
        :return: boolean True/False by which user can acknowledge success or failure of plotting
        """
        try:
            G = nx.from_numpy_array(np.array(self.adjy()), parallel_edges=True, create_using=nx.MultiGraph)
            labels = dict(zip(G.nodes(), self.incidentDict.keys()))
            color_lookup = {k: v for v, k in enumerate(sorted(set(G.nodes())))}
            low, *_, high = sorted(color_lookup.values())
            norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
            mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
            nx.draw(
                    G, with_labels=True,
                    labels=labels,
                    connectionstyle='arc3, rad = 0.1',
                    arrows=True,
                    node_color=[mapper.to_rgba(i) for i in color_lookup.values()],
                    font_color='white'
            )
            plt.title("Graph")
            plt.style.use('dracula')
            plt.show()
            return True
        except Exception as e:
            I18n.raise_(TypeError, "E03", e)


if __name__ == "__main__":
    M = list()
    """
    Sample incidence matrix pattern is shown below:
    *  e1   e2   e3   e4
    A ⌈ 1    1    1    0 ⌉
    B | 1    0    0    0 |
    C | 0    1    0    1 |
    D ⌊ 0    0    1    1 ⌋
    """
    inp = input(I18n.log_("I01"))  # ex. 4 3
    if len(inp.split()) != 2:
        I18n.raise_(ValueError, "E01", len(inp.split()))
    rows, columns = map(int, inp.split())
    print(I18n.log_("I02"))
    for row in range(rows):
        col = input().split()
        if len(col) == columns:
            M.append(list(map(int, col)))  # TODO: check if not decimal
        else:
            I18n.raise_(ValueError, "E02", columns, len(col))
    Graph = Graph(M)
    print(I18n.log_("I03"))
    while True:
        inp = input(I18n.log_("I04"))
        inp = inp.split()
        if inp and (inp[0] in I18n.var_()):
            if inp[0] == "exit":
                break
            elif inp[0] == "help":
                if len(inp) > 1:
                    if inp[1] in I18n.var_():
                        h = I18n.var_(inp[1])
                        print("\t$~" + I18n.log_("I04") + f"{inp[1]}{' ' + h[1] if h[1] else ''}" +
                              I18n.bl_(I18n.read("I05")) + "\n",
                              I18n.inf_("\t" + h[0]))
                    else:
                        print(I18n.warn_("W01"))
                else:
                    print(*list(I18n.var_()))
            else:
                if len(inp) > 1:
                    print(getattr(Graph, inp[0])(*inp[1:]))
                else:
                    print(getattr(Graph, inp[0])())
        else:
            print(I18n.warn_("W01"))

    print(I18n.log_("I99"))
