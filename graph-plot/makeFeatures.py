# This file contains the logic to populate edges and nodes in the graph of the webpage.
import json
import numpy as np
import requests
from storageNodeHandler import addStorage, getStorageDic
from inforShareHandler import getReqCookie, IsInfoShared
from redirectionEdgeHandler import getRedirection
from networkNodeHandler import getInitiator, getInitiatorURL
from graphviz import Digraph
import networkx as nx
from networkx.drawing import nx_agraph
import pygraphviz


def main():
    path = "C:/Users/Hadiy/OneDrive/Desktop/webpage-crawler-extension/server/output/washingtonpost.com/graph"
    # g = nx.read_dot(path)
    # g= nx.Graph(nx.nx_pydot.read_dot(path))
    g = nx_agraph.from_agraph(pygraphviz.AGraph(path))

    nodes = nx.closeness_centrality(g)
    # nodes = nx.diameter(g.to_undirected())
    # nodes = max([max(j.values()) for (i,j) in nx.shortest_path_length(g)])
    # for k in nx.connected_components(g.to_undirected()):
    #     prigitnt(nx.diameter(k))
    print(len(nodes))


main()
