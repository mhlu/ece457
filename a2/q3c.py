#!/usr/bin/env python
import numpy as np
import itertools as it

# lower is better
def getEval(F,D,p):
    total = 0
    for i in range(F.shape[0]):
        for j in range(F.shape[0]):
            total += F[p[i], p[j]]*D[i,j]
    return total

# def getEval2(F,D,p):
    # f1 = F[p,:]
    # f2 = f1[:,p]
    # total = 0
    # for i in range(F.shape[0]):
        # for j in range(F.shape[0]):
            # total += f2[i,j]*D[i,j]
    # return total

def ts(F, D, p, goalEval, tabuLen, dynLen=False, dynDurr=0, aspType=0):
    size = F.shape[0]
    T = np.zeros(F.shape, dtype=int)

    currEval = getEval(F,D,p)

    # initialize tabu list length
    tabuLenCnt = 0 #how long a dynamic tabu length has persisted
    tl = tabuLen

    gBest = currEval
    gPerm = p

    # while True:
    for i in range(3):
        bestDelta = float('inf')
        for i in range(size-1):
            for j in range(i+1, size):
                newP = p.copy()
                newP[i], newP[j] = newP[j], newP[i]
                newEval = getEval(F,D,newP)

                if T[newP[i], i] or T[newP[j],j]:
                    if aspType == 1 and\
                            newEval - currEval < bestDelta and\
                            newEval < gBest:
                        print('wtf1')
                        bestDelta = newEval - currEval
                    elif aspType == 2:
                        print('wtf2')
                        bestDelta = newEval - currEval

                elif newEval - currEval <= bestDelta: #<= to overwrite equal tabu aspiration
                    bestDelta = newEval - currEval
                    di, dj = i, j

        currEval = getEval(F,D,p)


        for i in range(size):
            for j in range(size):
                T[i][j] = max(T[i][j]-1, 0)

        # update tabu list length
        if dynLen:
            tabuLenCnt += 1
            if tabuLenCnt == dynDurr:
                tl = randrange(tabuLen//2, tabuLen)
                tabuLenCnt = 0

        T[p[di], di] = tl
        T[p[dj], dj] = tl
        p[di], p[dj] = p[dj], p[di]

        if currEval < gBest:
            gBest = currEval
            gPerm = p

        print(T, p, currEval)
    print(gBest, gPerm)



if __name__ == "__main__":
    D = np.genfromtxt('Distance.csv', delimiter=',', dtype=int)
    F = np.genfromtxt('Flow.csv', delimiter=',', dtype=int)
    assert D.shape == F.shape
    assert D.shape[0] == D.shape[1]
    size = D.shape[0]

    # p = np.random.permutation(size)
    p = [1,3,0,4,2]
    print(getEval(F,D,p))
    ts(F,D,p,1285,6)

