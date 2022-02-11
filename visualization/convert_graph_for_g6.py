import json
from pathlib import Path
import networkx as nx

cwd = Path.cwd()
g_filepath     = cwd / 'G.json'
cost_filepath  = cwd / 'Cost.json'
coord_filepath = cwd /'Coord.json'
dist_filepath  = cwd / 'Dist.json'

outpath = cwd / 'out.gexf'

with open(g_filepath, 'r') as f:
    graph = json.load(f)
with open(cost_filepath, 'r') as f:
    cost = json.load(f)
with open(coord_filepath, 'r') as f:
    coord = json.load(f)
with open(dist_filepath, 'r') as f:
    dist = json.load(f)

graph = nx.from_dict_of_lists(graph)

for edge in cost.keys():
    src,tgt = list(map(str.strip, edge.split(',')))
    _cost = cost[edge]
    graph[src][tgt]['cost'] = _cost
for edge in dist.keys():
    src,tgt = list(map(str.strip, edge.split(',')))
    _dist = dist[edge]
    graph[src][tgt]['weight'] = _dist
for node in coord:
    x,y = coord[node]
    graph.nodes[node]['coords'] = ','.join(list(map(str,[x,y])))

print(graph.nodes['1'])
nx.write_gexf(graph, path=outpath)
# print('starting')
# graph = nx.read_gml(path=outpath)
# print('finished import')
# print(graph.nodes['1'])

