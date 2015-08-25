from Enemy import Enemy, Animation
import nilutils as nl
from bge import logic

class PhysicalEnemy(Enemy):
	def __init__(self, own):
		super().__init__(own)
		
		self.attack_frames = [0, 20]
		self.movement_frames = [0, 20]
		
		animation = Animation(self)
		
		self.components.append(animation)
		
		
def init(cont):
	PhysicalEnemy(cont.owner)
	
def main(cont):
	cont.owner.main()