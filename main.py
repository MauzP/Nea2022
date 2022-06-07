import pygame, random, math, time, pygame.freetype

#variables
#width, height = 500, 400
width, height = 775, 420
pygame.init()
pygame.display.set_caption('  Physikas')
myfont = pygame.freetype.SysFont('Comic Sans MS', 20)
screen = pygame.display.set_mode((width, height))
background_colour = 130, 209, 209
gravity = (math.pi, 0.02)
drag = 0.999
elasticity = 0.75
mass_of_air = 0.2

#function to add a vector to an object
def addVectors(inp1, inp2):
	angle1, length1 = inp1
	angle2, length2 = inp2
	x = math.sin(angle1) * length1 + math.sin(angle2) * length2
	y = math.cos(angle1) * length1 + math.cos(angle2) * length2
	length = math.hypot(x, y)
	angle = 0.5 * math.pi - math.atan2(y, x)
	return (angle, length)

#checks location of particle
def findParticle(particles, x, y):
	for p in particles:
		if math.hypot(p.x-x, p.y-y) <= p.size:
			return p

#class for a physics object
class Particle:
	def __init__(self, position, size, mass=1):
		self.x, self.y = position
		self.size = size
		self.mass = mass
		self.colour = (255, 0, 0)
		self.thickness = 1000
		self.speed = 0.1
		self.angle = 0
		self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size
	def display(self):
		ball = pygame.image.load("ball.png").convert_alpha()
		ball = pygame.transform.scale(ball, (self.size, self.size))
		screen.blit(ball, (int(self.x), int(self.y)))		
	def move(self):
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) * self.speed
		(self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
		self.speed *= self.drag
	def bounce(self):
		if self.x > width - self.size:
			self.x = 2 * (width - self.size) - self.x
			self.angle = - self.angle
			self.speed *= elasticity
		elif self.x < 0:
			self.x = 0.5 * self.size - self.x
			self.angle = - self.angle
			self.speed *= elasticity
		if self.y > height - self.size:
			self.y = 2 * (height - self.size) - self.y
			self.angle = math.pi - self.angle
			self.speed *= elasticity
		elif self.y < 0:
			self.y = 0.5 * self.size
			self.angle = math.pi - self.angle
			self.speed *= elasticity

#creates the specified number of particles
number_of_particles = 1
my_particles = []
for n in range(number_of_particles):
	size = random.randint(20, 50)
	density = random.randint(1, 20)
	x = random.randint(size, width-size)
	y = random.randint(size, height-size)
	particle = Particle((x, y), size, density * size ** 2)
	particle.speed = (random.randint(1, 10) / 5)
	particle.angle = random.uniform(0, math.pi*2)
	my_particles.append(particle)
	
#runs the simulation
running = True
selected_particle = None
while running:
	screen.fill(background_colour)
	myfont.render_to(screen, (10, 10), "Gravity is " + str(gravity[1]), (0, 0, 0))
	myfont.render_to(screen, (10, 40), "Drag is " + str(drag), (0, 0, 0))
	myfont.render_to(screen, (10, 70), "Elasticity is " + str(elasticity), (0, 0, 0))
	myfont.render_to(screen, (10, 100), "Density of Medium is " + str(mass_of_air), (0, 0, 0))
	for particle in my_particles:
		if selected_particle:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			dx = mouseX - selected_particle.x
			dy = mouseY - selected_particle.y
			selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
			selected_particle.speed = math.hypot(dx, dy) * 0.1
		if particle != selected_particle:
			particle.move()
			particle.bounce()
		particle.display()
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			selected_particle = findParticle(my_particles, mouseX, mouseY)
		elif event.type == pygame.MOUSEBUTTONUP:		
			selected_particle = None

pygame.quit ()