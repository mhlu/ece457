from random import uniform, random
from math import sqrt
class Particle:
    def __init__(self):
        self.fit = None
        self.pBest = None
        self.v = None
        self.x = None

def camelBack(x, y):
    return float((4-2.1*pow(x,2)+pow(x,4)/3)*pow(x,2)+x*y+(-4+4*pow(y,2))*pow(y,2))

def pso(popSize, iterMax, w=0.79, c1=1.49, c2=1.49, 
        inertia=False, constriction=False, vMax=None,
        localBest=False, GCPSO=False):

    if GCPSO:
        fc = 5.0
        sc = 15.0
        pt = 1.0
        fail = 0

    particles = []
    gBest = None
    gPart = None
    for i in xrange(popSize):
        p = Particle()
        p.x = (uniform(-100, 100), uniform(-100, 100))
        p.fit = camelBack(p.x[0], p.x[1])
        p.v = (0.0, 0.0)
        p.pBest = (p.fit, p.x)
        particles.append(p)

        if gBest is None or gBest[0] > p.fit:
            gBest = (p.fit, p.x)
            gPart = p

    for i in xrange(iterMax):
        for j in xrange(popSize):
            p = particles[j]

            if GCPSO and p is gPart:
                v0 = -p.x[0] + gBest[1][0] + w*p.v[0] + pt*(1-2*random())
                v1 = -p.x[1] + gBest[1][1] + w*p.v[1] + pt*(1-2*random())

                fit = camelBack(p.x[0]+v0, p.x[1]+v1)
                if fit >= p.fit:
                    fail = max(1, fail+1)
                else:
                    fail = min(-1, fail-1)

                if fail < -sc:
                    pt = 2*pt
                elif fail > fc:
                    pt = 0.5*pt
            else:
                if localBest:
                    na = particles[(j+popSize-1)%popSize].pBest
                    nb = particles[(j+1)%popSize].pBest
                    nc = p.pBest
                    if na[0] == min(na[0], nb[0], nc[0]):
                        socialPos = na[1]
                    elif nb[0] == min(na[0], nb[0], nc[0]):
                        socialPos = nb[1]
                    else:
                        socialPos = nc[1]
                else:
                    socialPos = gBest[1]
            
                v0 = c1*random()*(p.pBest[1][0]-p.x[0]) \
                    + c2*random()*(socialPos[0]-p.x[0])
                v1 = c1*random()*(p.pBest[1][1]-p.x[1]) \
                    + c2*random()*(socialPos[1]-p.x[1])

                if inertia:
                    v0 += w*p.v[0]
                    v1 += w*p.v[1]

                if constriction:
                    phi = max(c1+c2, 4)
                    k = 2.0 / abs(2-phi-sqrt(pow(phi, 2)-4*phi))
                    v0 = k*(p.v[0]+v0)
                    v1 = k*(p.v[1]+v1)

                if vMax is not None:
                    v0Sign = 1.0 if v0 > 0 else -1.0
                    v1Sign = 1.0 if v1 > 0 else -1.0
                    v0 = min(abs(v0), vMax) * v0Sign
                    v1 = min(abs(v1), vMax) * v1Sign



            p.v = (v0, v1)
            p.x = (p.x[0]+p.v[0], p.x[1]+p.v[1])
            p.fit = camelBack(p.x[0], p.x[1])

            if p.pBest[0] > p.fit:
                p.pBest = (p.fit, p.x)

            if gBest[0] > p.fit:
                gBest = (p.fit, p.x)

    return gBest

if __name__ == "__main__":
    # random run
    v, (x, y) = pso(10, 100)
    print('without inertia) \tvalue: %f, x: %f, y: %f\n' % (v, x, y))


    print('global best ----------')
    # inertia weight
    v, (x, y) = pso(10, 100, inertia=True)
    print('with inertia) \t\tvalue: %f, x: %f, y: %f' % (v, x, y))

    # vmax set to 10
    v, (x, y) = pso(10, 100, inertia=True, vMax=10)
    print('with vmax) \t\tvalue: %f, x: %f, y: %f' % (v, x, y))

    # constriction
    v, (x, y) = pso(10, 100, constriction=True)
    print('with constriction) \tvalue: %f, x: %f, y: %f' % (v, x, y))
    print('---------------------\n\n')



    print('local best ----------')
    # inertia weight
    v, (x, y) = pso(10, 100, inertia=True, localBest=True)
    print('with inertia) \t\tvalue: %f, x: %f, y: %f' % (v, x, y))

    # vmax set to 10
    v, (x, y) = pso(10, 100, inertia=True, vMax=10, localBest=True)
    print('with vmax) \t\tvalue: %f, x: %f, y: %f' % (v, x, y))

    # constriction
    v, (x, y) = pso(10, 100, constriction=True, localBest=True)
    print('with constriction) \tvalue: %f, x: %f, y: %f' % (v, x, y))
    print('---------------------\n\n')

    v, (x, y) = pso(10, 100, inertia=True, GCPSO=True)
    print('with GCPSO) \t\tvalue: %f, x: %f, y: %f\n\n' % (v, x, y))


    print('10 random trails(with inertia)')
    for i in xrange(10):
        v, (x, y) = pso(10, 100, inertia=True)
        print('value: %f, x: %f, y: %f' % (v, x, y))
