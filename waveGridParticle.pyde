fc = 2

xn = 2*36/fc
yn = xn
r = 2
A = 2**.5*1080./(xn*fc)
f = 12/fc
v = 1

nframe = 60
N_PHI = abs(nframe*f)

# each vector is the origin of a wave source
p1 = PVector(random(1080)/fc,random(1080)/fc)
p2 = PVector(random(1080)/fc,random(1080)/fc)
p3 = PVector(random(1080)/fc,random(1080)/fc)
p4 = PVector(random(1080)/fc,random(1080)/fc)

def setup():
    global saver,po,p
    size(1080/fc,1080/fc,FX2D)
    colorMode(HSB,1)
    ellipseMode(RADIUS)
    noStroke()
    background(0)
    ##
    po = PVector(width/2.,height/2.)
    p = Psyst(xn,yn,r)

def draw():
    background(0)
    p.show()

# Calculates radial waves
def sine(t,A,x,y,xo,yo,fq,v,phi):
    """ t: current time fraction; A: amplitude; x,y: position of element;
        xo,yo: position of source; fq: frequency; v: wave velocity; phi: phase"""
    wh = (width**2 + height**2)**0.5
    k = TWO_PI*fq/(wh*v)
    w = TWO_PI*fq
    r = ((x-xo)**2 + (y-yo)**2)**0.5
    z = A*sin(k*r - w*t + phi)
    return z

############################
###### PARTICLE CLASS ######
############################
class particle():
    # Particle objects
    def __init__(self,x,y,r):
        # position vector
        self.pos = PVector(x,y)
        # moved position vector (where the particle is displayed)
        self.move = PVector(0,0)
        # next move vector, used for calculating the next position
        self.nmove = PVector(0,0)
        # intermediate move vector, buffer to store previous position while new ones are calculated
        self.imove = PVector(0,0)
        # radius, if displaying ellipses
        self.r = r
        self.c = color(1)
        # Calculate vectors of direction in relation to wave source(s)
        pp1 = PVector.sub(self.pos,p1)
        # pp2 = PVector.sub(self.pos,p2)
        # pp3 = PVector.sub(self.pos,p3)
        # pp4 = PVector.sub(self.pos,p4)
        # pa = PVector.add(pp1,pp2)
        # pb = PVector.add(pp3,pa)
        # ps = PVector.add(pa,pb)
        # Direction shift vector
        self.shift = pp1.copy().normalize()
    
    def update(self,m):
        # Multiplies the self.shift by magnitude m to give
        # new position for particle
        self.imove = self.nmove.copy()
        self.nmove = PVector.add(self.pos,self.shift.copy().setMag(m))
        # calculate a value for use in color depending on how much the
        # particle has shifted
        h = abs(map(abs(m),-A,A,317./360,206./360))
        self.c = color(h,1,1)
    
    # Use after nmove has been calculated in update() for all particles
    def updatemove(self):
        self.move = self.imove.copy()
    
    # For displaying particles
    def show(self):
        fill(self.c)
        noStroke()
        ellipse(self.move.x,self.move.y,self.r,self.r)
        # point(x,y)

class Psyst():
    # Particle system
    # nx,ny: number of particles in x,y axes
    def __init__(self,nx,ny,r,extra=True):
        self.t = 0
        self.r = r
        if extra:
            # Add to rows/columns outside of canvas to
            # avoid empty edges when particles move inside too much;
            # calculate their positions, create array of particles
            self.nx = nx + 4
            self.ny = ny + 4
            self.n = self.nx*self.ny
            mloc = (nx-1) + (ny-1)*nx
            dx =  width*(1. - (mloc%nx)/(1.*nx))/2
            dy = height*(1. - (mloc/nx)/(1.*ny))/2
            self.ps = []
            for i in xrange(-2,nx+2):
                for j in xrange(-2,ny+2):
                    x =  width*1.*i/nx + dx
                    y = height*1.*j/ny + dy
                    self.ps.append(particle(x,y,r))
            
        else:
            # Calculate particle positions without extra particles 
            # on edges
            self.nx = nx
            self.ny = ny
            self.n = nx*ny
            
            dx =  width*(1. - ((self.n-1)%nx)/(1.*nx))/2
            dy = height*(1. - ((self.n-1)/nx)/(1.*ny))/2
            self.ps = [None]*self.n
            for loc in xrange(self.n):
                x =  width*1.*(loc%nx)/nx + dx
                y = height*1.*(loc/nx)/ny + dy
                self.ps[loc] = particle(x,y,r)
    
    def show(self):
        self.gettime()
        for i in xrange(self.n):
            ## update values
            x = self.ps[i].pos.x
            y = self.ps[i].pos.y
            # Calculate value(s) for wave source(s)
            s1 = sine(self.t, A, x, y, p1.x,p1.y, f, v, 0)
            # s2 = sine(self.t, A, x, y, p2.x,p2.y, f, v, 0)
            # s3 = sine(self.t, A, x, y, p3.x,p3.y, f, v, 0)
            # s = (s1 + s2 + s3)/3.
            # s = (s1 + s2)/2
            self.ps[i].update(s1)
            ### make a grid and/or display particles
            self.grid(i)
            # self.ps[i].show()\
        # push the next move positions for next frame
        for i in xrange(self.n):
            self.ps[i].updatemove()
    
    def grid(self,i):
        ## Make a grid
        # if i == self.n-1:
        #     return
        stroke(self.ps[i].c)
        strokeWeight(2)
        # if i%self.nx in [0,self.nx-1] or i/self.nx in [0,self.ny]:
        #     return
        i1 = i+1
        i2 = i+self.nx
        if i2 < self.n:
            line(self.ps[i].move.x,self.ps[i].move.y,self.ps[i2].move.x,self.ps[i2].move.y)
        if i1%self.nx != 0:
            line(self.ps[i].move.x,self.ps[i].move.y,self.ps[i1].move.x,self.ps[i1].move.y)
            
    
    def gettime(self):
        # Current time value
        self.t = 1.*frameCount/N_PHI
