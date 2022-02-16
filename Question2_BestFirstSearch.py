import heapq
import json
from pathlib import Path

from utils.utils import timeit, progress_display

@timeit
def bestFirstSearch(graph, distancecosts, energycosts, start, target, energy_weight=1, distance_weight=1, max_energy_cost=287932):
    logger = progress_display(log_every=10000)

    graph = {k:v for k,v in graph.items()}

    avg_distance = sum(distancecosts.values()) / len(distancecosts)
    avg_energy   = sum(energycosts.values()) / len(distancecosts)

    normalised_cost = lambda prev_norm_cost, energy, dist: prev_norm_cost + distance_weight*(dist/avg_distance) + energy_weight*(energy/avg_energy)
    
    # adj nodes, distance to the node, cost to the node
    for node in graph:
        graph[node] = [graph[node], None, None, []]

    # normalised cost, current node
    queue = [(0, start)]

    graph[start][1:] = 0, 0, []

    explored_nodes = set()
    while queue:
        cost_to_curr, current_node = heapq.heappop(queue)
        neighbours, total_dist_to_curr, total_energy_to_curr, path_to_curr = graph[current_node]
        path_to_neighbour = [*path_to_curr, current_node]

        explored_nodes.add(current_node)  # since UCS guarantees that every node explored has the shortest possible path from source, we can discard the node from future exploration

        for node in neighbours:
            try:
                if node in explored_nodes:
                    continue    
            except TypeError as E:
                print(node)
                raise E

            # key to access an edge's properties in the json data file provided
            edge_key = f'{current_node},{node}'

            edge_distance, edge_energy = distancecosts[edge_key], energycosts[edge_key]
            dist_to_neighbour, energy_to_neighbour = total_dist_to_curr + edge_distance, total_energy_to_curr + edge_energy

            if energy_to_neighbour > max_energy_cost:
                continue 

            if node == target:
                logger(True)
                return dist_to_neighbour, energy_to_neighbour, path_to_neighbour

            graph[node][1:] = dist_to_neighbour, energy_to_neighbour, path_to_neighbour
            
            # calculate the g(n) of neighbouring nodes of the currently explored node to add them to the queue
            cost_to_neighbour = normalised_cost(cost_to_curr, edge_distance, edge_energy)

            heapq.heappush(queue, (cost_to_neighbour, node))
        logger()

if __name__ == "__main__":
    cwd = Path(__file__).parent.resolve()
    data_dir = cwd / 'data'

    with open(data_dir / 'G.json') as graph_data:
        graphdict = json.load(graph_data)

    with open(data_dir / 'Dist.json') as dist_data:
        distancedict = json.load(dist_data)

    with open(data_dir / 'Cost.json') as cost_data:
        costdict = json.load(cost_data)

    print('import complete')

    print('Params optimised for distance\n','-'*50)
    dist, energy, path = bestFirstSearch(graphdict, distancedict, costdict, '1', '50', energy_weight=11, distance_weight=1)
    path = "->".join(path)
    print()
    print(f"{dist=}\n{energy=}\n{path=}")
    print('\n')
    print('Params optimised for energy\n', '-'*50)
    dist, energy, path = bestFirstSearch(graphdict, distancedict, costdict, '1', '50', energy_weight=1, distance_weight=6)
    path = "->".join(path)
    print()
    print(f"{dist=}\n{energy=}\n{path=}")

    


