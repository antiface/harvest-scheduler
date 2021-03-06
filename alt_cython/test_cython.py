from scheduler import schedule
import numpy as np
import json
import prep_data

if __name__ == '__main__':
    # 4D: stands, rxs, time periods, variables
    try:
        stand_data = np.load('cache.array.npy')
        axis_map = json.loads(open('cache.axis_map').read())
        valid_mgmts = json.loads(open('cache.valid_mgmts').read())
    except:
        stand_data, axis_map, valid_mgmts = prep_data.from_files()

    # pick a strategy for each stand rx time period variable
    # cumulative_maximize : target the absolute highest cumulative value
    # evenflow            : minimize variance around a target
    # cumulative_cost     : treated as cost; sum over all time periods
    strategies = ['cumulative_maximize', 'cumulative_maximize', 'evenflow', 'cumulative_cost']
    variable_names = ['carbon', 'harvest', 'harvest flow', 'cost']
    weights = [1.0, 100.0, 300.0, 1.0]

    # TODO need to define which variable is considered ("harvest")
    # and when rx is changed, check the adjacent stands for each time period
    # penalize/avoid if they have overlapping harvests.
    adjacency = [None for x in range(stand_data.shape[0])]
    adjacency[4] = (3, 2, 4)  # avoid cutting stand 4 when 1,2,3 have harvests?

    # restrict managment options for certain stands
    # valid_mgmts = [None for x in range(stand_data.shape[0])]
    # valid_mgmts[0] = (0, 1, 2)
    # valid_mgmts[1] = (0, 1, 2)
    # valid_mgmts[2] = (0, 1, 2)

    best, optimal_stand_rxs = schedule(
        stand_data,
        strategies,
        weights,
        variable_names,
        adjacency,
        valid_mgmts,
        temp_min=.1,
        temp_max=5000.0,
        steps=50000,
        report_interval=10000
    )

    print best
    for osrx in optimal_stand_rxs:
        print axis_map['mgmt'][osrx]
