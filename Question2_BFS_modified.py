import heapq
import json
from pathlib import Path

from utils.utils import timeit, progress_display

@timeit
def BFS_all_edges(graph, start, target, max_energy_cost=287932):
    graph = graph.copy()
    
    for node in graph:
        graph[node] = [graph[node], None, []]

    queue = [(0, start)]
    explored_edge_list = set() 
    graph[start][1:] = 0, []
    final_path = None

    node_count = 0

    logger = progress_display(log_every=10000)
    while queue:
        logger()

        dist, current_node = heapq.heappop(queue)
        neighbours, distance_to_curr, path_to_curr = graph[current_node]

        for neighbour in neighbours:
            full_dist_to_neighbour, full_path_to_neighbour = graph[neighbour][1:]
            edge = ','.join([current_node, neighbour])
            edge_distance = distancedict[edge]

            distance_changed = False
            new_distance = distance_to_curr + edge_distance

            if full_dist_to_neighbour is None or new_distance < full_dist_to_neighbour:
                graph[neighbour][1:] = new_distance, [*path_to_curr, current_node]
                distance_changed = True

                if neighbour == target:
                    possible_final_path = [*path_to_curr, current_node, neighbour]
                    energy_cost=0
                    for i in range(len(possible_final_path)-1):
                        key = ','.join([possible_final_path[i], possible_final_path[i+1]])
                        energy_cost += costdict[key]
                    if energy_cost < max_energy_cost:
                        final_path = [*path_to_curr, current_node, neighbour]
                        print('\n',final_path, energy_cost)

            if edge not in explored_edge_list or distance_changed:
                heapq.heappush(queue, (edge_distance, neighbour))

            explored_edge_list.add(edge)
    
    logger(True)
    return final_path


if __name__ == "__main__":
    cwd = Path.cwd()
    data_dir = cwd / 'data'

    with open(data_dir / 'G.json') as graph_data:
        graphdict = json.load(graph_data)

    with open(data_dir / 'Dist.json') as dist_data:
        distancedict = json.load(dist_data)

    with open(data_dir / 'Cost.json') as cost_data:
        costdict = json.load(cost_data)

    print('import complete')

    distance, path = BFS_all_edges(graphdict, '1', '50')

    path = "->".join(path)
    print()
    print(f"{distance=}\n{path=}")
