import pygame, random, math, time, pygame.freetype
from particleFuncs import * 
pygame.init()

#creates the specified number of particles
number_of_particles = 1
my_particles = []
for n in range(number_of_particles):
	size = 40
	density = random.randint(1, 5)
	x = width / 2
	y = 20
	particle = Particle((x, y), size, density * size ** 2)
	particle.speed = 0
	particle.angle = random.uniform(0, math.pi*2)
	my_particles.append(particle)

number_of_obstacles = 30
obx = [30,150,270,390,510,630,750]
oby = [150,250,350,450,550,650]
layer = 0
column = 0
my_obstacles = []
for n in range(number_of_obstacles):
	for i in range(len(oby)):
		for j in range(len(obx)):
			size = 25
			if i % 2 == 0:
				position = (obx[j],oby[i])
			else:
				position = (obx[j]-60,oby[i])
			obstacle = Obstacle(position, size)
			my_obstacles.append(obstacle)

goaln = [[0,75,225,350,425,550,700,800], [75,150,125,75,125,150,75], [10,25,50,100,50,25,10]]
my_goals = []
for n in range(7):
	goal = Goal(goaln[0][n],goaln[1][n],goaln[2][n])
	my_goals.append(goal)

			
#runs the simulation
running = True
selected_particle = None
activated = False
timegone = False
while running:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				activated = True
				for i, particle in enumerate(my_particles):
					if particle.horizontal > 0:
						particle.angle, particle.speed = addVectors((particle.angle, particle.speed), (math.pi/2, particle.horizontal))
					else:
						particle.angle, particle.speed = addVectors((particle.angle, particle.speed), (math.pi/2, particle.horizontal))
		if event.type == pygame.QUIT: 
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			selected_particle = findParticle(my_particles, mouseX, mouseY)
		elif event.type == pygame.MOUSEBUTTONUP:		
			selected_particle = None
			
	"""if selected_particle:
		(mouseX, mouseY) = pygame.mouse.get_pos()
		dx = mouseX - selected_particle.x
		dy = mouseY - selected_particle.y
		selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
		selected_particle.speed = math.hypot(dx, dy) * 0.1"""

	if (pygame.time.get_ticks()/1000) >= 60:
		timegone = True
	
	if not timegone:
		screen.fill(background_colour)
		myfont.render_to(screen, (40, 0), "YOU HAVE 60 SECONDS", (0, 0, 0))
		myfont.render_to(screen, (40, 60), "time "+str(pygame.time.get_ticks()/1000), (0, 0, 0))
		myfont.render_to(screen, (40, 80), "score "+str(int(score)), (0, 0, 0))
		
		for i, particle in enumerate(my_particles):
			if activated:
				particle.move()
				particle.bounce()
				for particle2 in my_particles[i+1:]:
					collide(particle, particle2)
				for obj in my_obstacles:
					objcollide(particle, obj)
				if particle.y > 725:
					for i in range(0, len(goaln[0])):
						if particle.x + 20 > goaln[0][i] and particle.x + 20 < goaln[0][i+1]:
							score = score + goaln[2][i]
					particle.x = width / 2
					particle.y = 20
					activated = False
			else:
				particle.horizontalm()
			particle.display()
		
		for i, obstacle in enumerate(my_obstacles):
			obstacle.display()
	
		for i, goal in enumerate(my_goals):
			goal.display()

	if timegone:
		screen.fill((0,0,0))
		gameover()
		myfont2.render_to(screen, (225, 500), "SCORE "+str(int(score)), (97, 33, 33))
	pygame.display.flip()

pygame.quit ()