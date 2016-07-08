#!/usr/bin/env python3
import numpy as np
import itertools as it
from random import randrange

# lower is better
def getEval(F,D,p,freqFactor=0):
    total = 0
    for i in range(F.shape[0]-1):
        for j in range(i+1,F.shape[0]):
            total += F[p[i], p[j]]*D[i,j]

    if freqFactor != 0:
        for i in range(len(p)):
            total += freq[p[i], i]/freqFactor
    return total

def ts(F, D, p, numIter, tabuLen, dynDurr=0, aspType=0, neighRatio=1, freqFactor=0):
    initialP = p.tolist()
    size = F.shape[0]
    T = np.zeros(F.shape, dtype=int)
    freq = np.zeros(F.shape, dtype=int)

    currEval = getEval(F,D,p)
    gBestEval = currEval
    gBestPerm = p

    # initialize dynamic tabu list
    tabuLenCnt = 0 #how long a dynamic tabu length has persisted
    tl = tabuLen

    for i in range(numIter):
        for i in range(size):
            freq[p[i], i] += 1

        bestDelta = float('inf')
        bestAspEval = float('inf')
        n = 0
        for i in range(size-1):
            for j in range(i+1, size):
                n+=1
                # if numNeigh != 0 and n>numNeigh:
                    # break
                if n > 1 and randrange(0,100) > neighRatio*100:
                    continue

                newPerm = p.copy()
                newPerm[i], newPerm[j] = newPerm[j], newPerm[i]

                newEval = getEval(F,D,newPerm) if not freqFactor == 0 else getEval(F,D,newPerm,freqFactor)

                if T[newPerm[i], i] or T[newPerm[j],j]:
                    if aspType != 0 and newEval < bestAspEval:
                        ai, aj = i, j
                        bestAspEval = newEval

                elif newEval - currEval < bestDelta:
                    bestDelta = newEval - currEval
                    di, dj = i, j

        localP = p.copy()
        localP[di], localP[dj] = localP[dj], localP[di]
        localEval = getEval(F,D,localP)

        if bestAspEval != float('inf'):
            aspP = p.copy()
            aspP[ai], aspP[aj] = aspP[aj], aspP[ai]
            aspEval = getEval(F,D,aspP)
            if (aspType == 1 and bestAspEval < min(localEval, gBestEval)) or (aspType == 2 and aspEval < localEval):
                di, dj = ai, aj

        # update tabu list length
        if dynDurr != 0:
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

        currEval = getEval(F,D,p)
        if currEval < gBestEval:
            gBestEval = currEval
            gBestPerm = p.copy()

        # print(gBestEval)
        # print(T, p, currEval)
    print('final eval: '+str(gBestEval))
    finalP = p.tolist()
    print('initial permuatation: \t'+str(initialP))
    print('final permuatation: \t'+str(gBestPerm.tolist()))
    print('\n')
    return gBestEval



if __name__ == "__main__":
    D = np.genfromtxt('resource/Distance.csv', delimiter=',', dtype=int)
    F = np.genfromtxt('resource/Flow.csv', delimiter=',', dtype=int)
    # D = np.genfromtxt('Distance.csv', delimiter=',', dtype=int)
    # F = np.genfromtxt('Flow.csv', delimiter=',', dtype=int)
    assert D.shape == F.shape
    assert D.shape[0] == D.shape[1]
    size = D.shape[0]

    print('*'*94)
    print('recency based tabu list only')
    print('*'*94)
    p = np.random.permutation(size)
    ts(F,D,p.copy(),250,15)

    print('*'*94)
    print('10 experiments with random initial starting points')
    print('*'*94)
    for i in range(10):
        p = np.random.permutation(size)
        ts(F,D,p.copy(),250,15)

    print('*'*94)
    print('Changing tabu list size')
    print('*'*94)
    p = np.random.permutation(size)
    print('tabu length {0}'.format(5))
    ts(F,D,p.copy(),250,5)
    print('tabu length {0}'.format(25))
    ts(F,D,p.copy(),250,25)
    print('tabu length {0}'.format(35))
    ts(F,D,p.copy(),250,35)
    print('tabu length {0}'.format(45))
    ts(F,D,p.copy(),250,45)
    print('tabu length {0}'.format(55))
    ts(F,D,p.copy(),250,55)

    print('*'*94)
    print('Changing tabu list size to dynamic size')
    print('*'*94)
    ts(F,D,p.copy(),250,55, dynDurr=20)

    print('*'*94)
    print('Add best fit so far aspiration')
    print('*'*94)
    ts(F,D,p.copy(),250,55, dynDurr=20, aspType=1)

    print('*'*94)
    print('Limit to part of neighbourhood')
    print('*'*94)
    ts(F,D,p.copy(),250,55, dynDurr=20, aspType=1, neighRatio=0.9)

    print('*'*94)
    print('Add frequency based list')
    print('*'*94)
    ts(F,D,p.copy(),250,55, dynDurr=20, aspType=1, neighRatio=0.9, freqFactor=250.0)


