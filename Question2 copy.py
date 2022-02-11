import heapq
from os import path
import json
with open(r'C:\Users\zhuwe\OneDrive\Desktop\VS Code Environment\CZ3005\G.json') as graph_data:
    graphdict = json.load(graph_data)

with open(r'C:\Users\zhuwe\OneDrive\Desktop\VS Code Environment\CZ3005\Dist.json') as dist_data:
    distancedict = json.load(dist_data)

with open(r'C:\Users\zhuwe\OneDrive\Desktop\VS Code Environment\CZ3005\Cost.json') as cost_data:
    costdict = json.load(cost_data)

def progress_display(log_every:int=10000,total_count:int=None):
    """Helper function to display a message every {log_every} iterations"""
    index = 0
    def display_updater():
        nonlocal index
        index+=1
        if index % log_every == 0:
            print(f'{index}           \r', end=' ')
    return display_updater

def BFS_all_edges(graph, start, target, max_energy_cost=287932):
    # initialize nodes to have properties 1. g(n) (distance) and 2. shortest path to that node thus far 
    for node in graph:
        graph[node] = [graph[node], None, []]

    # create a heap of nodes to be explored next, ordered by path cost to that node
    # properties: 1.path cost, 2. node id, 3. previous node
    queue = [(0, start, None)]
    explored_edge_list = set() # maintain a list of explored edges, which may need to be traversed again
    
    # set the source node to have path cost of 0 and path to it = [] (its the starting node)
    graph[start][1:] = 0, []
    final_path = None

    node_count = 0

    display_update = progress_display(log_every=10000)
    nc = 0
    while queue and nc<50:
        nc+=1
        # display progress of the traversal
        display_update()

        print(queue)
        # should put in g(n) into the queue instead of weight of edge from src->next node
        dist, current_node, previous_node = heapq.heappop(queue)
        neighbours, distance_to_curr, path_to_curr = graph[current_node]
        print(current_node,distance_to_curr)


        for neighbour in neighbours:
            if neighbour == previous_node:
                continue

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
                heapq.heappush(queue, (edge_distance, neighbour, current_node))

            explored_edge_list.add(edge)

    return final_path


BFS_all_edges(graphdict, '1', '50')
