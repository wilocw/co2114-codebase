import math
import warnings
import json

from matplotlib import pyplot as plt

from agent.things import Thing, Agent
from agent.environment import Environment


class Node(Thing):
    def __init__(self, label=""):
        self.label = label
        self.neighbours = set()
        self.weights = {}
    def __repr__(self):
        return self.label
    def add_neighbour(self, node, weight=None):
        if not isinstance(node, Node):
            raise TypeError(f"{self}: {node} is not a Node")
        if node not in self.neighbours:
            self.neighbours.add(node)
            self.weights[node] = weight
            node.add_neighbour(self, weight)

class Graph:
    def __init__(self):
        self.nodes = set()

    def __iter__(self):
        return iter(self.nodes)

    def add_node(self, node):
        if not isinstance(node, Node):
            raise TypeError(f"{self}: {node} is not a Node")
        if node not in self.nodes:
            self.nodes.add(node)
            for neighbour in node.neighbours:
                self.add_node(neighbour)

    def plot_nodes(self, condition=None, init = None, labels=None):
        nodes = self.nodes if condition is None else \
            {node for node in self.nodes if condition(node)}
        if len(nodes) == 0:
            return plt.figure(figsize=(8,8))
        if init is None or init not in nodes:
            init = next(iter(nodes))  # random node
        locs = {init: (0,0)}
        tree = {0: {init}}
        dist = 1  # dist from init
        tree[dist] = init.neighbours & nodes  # set intersection
        for i, node in enumerate(tree[dist]):
            locs[node] = (dist, i-0.5*len(tree[dist]))

        while len(tree[dist]) > 0:
            tree[dist+1] = set()
            for node in tree[dist]:
                neighbours = node.neighbours & nodes # set intersection
                for _node in neighbours:
                    if _node not in locs and _node not in tree[dist+1]:
                        tree[dist+1].add(_node)
            dist += 1
            for i, node in enumerate(tree[dist]):
                offset = i-0.5*len(tree[dist])
                locs[node] = (dist + 0.1*offset, offset)
        
        edges = set()
        for node in nodes:
            for _node in (node.neighbours & nodes):
                forward = (node, _node, node.weights[_node])
                backward = (_node, node, _node.weights[node])
                if forward not in edges and backward not in edges:
                    edges.add(forward)

        fig, ax = plt.subplots(figsize=(8,8))
        for node, loc in locs.items():
            name = str(node) if labels is None else labels[node]
            ax.plot(*loc, 'ko', ms=20)
            ax.text(loc[0]+0.1, loc[1]+0.1, name)
        
        for edge in edges:
            a,b, weight = locs[edge[0]], locs[edge[1]], edge[2]
            ax.plot(*[[i,j] for i,j in zip(a,b)],'k')
            if weight is not None:
                ax.text(*[i+(j-i)/2 for i,j in zip(a,b)], str(weight))
        ax.axis("off")
        return fig


class GraphEnvironment(Environment):
    def __init__(self, graph=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph = graph if isinstance(graph, Graph) else Graph()

    def add_node(self, node):
        self.graph.add_node(node)

    def percept(self, agent):
        node = agent.location
        if len(node.weights) == 0:
            return node.neighbours
        else:
            return [(n, node.weights[n]) for n in node.neighbours]

    def add_agent(self, agent, location=None, node=None):
            if not isinstance(agent, Agent):
                raise TypeError("f{self}: {agent} is not an Agent")
            if node is not None:
                if not isinstance(node, Node):
                    print(f"{self}: {node} is not a valid Node")
                if node in self.graph:
                    super().add_agent(agent, node)
                else:
                    print(f"{self}: {node} is not in graph")
            elif location is not None:
                _flag = True
                for node in self.graph:
                    if location == node.location:
                        super().add_agent(agent, node)
                        _flag = False
                        break
                if _flag:
                    print(f"{self}: {location} was not found in environment")
            else:
                super().add_agent(agent)

    def show(self, *args, **kwargs):
        with warnings.catch_warnings(action="ignore"):
            self.graph.plot_nodes(*args, **kwargs).show()

    @classmethod
    def from_dict(ShortestPathEnvironment, graph_dict):
        if "vertices" not in graph_dict and "edges" not in graph_dict:
            raise ValueError(f"No vertices in json string {graph_dict}")
        if "edges" not in graph_dict:
            raise ValueError(f"No edges in json string {graph_dict}")
        vertices = graph_dict['vertices' if 'vertices' in graph_dict else 'nodes']
        edges = graph_dict['edges']
        for edge in edges:
            if len(edge) != 2:
                raise ValueError(f"Edges must comprise two nodes, {edge} does not")
            if any(v not in vertices for v in edge):
                raise ValueError(f"Edges must map between valid vertices, {edge} does not")
        
        nodes = {v: Node(v) for v in vertices}
        if 'weights' in graph_dict:
            weights = graph_dict['weights']
        else:
            weights = [None]*len(edges)
        for edge, weight in zip(edges, weights):
            a, b = edge
            nodes[a].add_neighbour(nodes[b], weight)

        environment = ShortestPathEnvironment()
        for _,node in nodes.items():
            environment.add_node(node)
        return environment
    
    @classmethod
    def from_json(ShortestPathEnvironment, json_str):
        return ShortestPathEnvironment.from_dict(json.loads(json_str))
