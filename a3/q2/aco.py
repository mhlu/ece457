from __future__ import division
import random
import math


cities = {}


cities[1] =  (1150.0, 1760.0)
cities[2] =  (630.0, 1660.0)
cities[3] =  (40.0, 2090.0)
cities[4] =  (750.0, 1100.0)
cities[5] =  (750.0, 2030.0)
cities[6] =  (1030.0, 2070.0)
cities[7] =  (1650.0, 650.0)
cities[8] =  (1490.0, 1630.0)
cities[9] =  (790.0, 2260.0)
cities[10] =  (710.0, 1310.0)
cities[11] =  (840.0, 550.0)
cities[12] =  (1170.0, 2300.0)
cities[13] =  (970.0, 1340.0)
cities[14] =  (510.0, 700.0)
cities[15] =  (750.0, 900.0)
cities[16] =  (1280.0, 1200.0)
cities[17] =  (230.0, 590.0)
cities[18] =  (460.0, 860.0)
cities[19] =  (1040.0, 950.0)
cities[20] =  (590.0, 1390.0)
cities[21] =  (830.0, 1770.0)
cities[22] =  (490.0, 500.0)
cities[23] =  (1840.0, 1240.0)
cities[24] =  (1260.0, 1500.0)
cities[25] =  (1280.0, 790.0)
cities[26] =  (490.0, 2130.0)
cities[27] =  (1460.0, 1420.0)
cities[28] =  (1260.0, 1910.0)
cities[29] =  (360.0, 1980.0)


def dist(i,j):
    return math.sqrt((cities[i][0]-cities[j][0])**2 + (cities[i][1]-cities[j][1])**2)

def pheromone(i,j):
    return 1 #constant initialization

edge = {j:{i:[pheromone(i,j),dist(i,j)] for i in cities if i != j} for j in cities}

evap = 0.1
pop = 10 
alpha = 1
beta = 5
q = 10
q2 = 100

def generate_solution(start_city):
    unvisited = set(cities.keys()) 
    unvisited.remove(start_city)
    sol = [start_city]
    current = start_city
    while unvisited:
        total = 0
        thresh = []
        nx = -1
        for i in unvisited:
            ph, d = edge[current][i]
            total += (ph**alpha)/(d**beta)
            thresh.append((i,total))
        pick = random.uniform(0, total)
        for i, j in thresh:
            if pick <= j:
                nx = i
                break 
        unvisited.remove(nx)
        sol.append(nx)
        current = nx
    return sol

def costf(sol):
    total = 0 
    prev = sol[0]
    for i in sol[1:]:
        total += dist(prev, i)
        prev = i
    total += dist(prev, sol[0])
    return total


def evaporate():
    global edge
    for i in edge:
        for c in edge[i]:
            edge[i][c][0] *= (1-evap)

times = 0
def updatePheromone(sol, cost, q):
    global times
    cur = sol[0]
    for node in sol[1:]:
        edge[cur][node][0] += q / cost
        cur = node

print "evap = {}, pop = {}, alpha = {}, beta = {}, q = {}, q2 = {}".format(evap, pop, alpha, beta, q, q2)

it = 0
bestc = 2**31 
bestp = []
best_it = 0
def keep_going():
    # return it - best_it <= 500
    return it < 50

while keep_going():
    res = []
    for ant in range(pop):
        for city in cities:
            sol = generate_solution(city)
            cost = costf(sol)
            res.append((cost, sol))
            # updatePheromone(sol, cost, q)

    goodc, goodp = sorted(res)[0]
    if goodc < bestc:
        bestc = goodc
        bestp = goodp[:]
        best_it = it
        print "new best is", bestc, "found on iteration", it

    updatePheromone(bestp, bestc, q2)
    evaporate()
    it += 1
print bestc, bestp
