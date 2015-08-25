import nilutils as nl
from bge import logic
from math import fabs


class Camera(nl.GameObject):
	def __init__(self, own):
		super().__init__(own)
		
		self.objects = logic.getCurrentScene().objects

		
		self.front_b = [i for i in self.childrenRecursive if "front" in i][0]
		self.back_b = [i for i in self.childrenRecursive if "back" in i][0]
		self.left_b = [i for i in self.childrenRecursive if "left" in i][0]
		self.right_b = [i for i in self.childrenRecursive if "right" in i][0]
		
	def main(self):
		p2 = [i for i in self.objects if "player" in i and i['player'] == 1][0]
		
		self.applyForce((0, 0, 9.8))
		self.worldLinearVelocity.z = 0
		

		delta_front = fabs((p2.worldPosition - self.front_b.worldPosition).y)
		delta_back = fabs((p2.worldPosition - self.back_b.worldPosition).y)
		delta_left = fabs((p2.worldPosition - self.left_b.worldPosition).x)
		delta_right = fabs((p2.worldPosition - self.right_b.worldPosition).x)
			
		if delta_front  < 2 or delta_back < 2 or delta_left < 2 or delta_right < 2:
			self.worldLinearVelocity.y = p2.worldLinearVelocity.y
			self.worldLinearVelocity.x = p2.worldLinearVelocity.x
				
		else:
			if fabs(self.worldLinearVelocity.x) > 0.25 or fabs(self.worldLinearVelocity.y) > 0.25:
				self.worldLinearVelocity.x *= 0.95
				self.worldLinearVelocity.y *= 0.95
			else:
				self.worldLinearVelocity.x = 0
				self.worldLinearVelocity.y = 0
		#print (self.worldLinearVelocity.magnitude)
		
def init(cont):
	Camera(cont.owner)

def main(cont):
	cont.owner.main()