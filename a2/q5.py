import copy
import math
import random
import sys

class SA:
    def __init__(self, initial_temp, final_temp, alpha, iterations):
        self.initial = initial_temp
        self.final = final_temp
        self.alpha = alpha
        self.iterations = iterations

    def set_cvrp(self, cap, cities, trucks, coords, demand):
        self.capacity = cap
        self.cities = cities
        self.trucks = trucks
        self.coords = coords
        self.demand = demand
    
    def run(self):
        cur_temp = float(self.initial)
        best_sol = None
        best_value = None
        cur_sol = self._initial_solution()
        cur_value = self._evaluate(cur_sol)
        while cur_temp > self.final:
            for iter in range(self.iterations):
                new_sol = self._neighbour(cur_sol)
                new_value = self._evaluate(new_sol)
                cost = new_value - cur_value
                if cost < 0:
                    cur_sol = new_sol
                    cur_value = new_value
                    if not best_value or cur_value < best_value:
                        best_sol = cur_sol
                        best_value = cur_value
                elif random.random() < math.exp(-cost/cur_temp):
                    cur_sol = new_sol
                    cur_value = new_value
            cur_temp *= self.alpha
        # Print result
        for i in range(len(best_sol)):
            print "Route #" + str(i+1) + ":", best_sol[i]
        print "Total Cost:", best_value, '\n'

    def _initial_solution(self):
        sol = [[] for i in range(self.trucks)]
        seen = set()
        for i in range(self.trucks):
            demand = 0
            for city in range(2, self.cities + 1):
                if city not in seen and demand + self.demand[city] <= self.capacity:
                    sol[i].append(city)
                    seen.add(city)
                    demand += self.demand[city]
        return sol

    def _neighbour(self, sol):
        new_sol = copy.deepcopy(sol)
        if random.random() < 0.8:
            self._move(new_sol)
        self._replace(new_sol)
        return new_sol

    def _move(self, sol):
        exclude = {1}
        pairs = []
        for route in sol:
            prev = 1
            for city in route:
                pairs.append((self._dist(self.coords[prev], self.coords[city]), city))
                prev = city
        pairs.sort()
        exclude.union({pairs[i][1] for i in range(5)})
        move_set = set()
        while len(move_set) < 5:
            city = random.randint(2, self.cities)
            if city not in exclude:
                move_set.add(city)
        self._insert_random(sol, move_set)
        return sol

    def _replace(self, sol):
        avg_dist = []
        for route in sol:
            if len(route) == 0:
                continue
            prev = 1
            for i in range(len(route) - 1):
                l1 = self._dist(self.coords[prev], self.coords[route[i]])
                l2 = self._dist(self.coords[route[i]], self.coords[route[i+1]])
                avg_dist.append(((l1 + l2) / 2.0, route[i]))
                prev = route[i]
            l1 = self._dist(self.coords[prev], self.coords[route[-1]])
            l2 = self._dist(self.coords[route[-1]], self.coords[1])
            avg_dist.append(((l1 + l2) / 2.0, route[-1]))
        avg_dist.sort(reverse=True)
        move_set = {avg_dist[i][1] for i in range(5)}
        self._insert_random(sol, move_set)
        return sol

    def _insert_random(self, sol, cities):
        for city in cities:
            # Remove
            for i in range(self.trucks):
                if city in sol[i]:
                    sol[i].remove(city)
                    break
            # Move to new route if valid
            while True:
                route = random.randint(0, self.trucks - 1)
                demand = sum([self.demand[i] for i in sol[route]])
                if demand + self.demand[city] <= self.capacity:
                    sol[route].append(city)
                    break

    def _evaluate(self, sol):
        cost = 0
        for route in sol:
            prev = 1
            for city in route:
                cost += self._dist(self.coords[prev], self.coords[city])
                prev = city
            cost += self._dist(self.coords[prev], self.coords[1])
        return cost

    def _dist(self, loc1, loc2):
        return int(round(math.sqrt((loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2)))



if __name__ == "__main__":
    capacity = 0
    cities = 0
    trucks = 0
    coords = {}
    demand = {}

    # Parse input file
    with open(sys.argv[1], 'r') as f:
        line = f.readline()
        trucks = int(line[line.rfind('k') + 1:])
        while not line.startswith('DIMENSION'):
            line = f.readline()
        cities = int(line[line.rfind(":") + 1:])

        while not line.startswith('CAPACITY'):
            line = f.readline()
        capacity = int(line[line.rfind(":") + 1:])

        while not line.startswith('NODE_COORD_SECTION'):
            line = f.readline()
        for i in range(cities):
            line = map(int, f.readline().split())
            coords[line[0]] = (line[1], line[2])

        while isinstance(line, list) or not line.startswith('DEMAND_SECTION'):
            line = f.readline()
        for i in range(cities):
            line = map(int, f.readline().split())
            demand[line[0]] = line[1] 

    sa = SA(1000, 1, 0.85, 100)
    sa.set_cvrp(capacity, cities, trucks, coords, demand)
    sa.run()
    sa = SA(600, 100, 0.96, 100)
    sa.set_cvrp(capacity, cities, trucks, coords, demand)
    sa.run()
