from pathlib import Path
from Question_1 import uniform_cost_search
from Question2_BestFirstSearch import bestFirstSearch
from Question3_A_Star import a_star_search
import json

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

    print('Question 1:')
    print('='*50)
    distance, path = uniform_cost_search(graphdict, distancedict, '1', '50')

    path = "->".join(path)
    print()
    print(f"{distance=}\n{path=}")

    print('Question 2:')
    print('='*50)
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

    print('modified BFS returns more optimal result but will take a long time to complete. To verify results, run Question2_BFS_modified.py')
    print()
    print('Question 3:')
    print('='*50)
    res = a_star_search(graph=graphdict, distancecosts=distancedict,
            energycosts=costdict, coords=coordsdict, start='1', target='50',)
    
    dist, energy, path = res['distance'], res['energy'], res['path']
    print('-'*50)
    print(f'dist={dist=}')
    print(f'energy={energy=}')
    path = "->".join(path)
    print(f'{path=}')
