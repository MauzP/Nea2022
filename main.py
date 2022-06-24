import pygame, random, math, time, pygame.freetype
from PyParticles import * 
pygame.init()

#creates the specified number of particles
number_of_particles = 1
my_particles = []
for n in range(number_of_particles):
	size = 50
	density = random.randint(1, 5)
	x = width / 2
	y = 20
	particle = Particle((x, y), size, density * size ** 2)
	particle.speed = 0
	particle.angle = random.uniform(0, math.pi*2)
	my_particles.append(particle)

number_of_obstacles = 1
my_obstacles = []
for n in range(number_of_obstacles):
	size = (random.randint(20,50),random.randint(20,50))
	position = (random.randint(0,width),random.randint(0,height))
	obstacle = Obstacle(position, size)
	my_obstacles.append(obstacle)
	
#runs the simulation
running = True
selected_particle = None
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			selected_particle = findParticle(my_particles, mouseX, mouseY)
		elif event.type == pygame.MOUSEBUTTONUP:		
			selected_particle = None
			
	if selected_particle:
		(mouseX, mouseY) = pygame.mouse.get_pos()
		dx = mouseX - selected_particle.x
		dy = mouseY - selected_particle.y
		selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
		selected_particle.speed = math.hypot(dx, dy) * 0.1
		
	screen.fill(background_colour)
	
	for i, particle in enumerate(my_particles):
		particle.move()
		particle.bounce()
		for particle2 in my_particles[i+1:]:
			collide(particle, particle2)
		particle.display()

	for i, obstacle in enumerate(my_obstacles):
		obstacle.display()
	
	pygame.display.flip()

pygame.quit ()