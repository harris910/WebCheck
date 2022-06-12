# This file contains the logic to add edges and nodes in the graph of the webpage.

def addNode(nodes, name, type, TC, FC, classlabel, label):
  if name not in nodes.keys():
    nodes[name] = [label[0], type, 0, 0, classlabel]
    label[0] += 1
  if classlabel == 0:
    nodes[name][2] += TC
    nodes[name][3] += FC
  return nodes[name][0]

def addEdge(edges, src, tar, type):
  if str(src)+'@'+str(tar) not in edges.keys():
    edges[str(src)+'@'+str(tar)] = [src, tar, type]