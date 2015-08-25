from bge import logic
import mathutils as mt
from Player import Player
from JoystickCont import Joystick
import nilutils as nl
import random as rand
from Player import Animation

import aud

class Reflect(nl.Component ):
	def __init__(self, gobj):
		super().__init__(gobj)
		
		#sound
		self.device = aud.device()
		sound = logic.expandPath("//sounds/aphtar_gun.ogg")
		factory = aud.Factory(sound)
		self.factory = aud.Factory.buffer(factory)
		
		
		bullet = "r__bullet"
		
		self.state("reflect")
		self.collision = self.gobj.sensors['Collision']
		
		self.hit = None
		
	def reflect(self):
		if self.collision.positive:

			hit_list =  [b for b in self.collision.hitObjectList if "bullet" in b and\
						not b["bullet"]]
			if len(hit_list):
				logic.getCurrentScene().addObject("r_bullet", self.gobj.empty, 50)
				handle = self.device.play(self.factory)
				handle.volume = 0.3
				
		
	
		
		

class Aphtar (Player):
	def __init__(self, own):
		super().__init__(own)
		
		self.run_frames = [0, 40]
		self.idle_frames = [0, 100]
		
		reflect = Reflect(self)
		animation = Animation(self)
		self.components.append(reflect)
		self.components.append(animation)
		

		
def init(cont):
	Aphtar(cont.owner)
	
def main(cont):
	cont.owner.main()