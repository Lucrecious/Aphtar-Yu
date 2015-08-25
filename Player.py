import nilutils as nl
from JoystickCont import Joystick
import mathutils as mt
from bge import logic


class Movement(nl.Component):
	def __init__(self, gobj):
	
		super().__init__(gobj)
		
		self.speed = 17
		
		self.joystick = self.gobj.joystick
		self.joyvaluedict = {
			"xbox" : { "movement": (0, 1), "rotation" : (4, 3) },
			"ps4" : { "movement" : (0, 1), "rotation" : (2, 3) }
		}
		
		self.joyvalue = self.joyvaluedict["xbox"] if "xbox" in self.joystick.joy.name.lower() else self.joyvaluedict["ps4"]
		
		self.state("move")
		
	def move(self):
		
		#linear motion
		joy_vect = self.joystick.values(self.joyvalue["movement"][0], self.joyvalue["movement"][1])
		joy_vect.normalize()
		
		
		velocity = self.speed*joy_vect
		
		self.gobj.worldLinearVelocity.x = velocity.x
		self.gobj.worldLinearVelocity.y = velocity.y
		
		if joy_vect.magnitude:
			self.gobj.moving = True
		else:
			self.gobj.moving = False
		
		#rotational motion
		vect = self.joystick.values(self.joyvalue["rotation"][0], self.joyvalue["rotation"][1])
		
		joy_vect2 = mt.Vector((vect.x, vect.y, 0))
		
		if joy_vect2.magnitude:
			self.gobj.alignAxisToVect(joy_vect2, 1, 0.7)
			self.gobj.alignAxisToVect(mt.Vector((0, 0, 1)), 2, 1)
			

class Health(nl.Component):
	def __init__(self, gobj):
	
		super().__init__(gobj)
		
		self.collision = self.gobj.sensors["Collision"]
		
		self.health_bar = self.gobj.health_bar
		
		self.ticker = nl.Ticker(0.5)
		
		self.state("hurting")
		
	def hurting(self):
		
		if self.collision.positive:

			bullets = [h for h in self.collision.hitObjectList if "enemy_bullet" in h]
			enemy = [h for h in self.collision.hitObjectList if "enemy" in h]
			
			self.gobj.health -= len(bullets)
			
			if self.ticker():
				self.gobj.health -= len(enemy)
			
			percent = self.gobj.health/self.gobj.health_max
			size = percent if percent > 0 else 0

			
			#print(percent)
			
			health_scale = self.health_bar.worldScale
			
			self.health_bar.worldScale = [size, health_scale.y, health_scale.z]
			
			if size <= 0:
				self.gobj.sendMessage("gameover")
			
			for b in bullets:
				b.endObject()
				return
		

class Animation(nl.Component):
	def __init__(self, gobj):
		super().__init__(gobj)
		
		self.run_animation = "run_"+self.gobj['who']
		self.idle_animation = "idle_"+self.gobj['who']
		self.mode = logic.KX_ACTION_MODE_LOOP
		
		self.run_frames = self.gobj.run_frames
		self.idle_frames = self.gobj.idle_frames
		
		self.armature = [a for a in self.gobj.children if "armature" in a][0]
		
		self.state('wait')
		
		
	def wait(self):
		
		if self.gobj.moving:
			self.armature.playAction(self.run_animation, \
			self.run_frames[0], \
			self.run_frames[1], 1, 1, 1.0, self.mode, 0, 1, 3)
		else:
			self.armature.playAction(self.idle_animation, \
			self.idle_frames[0], \
			self.idle_frames[1], 1, 1, 1.0, self.mode, 0, 1, 1)

			
		
class Player (nl.GameObject):
	def __init__(self, own):
		
		self.health_max = 50
		
		self.health = self.health_max
		
		self.moving = False
		
		
		self.run_frames = [0, 0]
		self.idle_frames = [0, 0]
		
		
		self.joystick = Joystick(logic.joysticks[self['player']])
		
		self.empty = [c for c in self.children if "shooter" in c][0]
		self.health_bar = [c for c in self.children if "health" in c][0]
		
		movement = Movement(self)
		health = Health(self)
		self.components = [movement, health]
		
