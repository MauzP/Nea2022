import random, math, pygame

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
balls = ["ball1.png", "ball2.png" ,"ball3.png"]

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
		self.image = balls[random.randint(0,len(balls)-1)]
	def display(self):
		ball = pygame.image.load(self.image).convert_alpha()
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
			self.x = 0.2 * self.size - self.x
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