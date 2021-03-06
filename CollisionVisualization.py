#Visulization using POVray for two particle collision
#import the appropriate ESyS-Particle modules:
from esys.lsm import *
from esys.lsm.util import Vec3, BoundingBox
from esys.lsm.vis import povray
def snapshot(particles=None, index=0):
pkg = povray
scene = pkg.Scene()
for pp in particles:
povsphere = pkg.Sphere(pp.getPosn(), pp.getRadius())
povsphere.apply(pkg.Colors.Red)
scene.add(povsphere)
camera = scene.getCamera()
camera.setLookAt(Vec3(0,0,0))
camera.setPosn(Vec3(0,0,20))
camera.setZoom(0.1)
scene.render(
offScreen=True,
interactive=False,
fileName="snap_{0:04d}.png".format(index),
size=[800,600]
)
return
#instantiate a simulation object
#and initialise the neighbour search algorithm:
sim = LsmMpi(numWorkerProcesses=1, mpiDimList=[1,1,1])
sim.initNeighbourSearch(
particleType="NRotSphere",
gridSpacing=2.5,
verletDist=0.5
)
#set the number of timesteps and timestep increment:
sim.setNumTimeSteps(10000)
sim.setTimeStepSize(0.001)
#specify the spatial domain for the simulation:
domain = BoundingBox(Vec3(-20,-20,-20), Vec3(20,20,20))
sim.setSpatialDomain(domain)
#add the first particle to the domain:
particle=NRotSphere(id=0, posn=Vec3(-5,5,-5), radius=1.0, mass=1.0)
particle.setLinearVelocity(Vec3(1.0,-1.0,1.0))
sim.createParticle(particle)
#add the second particle to the domain:
particle=NRotSphere(id=1, posn=Vec3(5,5,5), radius=1.5, mass=2.0)
particle.setLinearVelocity(Vec3(-1.0,-1.0,-1.0))
sim.createParticle(particle)
#specify the type of interactions between colliding particles:
sim.createInteractionGroup(
NRotElasticPrms(
name = "elastic_repulsion",
normalK = 10000.0,
scaling = True
)
)
#compute the specified number of timesteps:
N_max = sim.getNumTimeSteps()
n=0
while (n < N_max):
#compute a single timestep:
sim.runTimeStep()
# Take a snapshot of the simulation every 100 timesteps:
if (n%100==0):
particles = sim.getParticleList()
snapshot(particles=particles, index=n)
# update the total number of timesteps computed (n):
n += 1
#Exit the simulation.
sim.exit()
