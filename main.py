import pygame, random, math, time, pygame.freetype
from particleFuncs import * 
pygame.init()

#initializes the specified number of particles
number_of_particles = 1
my_particles = []
for n in range(number_of_particles):
	size = 40
	density = random.randint(1, 5)
	x = width / 2
	y = 20
	particle = Particle((x, y), size, density * size ** 2,)
	particle.speed = 0
	particle.angle = random.uniform(0, math.pi*2)
	my_particles.append(particle)

#defines the positions of obstacles
number_of_obstacles = 30
obx = [30,150,270,390,510,630,750]
oby = [150,250,350,450,550,650]
layer = 0
column = 0
#initializes the specified number of obstacles
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

#initializes the specified number of goals
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
hasleadered = False
while running:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			#determines when to drop the ball
			if event.key == pygame.K_SPACE:
				activated = True
				for i, particle in enumerate(my_particles):
					#drops the ball at an angle
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

	if (pygame.time.get_ticks()/1000) >= 60:
		timegone = True
	
	if not timegone:	
		screen.blit(irithyll, (0, 0))
		myfont.render_to(screen, (40, 0), "YOU HAVE 60 SECONDS", (0, 0, 0))
		myfont.render_to(screen, (40, 60), "time "+str(math.floor((pygame.time.get_ticks()/1000))), (0, 0, 0))
		myfont.render_to(screen, (40, 80), "score "+str(score), (0, 0, 0))
		
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
					particle.speed = 0
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
		myfont2.render_to(screen, (225, 400), "SCORE "+str(score), (97, 33, 33))

		if hasleadered == False:
			leader = open("leaderboard.txt", "a")
			leader.write(str(score) + "\n")
			leader.close()

			leader = open("leaderboard.txt", "r")
			scores = []
			for line in leader:
				scores.append(int(line))
			leader.close()

			quicksort(scores, 0, (len(scores)-1))
			scores.reverse()

			hasleadered = True

		myfont2.render_to(screen, (225, 500), "Top 10 Scores:", (97, 33, 33))
		for i in range(5):
			myfont3.render_to(screen, (225, (580 + (40*i))), str(i + 1) + ") " + str(scores[i]), (97, 33, 33))
			myfont3.render_to(screen, (500, (580 + (40*i))), str(i + 6) + ") " + str(scores[i + 5]), (97, 33, 33))
		
	pygame.time.Clock().tick()
	pygame.display.flip()

pygame.quit ()