# This file contains the logic to populate edges and nodes in the graph of the webpage.
import json
from platform import node
import numpy as np
import pandas as pd
from storageNodeHandler import getStorageScriptFromStackWebGraph
from graphviz import Digraph
import networkx as nx
from networkx.drawing import nx_agraph
import pygraphviz
import os


def convGraphToNX(file):
    return nx_agraph.from_agraph(pygraphviz.AGraph(file))


def dicToExcel(dict, path):
    df = pd.DataFrame(data=dict)
    df = df.T
    df.columns = [
        "script_name",
        "label",
        "num_requests_sent",
        "num_nodes",
        "num_edges",
        "nodes_div_by_edges",
        "edges_div_by_nodes",
        "in_degree",
        "out_degree",
        "in_out_degree",
        "ancestor",
        "descendants",
        "closeness_centrality",
        "in_degree_centrality",
        "out_degree_centrality",
        "is_eval_or_external_function",
        "descendant_of_eval_or_function",
        "ascendant_script_has_eval_or_function",
        "num_script_successors",
        "num_script_predecessors",
        "storage_getter",
        "storage_setter",
        "cookie_getter",
        "cookie_setter",
    ]
    df.to_excel(path)


def fileToCount(file, types, category):
    dic = {}
    for line in file:
        dataset = json.loads(line)
        script_url = getStorageScriptFromStackWebGraph(dataset["stack"])
        if script_url not in dic:
            dic[script_url] = [0] * len(types)
        dic[script_url][types.index(dataset[category])] += 1
    return dic


def main():
    count = 0
    fold = os.listdir(
        "server/output"
    )
    for site in fold:
      try:
        # scripts = {id: ['script_name-0', 'label-1', 'num_requests_sent-2', 'num_node-3', 'num_edges-4', 'nodes_div_by_edges-5', 'edges_div_by_nodes-6', 'in_degree-7', 'out_degree-8', 'in_out_degree-9', 'ancestor-10', 'descendants-11',
        # 'closeness_centrality-12', 'in_degree_centrality-13', 'out_degree_centrality-14', 'is_eval_or_external_function-15', 'descendant_of_eval_or_function-16', 'ascendant_script_has_eval_or_function-17','num_script_successors-18',
        # 'num_script_predecessors-19', 'storage_getter-20', 'storage_setter-21', 'cookie_getter-22', 'cookie_setter-23']}
        scripts = {}

        print("features: ", site)

        folder = (
            "server/output/"
            + site
            + "/"
        )
        path = folder + "graph"
        graph = convGraphToNX(path)

        pathtonodes = folder + "nodes.json"

        # Opening JSON file
        f = open(pathtonodes)
        data = json.load(f)
        track = 0
        func = 0
        is_eval_or_external_function_ids = []
        script_ids = []
        for key in data.keys():

            if data[key][1] == "Script":
                script_ids.append(data[key][0])
                if key.split("@")[1] == "":
                    is_eval_or_external_function_ids.append(data[key][0])

                if data[key][0] not in scripts.keys():
                    # https:115 -- handling such cases
                    if "https://" in key.split("@")[1]:
                        scripts[(data[key][0])] = [key.split("@")[1]]
                    else:
                        scripts[(data[key][0])] = [""]

                # label as functional (label -> 0)
                if data[key][2] == 0 and data[key][3] != 0:
                    scripts[data[key][0]].append(0)
                    func += data[key][3]
                # label as tracking (label -> 1)
                elif data[key][3] == 0 and data[key][2] != 0:
                    scripts[data[key][0]].append(1)
                    track += data[key][2]
                # label mixed as tracking (label -> 1)
                elif data[key][2] != 0 and data[key][3] != 0:
                    scripts[data[key][0]].append(1)
                # label no initialization scripts as functional (label -> 0)
                elif data[key][2] == 0 and data[key][3] == 0:
                    scripts[data[key][0]].append(0)
                # num_requests_sent
                scripts[data[key][0]].append(data[key][2] + data[key][3])

        # num of nodes, edges, (n/e), and (e/n)
        num_edges = graph.number_of_edges()
        num_nodes = graph.number_of_nodes()
        nodes_div_by_edges = num_nodes / num_edges
        edges_div_by_nodes = num_edges / num_nodes

        for key in scripts.keys():
            scripts[key].append(num_nodes)
            scripts[key].append(num_edges)
            scripts[key].append(nodes_div_by_edges)
            scripts[key].append(edges_div_by_nodes)

        # node ids from int to str
        method_ids = [str(i) for i in scripts.keys()]
        # in-out degree
        out_degree = graph.out_degree(method_ids)
        in_degree = graph.in_degree(method_ids)

        for item in in_degree:
            scripts[int(item[0])].append(item[1])
        for item in out_degree:
            scripts[int(item[0])].append(item[1])

        in_degree_centrality = nx.in_degree_centrality(graph)
        out_degree_centrality = nx.out_degree_centrality(graph)

        for key in scripts.keys():
            # sum of in-out degree
            scripts[key].append(scripts[key][7] + scripts[key][8])
            # ancestors and desendants
            scripts[key].append(len(nx.ancestors(graph, str(key))))
            scripts[key].append(len(nx.descendants(graph, str(key))))
            # closeness_centrality
            scripts[key].append(nx.closeness_centrality(graph, str(key)))
            # in_degree_centrality
            scripts[key].append(in_degree_centrality[str(key)])
            # out_degree_centrality
            scripts[key].append(out_degree_centrality[str(key)])

            # is_eval_or_external_function
            if scripts[key][0] == "":
                scripts[key].append(1)
            else:
                scripts[key].append(0)

            # descendant_of_eval_or_function
            # ascendant_script_has_eval_or_function
            # num_script_successors
            # num_script_predecessors
            scripts[key].append(0)
            scripts[key].append(0)
            scripts[key].append(0)
            scripts[key].append(0)
            for node_id in nx.descendants(graph, str(key)):
                if int(node_id) in is_eval_or_external_function_ids:
                    scripts[key][16] = 1
                if int(node_id) in script_ids:
                    scripts[key][18] += 1
            for node_id in nx.ancestors(graph, str(key)):
                if int(node_id) in is_eval_or_external_function_ids:
                    scripts[key][17] = 1
                if int(node_id) in script_ids:
                    scripts[key][19] += 1

        # nodes = nx.closeness_centrality(graph)
        # print(nx.reciprocity(graph, method_ids))

        # 'storage_getter', 'storage_setter', 'cookie_getter', 'cookie_setter'
        with open(folder + "cookie_storage.json") as file:
            storage = fileToCount(
                file,
                [
                    "storage_getter",
                    "storage_setter",
                    "cookie_getter",
                    "cookie_setter",
                ],
                "function",
            )
        for scrpt in scripts.keys():
            scripts[scrpt].append(0)
            scripts[scrpt].append(0)
            scripts[scrpt].append(0)
            scripts[scrpt].append(0)
            for key in storage.keys():
                if scripts[scrpt][0] == key:
                    # ["storage_getter", "storage_setter", "cookie_getter", "cookie_setter"]
                    scripts[scrpt][20] = storage[key][0]
                    scripts[scrpt][21] = storage[key][1]
                    scripts[scrpt][22] = storage[key][2]
                    scripts[scrpt][23] = storage[key][3]

        dicToExcel(
            scripts,
            folder + "/webGraphfeatures.xlsx",
        )
        print(track, func)
        count += 1
        with open("webGraphfeatures_logs.txt", "w") as log:
            log.write(str(count))
            log.close()
      except Exception as e:
            print("not-features: ", e)


main()
