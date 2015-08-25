from bge import logic
import nilutils as nl
import random as rand

class Bullet(nl.GameObject):
		
	def stay_up(self):
		self.applyForce = [0, 0, 9.8]
		self.worldLinearVelocity.z = 0

class PlayerBullet(Bullet):
	def __init__(self, own):
		super().__init__(own)
		
		self.collision = self.sensors["Collision"]
		
		self.type = self['bullet']
		
		self.speed = [25, 40]
		
		self.side = rand.choice([-1, 0, 1])
		
	def main(self):
	
		self.stay_up()
		
		self.localLinearVelocity.y = self.speed[self.type]
		self.localLinearVelocity.x = self.side
		
	
		if self.collision.positive:
			hit_list = self.collision.hitObjectList
			walls = [h for h in hit_list if "wall" in h]
			players = [h for h in hit_list if "player" in h and h["player"] != self.type]
			
			if len(players) or len(walls):
				self.endObject()
				return
			
				
		
		

		
		
def init(cont):
	PlayerBullet(cont.owner)
	
def main(cont):
	cont.owner.main()
