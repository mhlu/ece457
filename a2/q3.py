#!/usr/bin/env python
import numpy as np
import itertools as it

# lower is better
def getEval(F,D,p,freq=None):
    total = 0
    for i in range(F.shape[0]):
        for j in range(F.shape[0]):
            total += F[p[i], p[j]]*D[i,j]

    if freq:
        pass
    return total

def ts(F, D, p, goalEval, tabuLen, dynLen=False, dynDurr=0, aspType=0):
    size = F.shape[0]
    T = np.zeros(F.shape, dtype=int)
    freq = np.zeros(F.shape, dtype=int)

    currEval = getEval(F,D,p)
    gBestEval = currEval
    gBestPerm = p

    # initialize dynamic tabu list
    tabuLenCnt = 0 #how long a dynamic tabu length has persisted
    tl = tabuLen

    k = 0
    for i in range(6):
        k += 1
        if gBestEval == goalEval:
            break
        for i in range(size):
            freq[p[i], i] += 1

        bestDelta = float('inf')
        bestAspEval = float('inf')
        for i in range(size-1):
            for j in range(i+1, size):

                newPerm = p.copy()
                newPerm[i], newPerm[j] = newPerm[j], newPerm[i]
                newEval = getEval(F,D,newPerm)

                if T[newPerm[i], i] or T[newPerm[j],j]:
                    if aspType != 0 and newEval < bestAspEval:
                        ai, aj = i, j
                        bestAspEval = newEval

                elif newEval - currEval < bestDelta: #<= to overwrite equal tabu aspiration
                    bestDelta = newEval - currEval
                    di, dj = i, j

        currEval = getEval(F,D,p)

        if (aspType == 1 and bestAspEval < min(currEval, gBestEval)) or (aspType == 2 and bestAspEval < currEval):
            i, j = ai, aj

        # update tabu list length
        if dynLen:
            tabuLenCnt += 1
            if tabuLenCnt == dynDurr:
                tl = randrange(tabuLen//2, tabuLen)
                tabuLenCnt = 0

        for i in range(size):
            for j in range(size):
                T[i][j] = max(T[i][j]-1, 0)
        T[p[di], di] = tl
        T[p[dj], dj] = tl
        p[di], p[dj] = p[dj], p[di]

        if currEval < gBestEval:
            gBestEval = currEval
            gBestPerm = p

        # print(gBestEval)
        # print(T, p, currEval)
    print(k)
    # print(gBestEval)



if __name__ == "__main__":
    # D = np.genfromtxt('resource/Distance.csv', delimiter=',', dtype=int)
    # F = np.genfromtxt('resource/Flow.csv', delimiter=',', dtype=int)
    D = np.genfromtxt('Distance.csv', delimiter=',', dtype=int)
    F = np.genfromtxt('Flow.csv', delimiter=',', dtype=int)
    assert D.shape == F.shape
    assert D.shape[0] == D.shape[1]
    size = D.shape[0]

    p = np.random.permutation(size)
    ts(F,D,p,2570,10, aspType=0)
    ts(F,D,p.copy(),2570,10, aspType=1)
    ts(F,D,p.copy(),2570,10, aspType=2)

