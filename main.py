from pyscipopt import Model, quicksum
#from read_excel import read_excel_data, process_data
#from read_excel import updated_dict, e, l, n
from instances_3_with_25_nodes import instances
import json


def tsptw2(n, c, e, l):
    """tsptw2: model for the traveling salesman problem with time windows
    (based on Miller-Tucker-Zemlin's formulation, two-index potential)
    Parameters:
        - n: number of nodes
        - c[i,j]: cost for traversing arc (i,j)
        - e[i]: earliest date for visiting node i
        - l[i]: latest date for visiting node i
    Returns a model, ready to be solved.
    """
    model = Model("tsptw2")

    x, u = {}, {}
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                x[i, j] = model.addVar(vtype="B", name="x(%s,%s)" % (i, j))
                u[i, j] = model.addVar(vtype="C", name="u(%s,%s)" % (i, j))

    for i in range(1, n + 1):
        model.addCons(quicksum(x[i, j] for j in range(1, n + 1) if j != i) == 1, "Out(%s)" % i)
        model.addCons(quicksum(x[j, i] for j in range(1, n + 1) if j != i) == 1, "In(%s)" % i)

    for j in range(2, n + 1):
        model.addCons(quicksum(u[i, j] + c[i, j] * x[i, j] for i in range(1, n + 1) if i != j) -
                      quicksum(u[j, k] for k in range(1, n + 1) if k != j) <= 0, "Relate(%s)" % j)

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                model.addCons(e[i] * x[i, j] <= u[i, j], "LB(%s,%s)" % (i, j))
                model.addCons(u[i, j] <= l[i] * x[i, j], "UB(%s,%s)" % (i, j))

    model.setObjective(quicksum(c[i, j] * x[i, j] for (i, j) in x), "minimize")

    model.data = x, u
    return model


if __name__ == "__main__":
    EPS = 1.e-6
    TIME_LIMIT = 1000  # seconds
    optimal_tour_lengths = {}
    instance_file_name = "instances_3_with_25_nodes"  # Change this dynamically

    try:
        for idx, instance in enumerate(instances):
            n = len(instance['earliest_times'])
            c = instance['distance_matrix']  # Distance matrix
            e = instance['earliest_times']  # Earliest times
            l = instance['latest_times']

            print("TWO INDEX MODEL")
            print(n)
            model = tsptw2(n, c, e, l)
            model.setParam('limits/time', TIME_LIMIT)  # Set a time limit
            model.optimize()

            # Check if a feasible solution was found

            if model.getStatus() == "optimal":
                optimal_value = model.getObjVal()
                print("Optimal value:", optimal_value)
                optimal_tour_lengths[idx + 1] = optimal_value  # Save the optimal tour length

                x, u = model.data
                for (i, j) in x:
                    if model.getVal(x[i, j]) > EPS:
                        print(x[i, j].name, i, j, model.getVal(x[i, j]))

                start_time = [0] * (n + 1)
                for (i, j) in u:
                    if model.getVal(u[i, j]) > EPS:
                        print(u[i, j].name, i, j, model.getVal(u[i, j]))
                        start_time[j] += model.getVal(u[i, j])

                start = [i for v, i in sorted([(start_time[i], i) for i in range(1, n + 1)])]
                print(start)
            else:
                print("No feasible solution found for instance", idx + 1)
    except Exception as e:
        print(f"Error processing instance {idx + 1}: {e}")
    output_file_name = f"optimal_tour_lengths_{instance_file_name}.json"
    with open(output_file_name, 'w') as json_file:
        json.dump(optimal_tour_lengths, json_file)

    print("Optimal tour lengths:", optimal_tour_lengths)
