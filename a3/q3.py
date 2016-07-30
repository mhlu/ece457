from random import uniform, random
class Particle:
    def __init__(self):
        self.fit = None
        self.pBest = None
        self.v = None
        self.x = None

def camelBack(x, y):
    return float((4-2.1*pow(x,2)+pow(x,4)/3)*pow(x,2)+x*y+(-4+4*pow(y,2))*pow(y,2))

def pso(popSize, iterMax, w=0.79, c1=1.49, c2=1.49):
    particles = []
    gBest = None
    for i in xrange(popSize):
        p = Particle()
        # p.x = (uniform(-3, 3), uniform(-2, 2))
        p.x = (uniform(-100000, 100000), uniform(-100000, 100000))
        p.fit = camelBack(p.x[0], p.x[1])
        p.v = (0.0, 0.0)
        p.pBest = (p.fit, p.x)
        particles.append(p)

        if gBest is None or gBest[0] > p.fit:
            gBest = (p.fit, p.x)

    for i in xrange(iterMax):
        for p in particles:
            socialPos = gBest[1]
        
            v0 = w*p.v[0] \
                + c1*random()*(p.pBest[1][0]-p.x[0]) \
                + c2*random()*(socialPos[0]-p.x[0])
            v1 = w*p.v[1] \
                + c1*random()*(p.pBest[1][1]-p.x[1]) \
                + c2*random()*(socialPos[1]-p.x[1])

            p.x = (p.x[0]+v0, p.x[1]+v1)
            p.fit = camelBack(p.x[0], p.x[1])

            if p.pBest[0] > p.fit:
                p.pBest = (p.fit, p.x)

            if gBest[0] > p.fit:
                gBest = (p.fit, p.x)

    return gBest

if __name__ == "__main__":
    # random run
    v, (x, y) = pso(20, 20)
    print('value: %f, x: %f, y: %f' % (v, x, y))

    # inertia weight
    v, (x, y) = pso(20, 20)
    print('value: %f, x: %f, y: %f' % (v, x, y))

    #   
    v, (x, y) = pso(20, 20)
    print('value: %f, x: %f, y: %f' % (v, x, y))
