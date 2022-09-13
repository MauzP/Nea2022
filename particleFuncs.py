import random, math, pygame

width, height = 775, 800
pygame.init()
pygame.display.set_caption("  Physikas")
myfont = pygame.freetype.Font("EBGaramond-Regular.ttf", 20)
myfont2 = pygame.freetype.Font("EBGaramond-Regular.ttf", 70)
screen = pygame.display.set_mode((width, height))
background_colour = 130, 209, 209
gravity = (math.pi, 0.2)
drag = 0.999
wallasticity = 0.85
elasticity = 0.85
mass_of_air = 0.2
score = 0

def loadimg(img):
  return pygame.image.load(img).convert_alpha()

irithyll = loadimg("Irithyll.jpg")
irithyll = pygame.transform.scale(irithyll, (width, height))

def gameover():
	death = loadimg("dead.png")
	death = pygame.transform.scale(death, (width, height/2))
	screen.blit(death, (0, 0))		

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

#checks for collision
def collide(p1, p2):
	dx = p1.x - p2.x
	dy = p1.y - p2.y
	distance = math.hypot(dx, dy)
	if distance < (p1.size)/2 + (p2.size)/2:
		tangent = math.atan2(dy, dx)
		angle = 0.5 * math.pi + tangent
		angle1 = 2 * tangent - p1.angle
		angle2 = 2 * tangent - p2.angle
		speed1 = p2.speed * elasticity
		speed2 = p1.speed * elasticity
		(p1.angle, p1.speed) = (angle1, speed1)
		(p2.angle, p2.speed) = (angle2, speed2)
		p1.x += math.sin(angle)
		p1.y -= math.cos(angle)
		p2.x -= math.sin(angle)
		p2.y += math.cos(angle)

def objcollide(p, obj):
	dx = p.x - (obj.x - 20)
	dy = p.y - (obj.y - 20)
	distance = math.hypot(dx, dy)
	if distance < (p.size)/2 + (obj.radius):
		tangent = math.atan2(dy, dx)
		angle = 0.5 * math.pi + tangent
		anglep = 2 * tangent - p.angle
		speed = p.speed * elasticity
		(p.angle, p.speed) = (anglep, speed)
		p.x += math.sin(angle)
		p.y -= math.cos(angle)

def goalcollide(particle, goal):
	return
#class for a physics object
class Particle:
	def __init__(self, position, size, mass=1):
		self.x, self.y = position
		self.size = size
		self.mass = mass
		self.colour = (255, 0, 0)
		self.thickness = 500
		self.speed = 0.5
		self.angle = 0
		self.drag = (self.mass/(self.mass + mass_of_air)) ** self.size
		self.horizontal = 1
	def display(self):
		ball = loadimg("ball.png")
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
			self.speed *= wallasticity
		elif self.x < 0:
			self.x = 0.2 * self.size - self.x
			self.angle = - self.angle
			self.speed *= wallasticity
		if self.y > height - self.size:
			self.y = 2 * (height - self.size) - self.y
			self.angle = math.pi - self.angle
			self.speed *= wallasticity
		elif self.y < 0:
			self.y = 0.5 * self.size
			self.angle = math.pi - self.angle
			self.speed *= wallasticity
	def horizontalm(self):
		if self.x > 0 and self.x < width - self.size:
			self.x += self.horizontal
		else:
			self.horizontal = 0-(self.horizontal)
			if self.x < 10:
				self.x = 5
			else:
				self.x = width - (self.size*1.5)
			
			

class Obstacle:
	def __init__(self, position, size):
		self.x, self.y = position
		self.radius = size
		self.colour = (105, 155, 224)
		self.thickness = 1000
	def display(self):
		pygame.draw.circle(screen, self.colour, (self.x,self.y), self.radius, self.thickness)

class Goal:
	def __init__(self, position, width, score):
		self.x = position
		self.width = width
		self.score = score
		self.g = random.randint(self.score,255)
		self.b = random.randint(self.score,255)
		self.colour = (0, self.g, self.b)
		self.rect = pygame.Rect((self.x, (height-50)), (self.width, 50))
	def display(self):
		pygame.draw.rect(screen, self.colour, self.rect)
		myfont.render_to(screen, ((self.x + self.width/2)-10, (height-25)), str(self.score), (255, 255-self.g, 255-self.b))