def center_of_vel():
	cov = np.zeros(DIMENSIONS)

	for dimension in range(DIMENSIONS):
		for rock in rock_group:
			cov[dimension] = cov[dimension] + rock.vel[dimension]
		cov[dimension] = cov[dimension]/len(rock_group)
	return cov

def center_of_pos():
	cop = np.zeros(DIMENSIONS)

	for dimension in range(DIMENSIONS):
		for rock in rock_group:
			cop[dimension] = cop[dimension] + rock.get_pos()[dimension]
		cop[dimension] = cop[dimension]/len(rock_group)
	return cop

def alignment():
	for rock in rock_group:
		steer1 = np.zeros(DIMENSIONS)
		steer1 = (center_of_vel() - rock.vel)*alignmentWeight
		rock.vel = rock.vel + steer1
		rock.pos = rock.pos + rock.vel


def cohesion():
	for rock in rock_group:
		steer2 = np.zeros(DIMENSIONS)
		steer2 = (center_of_pos() - rock.get_pos())*centerOfMassWeight
		rock.vel = rock.vel + steer2
		rock.pos = rock.pos + rock.vel

def separation():

	for rock in rock_group:
		steer3 = np.zeros(DIMENSIONS)
		for rock2 in rock_group:
			difference = np.stack(rock2.get_pos()) - np.stack(rock.get_pos())
			distance = np.linalg.norm(difference)
			if distance < separationDistance and rock2 != rock:
				steer3 = steer3 - difference/distance
		rock.vel = rock.vel + steer3*separationWeight
		rock.pos = rock.pos + rock.vel

def avoid_ship():
	for rock in rock_group:
		steer4 = np.zeros(DIMENSIONS)
		difference = np.stack(my_ship.get_pos()) - np.stack(rock.get_pos())
		distance = np.linalg.norm(difference)
		if distance < avoidDistance:
			steer4 = (steer4 - difference)*avoidWeight
		rock.vel = rock.vel + steer4
		rock.pos = rock.pos + rock.vel 

def attack_ship():
	for rock in rock_group:
		steer5 = np.zeros(DIMENSIONS)
		difference = np.stack(rock.get_pos()) - np.stack(my_ship.get_pos())
		distance = np.linalg.norm(difference)
		if distance < attackDistance:
			steer5 = (steer5 - difference)*attackWeight
		rock.vel = rock.vel + steer5
		rock.pos = rock.pos + rock.vel 
