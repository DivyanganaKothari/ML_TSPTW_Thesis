import math
import random

from pyscipopt import Model, quicksum
from read_excel import expected_dict,n, e,l


def mtz2tw(n, c, e, l):
    model = Model("tsptw - mtz-strong")

    x, u = {}, {}
    nodes = set(e.keys()) & set(l.keys())  # Only consider nodes that are present in e and l

    for i in nodes:
        u[i] = model.addVar(lb=e[i], ub=l[i], vtype="C", name="u(%s)" % i)
        for j in nodes:
            if i != j:
                x[i, j] = model.addVar(vtype="B", name="x(%s,%s)" % (i, j))

    for i in nodes:
        model.addCons(quicksum(x[i, j] for j in nodes if j != i) == 1, "Out(%s)" % i)
        model.addCons(quicksum(x[j, i] for j in nodes if j != i) == 1, "In(%s)" % i)

        for j in nodes:
            if i != j:
                M1 = max(l[i] + c[i, j] - e[j], 0)
                M2 = max(l[i] + min(-c[j, i], e[j] - e[i]) - e[j], 0)
                model.addCons(u[i] + c[i, j] - M1 * (1 - x[i, j]) + M2 * x[j, i] <= u[j], "LiftedMTZ(%s,%s)" % (i, j))

    for i in nodes:
        model.addCons(e[i] + quicksum(max(e[j] + c[j, i] - e[i], 0) * x[j, i] for j in nodes if i != j) \
                      <= u[i], "LiftedLB(%s)" % i)

        model.addCons(u[i] <= l[i] - \
                      quicksum(max(l[i] - l[j] + c[i, j], 0) * x[i, j] for j in nodes if i != j), \
                      "LiftedUB(%s)" % i)

    model.setObjective(quicksum(c[i, j] * x[i, j] for (i, j) in x), "minimize")

    model.data = x, u
    return model


if __name__ == "__main__":
    EPS = 1.e-6
    # n = 10
    # width = 10
    # c,x,y,e,l = make_data(n,width)
    c=expected_dict

    print(c)
    print(e)
    print(l)

    model = mtz2tw(n, c, e, l)
    model.optimize()
    x, u = model.data

    sol = [i for (v, i) in sorted([(model.getVal(u[i]), i) for i in u])]
    print("mtz2:")
    print(sol)
    print("Optimal value:", model.getObjVal())
    if model.getStatus() == "optimal":
        sol = [i for (v, i) in sorted([(model.getVal(u[i]), i) for i in u])]
    else:
        print("The problem is infeasible or not in the SOLVING stage.")
