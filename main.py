import json
import math
from operator import itemgetter
import time

import json
from pathlib import Path

cwd = Path.cwd()
data_dir = cwd / 'data'

with open(data_dir / 'G.json') as f:
    graph = json.load(f)

with open(data_dir / 'Dist.json') as f:
    distance = json.load(f)

with open(data_dir / 'Cost.json') as f:
    cost = json.load(f)

with open(data_dir / 'Coord.json') as f:
    coord = json.load(f)


ENERGY_LIMIT = 287932
START_COORDINATE = "1"
START_X = coord[START_COORDINATE][0]
START_Y = coord[START_COORDINATE][1]
FINAL_COORDINATE = "50"
FINAL_X = coord[FINAL_COORDINATE][0]
FINAL_Y = coord[FINAL_COORDINATE][1]

def pythagoras(first):
    # print(first)
    return math.sqrt(((FINAL_X-first[0])**2)+((FINAL_Y-first[1])**2))

def shortest_path_generator(path):
    shortest_path_arrow = ""
    for i in path:
        if i == FINAL_COORDINATE:
            shortest_path_arrow += i
        else:
            shortest_path_arrow += i + "->"
    return shortest_path_arrow

def main():
    print("Task 1:")
    ############################### Task 1 ############################################################################
    possible_list = [(START_COORDINATE, 0)]
    expanded = set()  # set of expanded nodes

    path_dict = {"1": [[["1"], 0]]}

    while len(possible_list) != 0:
        current_node = possible_list[0][0]
        possible_list.pop(0)

        if current_node != FINAL_COORDINATE:
            for i in graph[current_node]:
                if i not in expanded:
                    for node_hist in range(len(path_dict[current_node])):
                        i_pair = current_node + "," + i
                        i_dist = distance[i_pair] + path_dict[current_node][node_hist][1]

                        i_path = path_dict[current_node][node_hist][0].copy()
                        i_path.append(i)

                        if i in path_dict:
                            path_dict[i].append([i_path, i_dist])

                        else:
                            path_dict[i] = [[i_path, i_dist]]

                        # remove extra combinations such that a maximum of 2 is left
                        if len(path_dict[i]) > 1:
                            min_dist = path_dict[i][0][1]
                            min_index = 0
                            for node_combi in range(1, len(path_dict[i])):
                                if path_dict[i][node_combi][1] < min_dist:
                                    min_index = node_combi
                                    min_dist = path_dict[i][node_combi][1]

                            for node_combi in range(1, len(path_dict[i])):
                                if node_combi != min_index:
                                    del_combi = path_dict[i][min_index]
                                    del_tuple = (i, path_dict[i][1])
                                    if del_tuple in possible_list:
                                        possible_list.remove(del_tuple)

                            new_combi = path_dict[i][min_index].copy()
                            path_dict[i] = [new_combi]

                    i_tuple = (i, i_dist)
                    if i_tuple not in possible_list:
                        possible_list.append(i_tuple)

            expanded.add(current_node)
        possible_list.sort(key=itemgetter(1))

    shortest_dist = path_dict[FINAL_COORDINATE][0][1]
    shortest_index = 0
    if len(path_dict[FINAL_COORDINATE]) > 1:
        if path_dict[FINAL_COORDINATE][1][1] < shortest_dist:
            shortest_dist = path_dict[FINAL_COORDINATE][1][1]
            shortest_index = 1

    shortest_path = shortest_path_generator(path_dict[FINAL_COORDINATE][shortest_index][0])

    print(f"Shortest Path: {shortest_path}")
    print("Shortest distance: %s." % shortest_dist)
    print()
    ###################################################################################################################
    print("Task 2:")
    # time_2_now = time.time()
    current = START_COORDINATE
    old_list = []
    possible_list = [(START_COORDINATE, 0)]
    # COUNT = 0

    # path_dict = {number: [[path from "1" to the number], total energy, accumulated distance]}
    path_dict = {"1": [
        [["1"], 0, 0]
        ]}
    # while(current!=FINAL_COORDINATE or path_dict["50"][1] > ENERGY_LIMIT):
    while (current != FINAL_COORDINATE):
        # if COUNT%10 == 0:
        #     input("Enter to continue:")

        if current == FINAL_COORDINATE:
            possible_list.pop(0)
        else:
            # COUNT += 1
            # print("Iteration Number "+str(COUNT) + ":")
            # print("Node Number: " + current)
            possible_list.pop(0)
            old_list.append(current)
            # print(f"Possible List after pop: {possible_list}")

            for i in graph[current]:
                if i not in old_list:
                    for node_hist in range(len(path_dict[current])):
                        i_coord = current + "," + i
                        i_cost = cost[i_coord] + path_dict[current][node_hist][1]

                        if i_cost <= ENERGY_LIMIT:
                            # append path_dict[i] with new combination of distance and cost
                            # print("Debug: " + str(path_dict[current][node_hist]))
                            # print("Debug: " + str(path_dict[current][node_hist][0]))

                            i_path = path_dict[current][node_hist][0].copy()
                            i_path.append(i)
                            # print("Debug: " + str(i_path))
                            i_accu = path_dict[current][node_hist][2] + distance[i_coord]

                            i_tuple = (i, i_accu)

                            # check if the node was previously in the dict
                            if i in path_dict:
                                path_dict[i].append([i_path, i_cost, i_accu])
                                # print("Repeated")
                                # print(i + ":" + str(path_dict[i]))

                            else:
                                path_dict[i] = [[i_path, i_cost, i_accu]]

                            # remove extra combinations such that a maximum of 2 is left
                            # (Scenario 1) lowest total distance and lowest total cost
                            # (Scenario 2) lowest total distance or lowest total cost
                            if len(path_dict[i]) != 1:
                                start_total_dist = path_dict[i][0][2]
                                start_total_energy = path_dict[i][0][1]
                                start_dist_index = 0
                                start_cost_index = 0
                                for node_combi in range(1, len(path_dict[i])):
                                    if start_total_dist > path_dict[i][node_combi][2]:
                                        start_dist_index = node_combi
                                        start_total_dist = path_dict[i][node_combi][2]
                                    if start_total_energy > path_dict[i][node_combi][1]:
                                        start_cost_index = node_combi
                                        start_total_energy = path_dict[i][node_combi][1]

                                # Remove not needed combinations in Possible List
                                for combi_num in range(len(path_dict[i])):
                                    if combi_num != start_dist_index or combi_num != start_cost_index:
                                        del_tuple = (i, path_dict[i][combi_num][2])
                                        if del_tuple in possible_list:
                                            possible_list.remove(del_tuple)

                                # For Scenario 1
                                if start_dist_index == start_cost_index:
                                    new_combi = path_dict[i][start_dist_index].copy()
                                    path_dict[i] = [new_combi]
                                    new_tuple = (i, path_dict[i][0][2])
                                    if new_tuple not in possible_list:
                                        possible_list.append(new_tuple)
                                # For Scenario 2
                                else:
                                    new_combi_dist = path_dict[i][start_dist_index].copy()
                                    new_combi_cost = path_dict[i][start_cost_index].copy()
                                    path_dict[i] = [new_combi_dist, new_combi_cost]
                                    new_tuple = (i, path_dict[i][0][2])
                                    if new_tuple not in possible_list:
                                        possible_list.append((new_tuple))
                                    new_tuple = (i, path_dict[i][1][2])
                                    if new_tuple not in possible_list:
                                        possible_list.append((new_tuple))

                                # print("After eliminating duplicates")
                                # print(i + ":" + str(path_dict[i]))
                            else:
                                possible_list.append(i_tuple)
                    # print(i + ":" + str(path_dict[i]))
        possible_list.sort(key=itemgetter(1))
        current = possible_list[0][0]

    # Check for possible final_combi in FINAL_COORDINATE
    final_combi_index = -1
    if path_dict[FINAL_COORDINATE][0][1] <= ENERGY_LIMIT and path_dict[FINAL_COORDINATE][1][1] <= ENERGY_LIMIT:
        if path_dict[FINAL_COORDINATE][0][2] < path_dict[FINAL_COORDINATE][1][2]:
            final_combi_index = 0
        elif path_dict[FINAL_COORDINATE][0][2] > path_dict[FINAL_COORDINATE][1][2]:
            final_combi_index = 1
        else:
            if path_dict[FINAL_COORDINATE][0][1] <= path_dict[FINAL_COORDINATE][1][1]:
                final_combi_index = 0
            else:
                final_combi_index = 1
    else:
        if path_dict[FINAL_COORDINATE][0][0] > ENERGY_LIMIT:
            final_combi_index = 1
        else:
            final_combi_index = 0

    if final_combi_index == -1:
        print("error with logic")
    else:
        shortest_path = shortest_path_generator(path_dict[FINAL_COORDINATE][final_combi_index][0])

    # print("############################################################################################")
    # print(f"Total iterations: {COUNT}")
    print(f"Shortest Path: {shortest_path}")
    # print(f"Shortest Path: {path_dict[FINAL_COORDINATE][0][0]}")
    # print(f"Length of Shortest Path: {len(path_dict[FINAL_COORDINATE][0][0])}")
    print(f"Shortest Distance: {path_dict[FINAL_COORDINATE][final_combi_index][2]}")
    print(f"Total energy cost: {path_dict[FINAL_COORDINATE][final_combi_index][1]}")
    # print(f"Total time taken: {time.time() - time_2_now}")
    ###################################################################################################################

    ############################### Task 3 ############################################################################
    print()
    print("Task 3: ")
    # time_3_now = time.time()
    current = START_COORDINATE
    old_list = []
    current_dist = pythagoras(coord[START_COORDINATE])
    possible_list = [(START_COORDINATE, current_dist)]

    # path_dict = {number: [[path from "1" to the number], total energy, direct distance, accumulated distance, accumulated+direct(total) distance]}
    path_dict = {"1": [[["1"], 0, current_dist, 0, current_dist]]}
    # while(current!=FINAL_COORDINATE or path_dict["50"][1] > ENERGY_LIMIT):
    while (current != FINAL_COORDINATE):
        # if COUNT%10 == 0:
        #     input("Enter to continue:")

        if current == FINAL_COORDINATE:
            possible_list.pop(0)
        else:
            # COUNT += 1
            # print("Iteration Number "+str(COUNT) + ":")
            # print("Node Number: " + current)
            possible_list.pop(0)
            old_list.append(current)
            # print(f"Possible List after pop: {possible_list}")

            for i in graph[current]:
                if i not in old_list:
                    for node_hist in range(len(path_dict[current])):
                        i_coord = current + "," + i
                        i_cost = cost[i_coord] + path_dict[current][node_hist][1]

                        if i_cost <= ENERGY_LIMIT:

                            # append path_dict[i] with new combination of distance and cost
                            # print("Debug: " + str(path_dict[current][node_hist]))
                            # print("Debug: " + str(path_dict[current][node_hist][0]))

                            i_path = path_dict[current][node_hist][0].copy()
                            i_path.append(i)
                            # print("Debug: " + str(i_path))
                            i_direct_dist = pythagoras(coord[i])
                            i_accu = path_dict[current][node_hist][3] + distance[i_coord]
                            i_total = i_accu + i_direct_dist

                            i_tuple = (i, i_total)

                            # check if the node was previously in the dict
                            if i in path_dict:
                                path_dict[i].append([i_path, i_cost, i_direct_dist, i_accu, i_total])
                                # print("Repeated")
                                # print(i + ":" + str(path_dict[i]))

                            else:
                                path_dict[i] = [[i_path, i_cost, i_direct_dist, i_accu, i_total]]

                            # remove extra combinations such that a maximum of 2 is left
                            # (Scenario 1) lowest total distance and lowest total cost
                            # (Scenario 2) lowest total distance or lowest total cost
                            if len(path_dict[i]) != 1:
                                start_total_dist = path_dict[i][0][4]
                                start_total_energy = path_dict[i][0][1]
                                start_dist_index = 0
                                start_cost_index = 0
                                for node_combi in range(1, len(path_dict[i])):
                                    if start_total_dist > path_dict[i][node_combi][4]:
                                        start_dist_index = node_combi
                                        start_total_dist = path_dict[i][node_combi][4]
                                    if start_total_energy > path_dict[i][node_combi][1]:
                                        start_cost_index = node_combi
                                        start_total_energy = path_dict[i][node_combi][1]

                                # Remove not needed combinations in Possible List
                                for combi_num in range(len(path_dict[i])):
                                    if combi_num != start_dist_index or combi_num != start_cost_index:
                                        del_tuple = (i, path_dict[i][combi_num][4])
                                        if del_tuple in possible_list:
                                            possible_list.remove(del_tuple)

                                # For Scenario 1
                                if start_dist_index == start_cost_index:
                                    new_combi = path_dict[i][start_dist_index].copy()
                                    path_dict[i] = [new_combi]
                                    new_tuple = (i, path_dict[i][0][4])
                                    if new_tuple not in possible_list:
                                        possible_list.append(new_tuple)
                                # For Scenario 2
                                else:
                                    new_combi_dist = path_dict[i][start_dist_index].copy()
                                    new_combi_cost = path_dict[i][start_cost_index].copy()
                                    path_dict[i] = [new_combi_dist, new_combi_cost]
                                    new_tuple = (i, path_dict[i][0][4])
                                    if new_tuple not in possible_list:
                                        possible_list.append((new_tuple))
                                    new_tuple = (i, path_dict[i][1][4])
                                    if new_tuple not in possible_list:
                                        possible_list.append((new_tuple))

                                # print("After eliminating duplicates")
                                # print(i + ":" + str(path_dict[i]))
                            else:
                                possible_list.append(i_tuple)
                    # print(i + ":" + str(path_dict[i]))
        possible_list.sort(key=itemgetter(1))
        current = possible_list[0][0]

    # Check for possible final_combi in FINAL_COORDINATE
    final_combi_index = -1
    if path_dict[FINAL_COORDINATE][0][1] <= ENERGY_LIMIT and path_dict[FINAL_COORDINATE][1][1] <= ENERGY_LIMIT:
        if path_dict[FINAL_COORDINATE][0][3] < path_dict[FINAL_COORDINATE][1][3]:
            final_combi_index = 0
        elif path_dict[FINAL_COORDINATE][0][3] > path_dict[FINAL_COORDINATE][1][3]:
            final_combi_index = 1
        else:
            if path_dict[FINAL_COORDINATE][0][1] <= path_dict[FINAL_COORDINATE][1][1]:
                final_combi_index = 0
            else:
                final_combi_index = 1
    else:
        if path_dict[FINAL_COORDINATE][0][0] > ENERGY_LIMIT:
            final_combi_index = 1
        else:
            final_combi_index = 0

    if final_combi_index == -1:
        print("error with logic")
    else:
        shortest_path = shortest_path_generator(path_dict[FINAL_COORDINATE][final_combi_index][0])

    # print("############################################################################################")
    # print(f"Total iterations: {COUNT}")
    # shortest_path = []
    # while current != "1":
    #     shortest_path.append(current)
    #     current = path_dict[current][0]
    # shortest_path = shortest_path.reverse()
    # print(f"Taking from dict: {path_dict[possible_list[0][0]]}")
    # print(f"Shortest Path: {shortest_path}")
    # print(f"Length of Shortest Path: {len(shortest_path)}")
    # print(f"Shortest Distance: {path_dict[possible_list[0][0]][4]}")
    # print(f"Total energy cost: {path_dict[possible_list[0][0]][1]}")
    # print(f"Taking from dict: {path_dict[FINAL_COORDINATE]}")
    # shortest_path = ""
    # for node in path_dict[FINAL_COORDINATE][0][0]:
    #     shortest_path += node+"->"
    # shortest_path -= "->"
    print(f"Shortest Path: {shortest_path}")
    # print(f"Shortest Path: {path_dict[FINAL_COORDINATE][0][0]}")
    # print(f"Length of Shortest Path: {len(path_dict[FINAL_COORDINATE][0][0])}")
    print(f"Shortest Distance: {path_dict[FINAL_COORDINATE][final_combi_index][3]}")
    print(f"Total energy cost: {path_dict[FINAL_COORDINATE][final_combi_index][1]}")
    # print(f"Total time taken: {time.time() - time_3_now}")
    ###################################################################################################################

if __name__ == "__main__":
    main()
