from bge import logic
import nilutils as nl
from PlayerBullet import Bullet

class EnemyBullet(Bullet):
	def __init__(self, gobj):
		super().__init__(gobj)
		
		self.speed = 15
		
		self.collision = self.sensors["Collision"]
		
	def main(self):
		self.stay_up()
		self.localLinearVelocity.y = self.speed
		
		if not "goat" in self:
			if self.collision.positive:
				walls = [w for w in logic.getCurrentScene().objects if "wall" in w]
				
				if len(walls):
					self.endObject()
					return
		

def init(cont):
	EnemyBullet(cont.owner)
	
def main(cont):
	cont.owner.main()