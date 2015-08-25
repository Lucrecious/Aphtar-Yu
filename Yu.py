from bge import logic
import mathutils as mt
from Player import Player, Animation
import nilutils as nl
import aud
	
	
class Shooting(nl.Component):
	def __init__(self, gobj):
		
		super().__init__(gobj)
		
		#sound
		self.device = aud.device()
		sound = logic.expandPath("//sounds/yu_gun.ogg")
		factory = aud.Factory(sound)
		self.factory = aud.Factory.buffer(factory)
		
		self.bullet_obj = "i_bullet"
		
		self.fire_speed = 5 #every 5 frames
		
		self.empty = self.gobj.empty
		
		self.joystick = self.gobj.joystick
		
		self.tick = nl.Ticker(0.04)
		
		self.state("shoot")
		
	def shoot(self):
		
		joy_vect = self.joystick.values(4, 3)
		
		if joy_vect.magnitude and self.tick():
			logic.getCurrentScene().addObject(self.bullet_obj, self.empty, 50)
			handle = self.device.play(self.factory)
			handle.volume = 0.3

class Yu (Player):
	def __init__(self, own):
		super().__init__(own)
		
		self.run_frames = [0, 40]
		self.idle_frames = [0, 100]
		
		shooting = Shooting(self)
		animation = Animation(self)
		self.components.append(shooting)
		self.components.append(animation)
		

		
def init(cont):
	Yu(cont.owner)
	
def main(cont):
	cont.owner.main()