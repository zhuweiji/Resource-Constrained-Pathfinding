import heapq
from os import path
import json
from pathlib import Path

from utils.utils import timeit, progress_display

cwd = Path(__file__).parent.resolve()
data_dir = cwd / 'data'

with open(data_dir / 'G.json') as graph_data:
    graphdict = json.load(graph_data)

with open(data_dir / 'Dist.json') as dist_data:
    distancedict = json.load(dist_data)

with open(data_dir / 'Cost.json') as cost_data:
    costdict = json.load(cost_data)

print('import complete')

@timeit
def uniform_cost_search(graph, start, target):
    # initialize nodes to have properties 1. g(n) (distance), 2. g(n) (cost) and 2. shortest path to that node thus far
    for node in graph:
        graph[node] = [graph[node], None, []]

    # create a heap of nodes to be explored next, ordered by path cost to that node
    # properties: 1.path cost g(n), 2. node id, 3. previous node
    queue = [(0, start, None)]

    # set the source node to have path cost of 0, and path to it = [] (its the starting node)
    graph[start][1:] = 0, []

    explored_nodes = set()

    # create a logger that logs a message every n iterations for user feedback 
    logger = progress_display(log_every=10000)

    while queue:
        dist_to_curr, current_node, previous_node = heapq.heappop(queue)  # get a node with smallest g(n) from the queue
        neighbours, dist_to_curr2, path_to_curr = graph[current_node]     # get neighbouring nodes and path to current node (path does not include current node)

        path_to_neighbours = [*path_to_curr, current_node]

        explored_nodes.add(current_node) # since UCS guarantees that every node explored has the shortest possible path from source, we can discard the node from future exploration
        
        for node in neighbours:
            if node in explored_nodes:
                continue

            edge_key = f'{current_node},{node}'     # key to access an edge's properties in the json data file provided
            
            edge_distance = distancedict[edge_key]  
            dist_to_neighbour = dist_to_curr + edge_distance    # calculate the g(n) of neighbouring nodes of the currently explored node to add them to the queue

            # while technically not exploring the neighbour nodes, since we calculated g(n) and path to the node already, we can just store the information
            graph[node][1:] = dist_to_neighbour, path_to_neighbours

            if node == target:
                logger(True)
                return dist_to_neighbour, path_to_neighbours   
            
            heapq.heappush(queue, (dist_to_neighbour, node, current_node)) 
                
        logger()


if __name__ == "__main__":
    distance, path = uniform_cost_search(graphdict, '1', '50')

    path = "->".join(path)
    print()
    print(f"{distance=}\n{path=}")
