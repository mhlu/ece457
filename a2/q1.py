#!/usr/bin/env python2.7
from collections import deque

def isFree(grid, i, j, seen):
    if not(0 <= i < len(grid) and 0 <= j < len(grid[0])):
        return False

    if (i,j) in seen:
        return False

    if grid[i][j] == 'x':
        return False

    return True

def reconstructPath(parent, start, goal):
    path = [goal]
    it = goal
    while it != start:
        it = parent[it]
        path.append(it)
    path.reverse()
    return path


def bfs(grid, start, goal):
    if start == goal:
        return [goal]
    parent = {}
    seen = set([start])
    queue = deque([start])
    while True:
        if not queue:
            raise ValueError('could not find goal')

        i, j = queue.popleft()
        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = i+di, j+dj
            if not isFree(grid, ni, nj, seen):
                continue
            parent[(ni,nj)] = i, j
            if (ni, nj) == goal:
                return reconstructPath(parent, start, goal)
            seen.add((ni, nj))
            queue.append((ni, nj))



def astar(grid, start, goal):
    if start == goal:
        return [goal]

    def eDis(start, end):
        return abs(start[0]-end[0])+abs(start[1]-end[1])

    closedSet = set()
    openSet = set([start])
    parent = {}
    truePastScore = {start: 0}
    futureScore = {start: eDis(start, goal)}

    while openSet:
        i, j = min(openSet, key=lambda x: futureScore[x])
        if (i, j) == goal:
            return reconstructPath(parent, start, (i,j))

        openSet.remove((i, j))
        closedSet.add((i, j))

        for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
            ni, nj = i+di, j+dj
            if not isFree(grid, ni, nj, closedSet):
                continue

            distance = truePastScore[(i, j)] + 1
            if (ni, nj) not in openSet:
                openSet.add((ni, nj))
            elif distance >= truePastScore[(ni, nj)]:
                continue

            # found better way to reach neighbour
            parent[(ni, nj)] = (i, j)
            truePastScore[(ni, nj)] = distance
            futureScore[(ni, nj)] = truePastScore[(ni, nj)] + eDis((ni, nj), goal)
    raise ValueError('could not find goal')

def dfs(grid, start, goal):
    seen = set([start])
    path = [start]
    found =  dfs_helper(grid, start, goal, seen, path)
    if found:
        return path
    raise ValueError('could not find goal')

def dfs_helper(grid, curr, goal, seen, path):
    if curr == goal:
        return True

    i, j = curr
    for di, dj in ((-1,0), (1,0), (0,-1), (0,1)):
        ni, nj = i+di, j+dj
        if not isFree(grid, ni, nj, seen):
            continue
        seen.add((ni, nj))
        path.append((ni, nj))
        found = dfs_helper(grid, (ni, nj), goal, seen, path)
        if found:
            return True
        path.pop()
    return False






if __name__ == "__main__":
    grid = []
    with open('figure1.txt') as fin:
        for line in fin:
            grid.append(line.strip())
    grid.reverse()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start = (i,j)
                continue
            if grid[i][j] == '1':
                goal1 = (i,j)
                continue
            if grid[i][j] == '2':
                goal2 = (i,j)
                continue

    print(astar(grid, start, goal1))
    print(bfs(grid, start, goal1))
    print(dfs(grid, start, goal1))
    assert len(astar(grid, start, goal1)) == len(bfs(grid, start, goal1))
    assert len(astar(grid, start, goal2)) == len(bfs(grid, start, goal2))




