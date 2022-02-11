import json

with open('G.json') as graph_data:
    graphdict = json.load(graph_data)

with open('Dist.json') as dist_data:
    distancedict = json.load(dist_data)

with open('Cost.json') as cost_data:
    costdict = json.load(cost_data)


"""
"""


def BFS(graphdict, start):
    for key in graphdict:
        graphdict[key] = [graphdict[key], 0, []]
 
    queue = [start]
    explored = []

    graphdict[start][1:] = 0, []
    while queue:
        current_node = queue.pop(0)
        if current_node not in explored:
            for possible_node in graphdict[current_node][0]:
                tempdist = 0
                key = ','.join([possible_node,current_node])
                tempdist = graphdict[current_node][1] + distancedict[key]
                queue.append(possible_node)

                if (graphdict[possible_node][1] > tempdist):
                    path_to_curr_node = graphdict[current_node][2][:]
                    path_to_curr_node.append(current_node)
                    graphdict[possible_node][1:] = tempdist, path_to_curr_node

                elif (graphdict[possible_node][1]==0):
                    path_to_curr_node = graphdict[current_node][2][:]
                    path_to_curr_node.append(current_node)
                    graphdict[possible_node][1:] = tempdist, path_to_curr_node
                else:
                    continue
        else:
            continue
    

        explored.append(current_node)
        return graphdict
                

    #     if current_node == goal:
    #         shortest_path = graphdict[goal][2]
    #         shortest_path.append('50')
    #         total_distance = 0
    #         total_cost = 0
    #         for start_index in range(len(shortest_path)-1):
    #             end_index = start_index + 1
    #             key = ','.join([shortest_path[start_index], shortest_path[end_index]])
    #             total_distance += distancedict[key]
    #             total_cost += costdict[key]

    #         if total_cost<energy_budget:
    #             pres_path = "->".join(shortest_path)
    #             pres_path = "S->" + pres_path + "->T"
    #             pres_dist = "Shortest Distance:",total_distance
    #             pres_cost = "Total Energy Cost:",total_cost
    #             return pres_path, pres_dist,pres_cost

    # return -1

def getresult (graphdict, goal, energy_budget=287932):
    shortest_path = graphdict[goal][2]
    print(type(shortest_path))
    shortest_path.append('50')
    total_distance = 0
    total_cost = 0

    for start_index in range(len(shortest_path)-1):
        end_index = start_index + 1
        key = ','.join([shortest_path[start_index], shortest_path[end_index]])
        total_distance += distancedict[key]
        total_cost += costdict[key]

    if total_cost<energy_budget:
        pres_path = "->".join(shortest_path)
        pres_path = "S->" + pres_path + "->T"
        pres_dist = "Shortest Distance:",total_distance
        pres_cost = "Total Energy Cost:",total_cost

        return pres_path, pres_dist,pres_cost



# graphdict = BFS(graphdict,'1')
# shortestpath, shortestdistance, cost = getresult(graphdict, '50')
# print(shortestpath)
# print(shortestdistance)
# print(cost)
