# This file contains the logic to populate edges and nodes in the graph of the webpage.
import json
import numpy as np
import requests
from storageNodeHandler import addStorage, getStorageDic
from inforShareHandler import getReqCookie, IsInfoShared
from redirectionEdgeHandler import getRedirection
from networkNodeHandler import getInitiator, getInitiatorURL
from graphviz import Digraph

# node labels
label = [0]


def addNode(nodes, name, type, TC, FC, classlabel):
    if name not in nodes.keys():
        nodes[name] = [label[0], type, 0, 0, classlabel]
        label[0] += 1
    if classlabel == 0:
        nodes[name][2] += TC
        nodes[name][3] += FC
    return nodes[name][0]


def addEdge(edges, src, tar, type):
    if str(src) + "@" + str(tar) not in edges.keys():
        edges[str(src) + "@" + str(tar)] = [src, tar, type]


def findWordInScript(script_url, word):
    try:
        resp = requests.get(script_url)
        if word in resp.text:
            return 1
        return 0
    except:
        return 1


def getDecendantsCount(node, adjEdges, visited, count):
    if node in adjEdges.keys():
        # count[0] += len(adjEdges[node])
        visited[node] = True
        for des in adjEdges[node]:
            if des not in visited.keys():
                count[0] += 1
                getDecendantsCount(des, adjEdges, visited, count)


