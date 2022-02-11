import json
from os import path

with open(r'C:\Users\zhuwe\OneDrive\Desktop\VS Code Environment\CZ3005\G.json') as graph_data:
    graphdict = json.load(graph_data)

with open(r'C:\Users\zhuwe\OneDrive\Desktop\VS Code Environment\CZ3005\Dist.json') as dist_data:
    distancedict = json.load(dist_data)

with open(r'C:\Users\zhuwe\OneDrive\Desktop\VS Code Environment\CZ3005\Cost.json') as cost_data:
    costdict = json.load(cost_data)


"""
"""

import heapq


def BFS_all_edges(graph, start, target):
    for node in graph:
        graph[node] = [graph[node], None, []]

    queue = [(0, start)]
    explored_edge_list = set()
    graph[start][1:] = 0, []

    node_count = 0

    while queue:
        node_count+= 1
        if node_count % 10000==0:
            print(f'{node_count}           \r', end=' ')

        dist, current_node = heapq.heappop(queue)
        neighbours, distance_to_curr, path_to_curr = graph[current_node]

        if current_node == target:
            print('---------------------------------------')
            print(distance_to_curr, path_to_curr)
            continue

        for neighbour in neighbours:
            full_dist_to_neighbour, full_path_to_neighbour = graph[neighbour][1:]
            edge = ','.join([current_node, neighbour])
            edge_distance = distancedict[edge]

            # if current_node == '1277':
                # print(path_to_curr)
                # print(edge)
                # print(path_to_curr == ['1', '1363', '1358', '1357', '1356', '1276', '1273', '1277', '1269', '1267'])
                # ['1', '1363', '1358', '1357', '1356','1276', '1273', '1277', '1269', '1267']
                # ['1', '1363', '1358', '1357', '1356', '1276', '1273']
                # ['1', '1363', '1358', '1357', '1356', '1276', '1273', '1277']
            # 1->1363->1358->1357->1356->1276->1273->1277->1269->1267->1268->1284->1283->1282->1255->1253->1260->1259->1249->1246->963

            # if edge == '1269,1267':
                # print(path_to_curr, neighbour)


            distance_changed = False
            if full_dist_to_neighbour is None or (distance_to_curr + edge_distance) < full_dist_to_neighbour:
                graph[neighbour][1:] = (distance_to_curr + edge_distance), [*path_to_curr, current_node]
                distance_changed = True

                # if edge == '1267,1268':
                    # print([*path_to_curr, current_node], neighbour, distance_to_curr + edge_distance)

                # print('########################################')
                # print(distance_to_curr, path_to_curr)
                # print(full_path_to_neighbour, full_dist_to_neighbour)

            if edge not in explored_edge_list or distance_changed:
                # if edge == '1277,1269':
                #     print('\nPATH IS LESS')
                #     print(graph[neighbour][1:])
                heapq.heappush(queue, (edge_distance, neighbour))

            explored_edge_list.add(edge)



BFS_all_edges(graphdict, '1','979')

start = False
# start = True
if start:
    # x = "1->1363->1358->1357->1356->1276->1273->1277->1269->1267->1268->1284->1283->1282->1255->1253->1260->1259->1249->1246->963->964->962->1002->952->1000->998->994->995->996->987->988->979"
    # ['1', '1363', '1358', '1357', '1356', '1276', '1273', '1277', '1269', '1267', '1268', '1284', '1283', '1282', '1255', '1253', '1260', '1259', '1249', '1246', '963', '964', '962', '1002', '952', '1000', '998', '994', '995', '996', '987', '988']
    # # x = "1->1363->1358->1357->1356->1276->1273->1277->1269->1267->1268->1284->1283->1282->1255->1253->1260->1259->1249->1246->963->964->962->1002->952->1000->998->994->995->996->987->988->979->980->969->977->989->990->991->2369->2366->2340->2338->2339->2333->2334->2329->2029->2027->2019->2022->2000->1996->1997->1993->1992->1989->1984->2001->1900->1875->1874->1965->1963->1964->1923->1944->1945->1938->1937->1939->1935->1931->1934->1673->1675->1674->1837->1671->1828->1825->1817->1815->1634->1814->1813->1632->1631->1742->1741->1740->1739->1591->1689->1585->1584->1688->1579->1679->1677->104->5680->5418->5431->5425->5429->5426->5428->5434->5435->5433->5436->5398->5404->5402->5396->5395->5292->5282->5283->5284->5280->50"
    # x=x.split('->')
    # x = ['1', '1363', '1358', '1357', '1359','1280', '1278', '1277', '1269', '1267']

    x = ['1', '1363', '1358', '1357', '1356', '1276', '1273', '1277', '1269', '1267']
    try:
        dist = 0
        for index,i in enumerate(x):
            current_node = i
            neighbour = x[index+1]
            assert x[index+1] in graphdict[i]
            edge = ','.join([current_node, neighbour])
            dist += distancedict[edge]

    except IndexError:
        pass
    print(dist)
