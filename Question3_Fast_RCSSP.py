import heapq
import json
import math
from pathlib import Path

from utils.utils import timeit, progress_display
from utils.utils import timeit, progress_display
from Question2_BestFirstSearch import bestFirstSearch

GLOBAL_ITERATIONS = 0

@timeit
def a_star_search(graph, distancecosts, energycosts, coords, start, target):
    graph = graph.copy()   
    distancecosts = distancecosts.copy()   
    energycosts = energycosts.copy() 
    coords = coords.copy()  

    global GLOBAL_ITERATIONS
    result = {'distance': None,'energy': None, 'path': None}
    
    tgt_x, tgt_y = coords[target]
    h = lambda x1,y1: math.sqrt( (x1-tgt_x)**2 + (y1-tgt_y)**2 )
    explored_nodes = set()

    # f cost, distance g cost, energy g cost, current node, path to current node
    queue = [(h(*coords[start]), 0, 0, start, [])]

    logger = progress_display(log_every=10000)

    while queue:   
        GLOBAL_ITERATIONS+=1
        logger()
        f_to_current, distance_to_current, energy_to_current, current_node, path_to_current = heapq.heappop(queue)
        neighbours = graph[current_node]
        path_to_neighbour = [*path_to_current, current_node]
        explored_nodes.add(current_node)
        
        for node in neighbours:
            if node in explored_nodes:
                continue
            edge_key = f'{current_node},{node}'
            node_x, node_y = coords[node]

            distance_to_neighbour = distance_to_current + distancecosts[edge_key]
            f_cost = distance_to_neighbour + h(node_x, node_y)
            energy_to_neighbour = energy_to_current + energycosts[edge_key]

            if node == target:
                result['distance'] = distance_to_neighbour
                result['energy'] = energy_to_neighbour
                result['path'] = path_to_neighbour
                return result

            heapq.heappush(queue, (f_cost, distance_to_neighbour, energy_to_neighbour, node, path_to_neighbour))
    return result


def shortest_energy_cost_path(graph, distancecosts, energycosts, start, target):
    graph = graph.copy()
    distancecosts = distancecosts.copy()
    energycosts  = energycosts.copy()
    
    global GLOBAL_ITERATIONS
    result = {'distance': None, 'energy': None, 'path': None}

    queue = [(0,0,start,[])]
    nodes_explored = set()
    while queue:
        GLOBAL_ITERATIONS+=1
        energy_to_current, distance_to_current, current_node, path_to_current = heapq.heappop(queue)
        nodes_explored.add(current_node)

        neighbours = graph[current_node]
        path_to_neighbour = [*path_to_current, current_node]

        for node in neighbours:
            if node in nodes_explored: continue

            edge_key = f'{current_node},{node}'
            energy_to_neighbour = energy_to_current + energycosts[edge_key]
            distance_to_neighbour = distance_to_current + distancecosts[edge_key]
            
            if node == target:
                result['distance'] = distance_to_neighbour
                result['energy'] = energy_to_neighbour
                result['path'] = path_to_neighbour
                return result

            heapq.heappush(queue, (energy_to_neighbour, distance_to_neighbour, node, path_to_neighbour))

@timeit
def fast_rcspp(graph, distancecosts, energycosts, coords, start, target, max_energy_cost=287932):
    global GLOBAL_ITERATIONS
    result = {'distance': None, 'energy': None, 'path': None}

    a_star_result = a_star_search(graph=graphdict, distancecosts=distancedict,
                                  energycosts=costdict, coords=coords, start=start, target=target,)

    if a_star_result['energy'] <= max_energy_cost:
        return a_star_result
    
    edge_key = lambda src, tgt: f'{src},{tgt}'
    a_star_energy, a_star_distance, a_star_path = a_star_result['energy'], a_star_result['distance'], a_star_result['path']
    
    last_node = a_star_path.pop(-1)
    a_star_energy = a_star_energy - energycosts[edge_key(last_node, target)]
    a_star_distance = a_star_distance - distancecosts[edge_key(last_node, target)]
    
    while True:
        GLOBAL_ITERATIONS+=1
        as_end_node = a_star_path.pop(-1)
        a_star_energy = a_star_energy - energycosts[edge_key(as_end_node, last_node)]
        a_star_distance = a_star_distance - distancecosts[edge_key(as_end_node, last_node)]
        
        last_result = shortest_energy_cost_path(graph, distancecosts, energycosts, as_end_node, target)
        net_energy = a_star_energy + last_result['energy']

        if net_energy <= max_energy_cost:
            result['distance'] = last_result['distance'] + a_star_distance
            result['energy'] = net_energy
            result['path'] = [*a_star_path, *last_result['path']]
            return result

        last_node = as_end_node

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

    res = fast_rcspp(graph=graphdict, distancecosts=distancedict,
            energycosts=costdict, coords=coordsdict, start='1', target='50',)
    dist, energy, path = res['distance'], res['energy'], res['path']
    print('-'*50)
    print(f'Completed with {GLOBAL_ITERATIONS} iterations')
    print(f'dist={dist=}')
    print(f'energy={energy=}')
    path = "->".join(path)
    print(f'{path=}')

