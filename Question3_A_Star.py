import heapq
import json
import math
from pathlib import Path

from utils.utils import timeit, progress_display
from utils.utils import timeit, progress_display
from Question2_BestFirstSearch import bestFirstSearch

GLOBAL_ITERATIONS = 0

@timeit
def a_star_search(graph, distancecosts, energycosts, coords, start, target, max_energy_cost=287932):
    graph = graph.copy()
    distancecosts = distancecosts.copy()
    energycosts = energycosts.copy()
    coords = coords.copy()
    global GLOBAL_ITERATIONS
    result = {'distance': None,'energy': None, 'path': None}
    
    tgt_x, tgt_y = coords[target]
    h = lambda x1,y1: math.sqrt( (x1-tgt_x)**2 + (y1-tgt_y)**2 )

    explored_edges = set()

    # f cost, distance g cost, energy g cost, current node, path to current node
    queue = [(h(*coords[start]), 0, 0, start, [])]

    logger = progress_display(log_every=10000)

    while queue :   
        GLOBAL_ITERATIONS+=1
        logger()
        f_to_current, distance_to_current, energy_to_current, current_node, path_to_current = heapq.heappop(queue)
        neighbours = graph[current_node]
        path_to_neighbour = [*path_to_current, current_node]
        for node in neighbours:
            edge_key = f'{current_node},{node}'
            if edge_key in explored_edges: continue
            
            explored_edges.add(edge_key)

            node_x, node_y = coords[node]

            distance_to_neighbour = distance_to_current + distancecosts[edge_key]
            f_cost = distance_to_neighbour + h(node_x, node_y)
            energy_to_neighbour = energy_to_current + energycosts[edge_key]

            if energy_to_neighbour > max_energy_cost: continue

            if node == target:
                logger(True)
                result['distance'] = distance_to_neighbour
                result['energy'] = energy_to_neighbour
                result['path'] = path_to_neighbour
                return result

            heapq.heappush(queue, (f_cost, distance_to_neighbour, energy_to_neighbour, node, path_to_neighbour))
    return result


if __name__ == "__main__":
    cwd = Path.cwd()
    data_dir = cwd / 'data'

    with open(data_dir / 'G.json') as f:
        graphdict = json.load(f)

    with open(data_dir / 'Dist.json') as f:
        distancedict = json.load(f)

    with open(data_dir / 'Cost.json') as f:
        costdict = json.load(f)

    with open(data_dir / 'Coord.json') as f:
        coordsdict = json.load(f)

    print('import complete')



    res = a_star_search(graph=graphdict, distancecosts=distancedict,
            energycosts=costdict, coords=coordsdict, start='1', target='50',)
    
    dist, energy, path = res['distance'], res['energy'], res['path']
    print('-'*50)
    print(f'dist={dist=}')
    print(f'energy={energy=}')
    path = "->".join(path)
    print(f'{path=}')

