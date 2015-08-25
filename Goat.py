from Enemy import Enemy
from bge import logic
import nilutils as nl
import random as rand


class Attack(nl.Component):
	def __init__(self, gobj):
		super().__init__(gobj)
		
		self.max_health = 1
		self.health = self.max_health
		
		self.states = ['spin_attack', 'wave_attack']
		self.current_rotation = 1
		
		self.state('random_state')
		
		self.shots = 0
		self.shots_last = 0
		
		self.shots_per_stage = 100
		
		self.empty = [c for c in self.gobj.children if "empty" in c][0]
		self.shot_delay = nl.Ticker(self.gobj['shoot_delay'])
		
	def random_state(self):
		self.shots = 0
		self.shots_last = 0
		state = rand.choice(self.states)
		
		self.state(state)
	
	def shoot(self):
		if self.shot_delay():
			self.shots += 1
			self.gobj.scene.addObject("g_bullet1", self.empty, 150)
			
	
	def spin_attack(self):
		
		self.spin_empty()
		
		self.shoot()
		
		if self.shots > self.shots_per_stage:
			self.state("random_state")
			return
			
		
		
	def wave_attack(self):
		self.wave_empty()
		
		self.shoot()
		
		if self.shots > self.shots_per_stage:
			self.state("random_state")
		
	def spin_empty(self):
		self.empty.applyRotation([0, 0, 0.1])
		
	def wave_empty(self):
		self.empty.applyRotation([0, 0, 0.1*self.current_rotation])
		
		if self.shots - self.shots_last == 10:
			self.shots_last = self.shots
			self.current_rotation *= -1
			
			
class Red (nl.Component):
	def __init__(self, gobj):
		super().__init__(gobj)
		
		self.red_goat = [r for r in self.gobj.children if "red" in r][0]
		
		self.state("turn_red")
		
	def turn_red(self):
		if self.gobj.got_hit:
			self.red_goat.setVisible(True)
		else:
			self.red_goat.setVisible(False)
			
		if self.gobj.dead:
			self.gobj.sendMessage("deadgoat")
			self.gobj.endObject()
			return
		
		
class Goat(Enemy):
	
	def __init__(self, own):
		super().__init__(own)
		
		self.max_health = 100
		self.health = 100
		
		attack = Attack(self)
		red = Red(self)
		self.components.append(attack)
		self.components.append(red)
		
		

		
def init (cont):
	Goat(cont.owner)
	
def main (cont):
	cont.owner.main()
		
	