def createGraphFeatures(url):

    folder = (
        "C:/Users/Hadiy/OneDrive/Desktop/webpage-crawler-extension/server/output/"
        + url
        + "/"
    )

    # name: [id, type, TC, FC, label]
    nodes = {}
    # src@tar = [src_id, tar_id, type]
    edges = {}
    # script_dic = {'https://ad/test.js@method': [set->[_gid,..], get->[_svd, ..]]}
    script_dic = {}
    # storage_dic = {'_gid' = ["cookie getter/setter",002, 5288992, 1], '_svd' = ["storage getter/setter",5]}
    storage_dic = {}

    # initial HTML iframe
    src = addNode(nodes, "Network@https://www." + url + "/", "Network", 0, 0, -1)
    tar = addNode(nodes, "HTML@https://www." + url + "/", "HTML@iframe", 0, 0, -2)
    addEdge(edges, src, tar, "Network->HTML/Script")
    src = addNode(nodes, "Script@https://" + url + "/", "Script", 0, 0, 0)
    addEdge(edges, tar, src, "Initiated")

    # creating storage nodes and edges
    with open(folder + "cookie_storage.json") as file:
        for line in file:
            dataset = json.loads(line)
            if url in dataset["top_level_url"]:
                addStorage(script_dic, storage_dic, dataset)
    for key in storage_dic:
        addNode(nodes, "Storage@" + key, "Storage", 0, 0, -3)

    # creating edges btw script method and storage nodes
    for key in script_dic:
        if key is not None:
            src = addNode(nodes, "Script@" + key.split("@")[0], "Script", 0, 0, 0)
            src2 = addNode(nodes, "ScriptMethod@" + key, "ScriptMethod", 0, 0, 0)
            # adding script and method relationship
            addEdge(edges, src, src2, "partof")
            # adding cookie setter and method realtionship
            for item in script_dic[key][0]:
                addEdge(edges, src2, nodes["Storage@" + item][0], "Storage Setter")
            # adding cookie getter and method realtionship
            for item in script_dic[key][0]:
                addEdge(edges, nodes["Storage@" + item][0], src2, "Storage Getter")

    # cookie set/get by inline JavaScript
    if "https://www." + url + "/" in script_dic.keys():
        for cookie_set in script_dic["https://www." + url + "/"][0]:
            addEdge(
                edges,
                nodes["HTML@" + "https://www." + url + "/"][0],
                nodes["Storage@" + cookie_set][0],
                "Storage Setter",
            )
        for cookie_get in script_dic["https://www." + url + "/"][1]:
            addEdge(
                edges,
                nodes["Storage@" + cookie_get][0],
                nodes["HTML@" + "https://www." + url + "/"][0],
                "Storage Getter",
            )

    # reading big request data line by line
    with open(folder + "label_request.json") as file:
        for line in file:
            data = json.loads(line)
            for dataset in data:
                ######### Single request level graph plotting #########
                # check to ensure graph is for one page
                # create network node
                src = addNode(
                    nodes, "Network@" + dataset["http_req"], "Network", 0, 0, -1
                )

                # check if request is redirected
                rdurl = getRedirection(
                    dataset["request_id"], dataset["http_req"], folder
                )
                if rdurl is not None:
                    tar = addNode(nodes, "Network@" + rdurl, "Network", 0, 0, -1)
                    addEdge(edges, src, tar, "Redirection")

                # if request setting up any cookie
                lst = getReqCookie(dataset["request_id"], folder)
                for item in lst:
                    lst1 = item.split(";")
                    for item1 in lst1:
                        # update the storage dictionary
                        keys = getStorageDic(storage_dic, item1.split("=")[0])
                        tar = addNode(nodes, "Storage@" + keys, "Storage", 0, 0, -3)
                        storage_dic[keys].append(item1.split("=")[1])
                        # add html and storage node
                        addEdge(edges, src, tar, "Storage Setter")

                # check if resource type is not script then create simple HTML node
                if dataset["resource_type"] != "Script":
                    tar = addNode(
                        nodes,
                        "HTML@" + dataset["http_req"],
                        "HTML@" + dataset["resource_type"],
                        0,
                        0,
                        -2,
                    )
                    addEdge(edges, src, tar, "Network->HTML")
                # create script node
                else:
                    if (
                        dataset["easylistflag"] == 1
                        or dataset["easyprivacylistflag"] == 1
                        or dataset["ancestorflag"] == 1
                    ):
                        tar = addNode(
                            nodes,
                            "Script@" + dataset["http_req"],
                            dataset["resource_type"],
                            0,
                            0,
                            1,
                        )
                    else:
                        tar = addNode(
                            nodes,
                            "Script@" + dataset["http_req"],
                            dataset["resource_type"],
                            0,
                            0,
                            0,
                        )
                    # create edge between the Request -> HTML/Script
                    addEdge(edges, src, tar, "Network->Script")

                # if its initiated by call stack javascript
                # else its generated from main iframe
                if (
                    dataset["call_stack"]["type"] == "script"
                    and "HTML@" + getInitiatorURL(dataset["call_stack"]["stack"])
                    not in nodes.keys()
                ):
                    if (
                        dataset["easylistflag"] == 1
                        or dataset["easyprivacylistflag"] == 1
                        or dataset["ancestorflag"] == 1
                    ):
                        tar = addNode(
                            nodes,
                            "ScriptMethod@"
                            + getInitiator(dataset["call_stack"]["stack"]),
                            "ScriptMethod",
                            1,
                            0,
                            0,
                        )
                        tar2 = addNode(
                            nodes,
                            "Script@" + getInitiatorURL(dataset["call_stack"]["stack"]),
                            "Script",
                            1,
                            0,
                            0,
                        )
                    else:
                        tar = addNode(
                            nodes,
                            "ScriptMethod@"
                            + getInitiator(dataset["call_stack"]["stack"]),
                            "ScriptMethod",
                            0,
                            1,
                            0,
                        )
                        tar2 = addNode(
                            nodes,
                            "Script@" + getInitiatorURL(dataset["call_stack"]["stack"]),
                            "Script",
                            0,
                            1,
                            0,
                        )
                    addEdge(edges, tar, src, "Initiated")
                    addEdge(edges, tar2, tar, "partof")
                else:
                    addEdge(
                        edges,
                        nodes["HTML@https://www." + url + "/"][0],
                        src,
                        "Initiated",
                    )

                # # Links between storage nodes and script [setter, getter]
                # if dataset["http_req"] in script_dic.keys():
                #     # script -> setter
                #     if len(script_dic[dataset["http_req"]][0]) != 0:
                #         for item in script_dic[dataset["http_req"]][0]:
                #             addEdge(
                #                 edges,
                #                 nodes["Script@" + dataset["http_req"]][0],
                #                 nodes["Storage@" + item][0],
                #                 "Storage Setter",
                #             )
                #     # getter -> script
                #     if len(script_dic[dataset["http_req"]][1]) != 0:
                #         for item in script_dic[dataset["http_req"]][1]:
                #             addEdge(
                #                 edges,
                #                 nodes["Storage@" + item][0],
                #                 nodes["Script@" + dataset["http_req"]][0],
                #                 "Storage Getter",
                #             )

                # if url has storage info
                val = IsInfoShared(storage_dic, dataset["http_req"])
                if val is not None:
                    addEdge(edges, nodes["Storage@" + val][0], src, "Info Shared")

    json.dump(nodes, open(folder + "nodes.json", "w"))
    json.dump(edges, open(folder + "edges.json", "w"))

    """

    """
    features = {}

    """

    """
    label = {}

    for nod in nodes:
        # only script nodes in the features
        if nodes[nod][1] == "Script":
            if nodes[nod][0] not in nodes.keys():
                # 0: script_url, 1: count of nodes, 2: count of edges, 3: in edges, 4: out edges, 5: get localstorage, 6: set localstorage, 7: get cookie, 8: set cookie, 9: has webpack keyword
                features[nodes[nod][0]] = [
                    nod.split("@")[1],
                    len(nodes),
                    len(edges),
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    findWordInScript(nod.split("@")[1], "webpack"),
                ]

    adjEdges = {}
    # incrementing in/out edges
    for edg in edges:
        # if its script node or not
        if edges[edg][0] in features.keys():
            # src: increment out edge
            features[edges[edg][0]][4] += 1
        # if its script node or not
        if edges[edg][1] in features.keys():
            # tar: increment in edge
            features[edges[edg][1]][3] += 1

        # making adjacency list src -> tar
        if edges[edg][0] not in adjEdges.keys():
            adjEdges[edges[edg][0]] = []
        adjEdges[edges[edg][0]].append(edges[edg][1])

    # incrementing get/set localstorage and cookie
    for script in script_dic:
        if script is not None:
            if "Script@" + script in nodes.keys():
                # setters
                for ids in script_dic[script][0]:
                    if storage_dic[ids][0] == "cookie_setter":
                        features[nodes["Script@" + script][0]][8] += 1
                    else:
                        features[nodes["Script@" + script][0]][6] += 1
                # getter
                for ids in script_dic[script][0]:
                    if storage_dic[ids][0] == "cookie_getter":
                        features[nodes["Script@" + script][0]][7] += 1
                    else:
                        features[nodes["Script@" + script][0]][5] += 1

    json.dump(features, open(folder + "features.json", "w"))
    json.dump(script_dic, open(folder + "script.json", "w"))
    json.dump(adjEdges, open(folder + "adjEdges.json", "w"))

    visited = {}
    count = [0]
    print(getDecendantsCount(21, adjEdges, visited, count))
    print(count)
    print(
        findWordInScript(
            "https://www.awxcdn.com/adc-assets/bundles/604.84bbfe709eb7f5136494.js",
            "webpack",
        )
    )
