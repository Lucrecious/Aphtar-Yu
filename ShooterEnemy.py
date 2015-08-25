from bge import logic
import nilutils as nl
from Enemy import Enemy, Animation


class Shooting(nl.Component):
	def __init__(self, gobj):
		super().__init__(gobj)
		
		self.state("shoot")
		
		self.empty = self.gobj.empty
		self.shoot_delay = nl.Ticker(self.gobj.shoot_delay)
		
		
	def shoot(self):
		scene = logic.getCurrentScene()
		if self.shoot_delay() and self.gobj.closest_player and not self.gobj.dead:
			scene.addObject("e_bullet1", self.empty, 100)
			
		

class ShooterEnemy(Enemy):
	def __init__(self, own):
		super().__init__(own)
		
		self.empty = [e for e in self.children if "empty" in e][0]
		self.shoot_delay = self['shoot_delay']
		
		self.attack_frames = [0, 5]
		self.movement_frames = [0, 20]
		
		
		animation = Animation(self)
		shooting = Shooting(self)
		self.components.append(shooting)
		self.components.append(animation)
		
		
def init(cont):
	ShooterEnemy(cont.owner)
	
def main(cont):
	cont.owner.main()