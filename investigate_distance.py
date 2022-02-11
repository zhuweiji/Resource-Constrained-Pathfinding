import json
import math
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
with open(coord_filepath, 'r') as f:
    coord = json.load(f)
with open(dist_filepath, 'r') as f:
    dist = json.load(f)

def str_line_dist(x1,x2,y1,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def variance(data, ddof=0):
    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - ddof)

def stdev(data):
    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev


print('n point distance calculation')

gt_errors = []
lt_errors = []
counter = 0
for src_node in graph:
    counter += 1
    if counter % 10000 == 0:
        print(f'{counter}/{len(graph)}')
    first_tgt = graph[src_node][0]

    sx,sy = coord[src_node]
    tx,ty = coord[first_tgt]
    calc_dist = str_line_dist(sx,tx,sy,ty)

    distance_given = dist[','.join([src_node, first_tgt])]
    error= distance_given - calc_dist
    if error < 0:
        lt_errors.append(error)
        print(src_node, first_tgt)
        print(f'{error=}')
    elif error > 1:
        gt_errors.append(error)

print('\n')
print('Percentage of distance errors, error > 1')
print('='*50)
print(len(gt_errors)/len(graph), len(gt_errors))
print('mean:',sum(gt_errors)/len(gt_errors),'stdev', stdev(gt_errors))
print()
print(sorted(gt_errors, reverse=True)[:10])
print('Percentage of distance errors, error < 0')
print('='*50)
print(len(lt_errors)/len(graph), len(lt_errors))
print()
print('Avg value of distance in graph')
print(sum(dist.values())/len(graph))