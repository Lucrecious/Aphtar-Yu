import nilutils as nl
from mathutils import Vector
import random as  rand
from bge import logic
from bge import logic
import aud


class Follow(nl.Component):
	def __init__(self, gobj):
		super().__init__(gobj)
		
		self.state("track")
		
	def track(self):
		
		players = [p for p in self.objects if "player" in p and \
					not self.gobj.rayCast(p, self.gobj, 0, "wall")[0] and \
					self.gobj.getDistanceTo(p) < self.gobj.sight_distance]
		
		players.sort(key=lambda p: self.gobj.getDistanceTo(p))
		
		if len(players):
			closest = players[0]

			self.gobj.closest_player = closest
			
		else:
			self.gobj.closest_player = None
			
class Hurting(nl.Component):
	def __init__(self, gobj):
		super().__init__(gobj)
		
		
		self.device = aud.device()
		sound = logic.expandPath("//sounds/enemy_hurt.ogg")
		factory = aud.Factory(sound)
		self.factory = aud.Factory.buffer(factory)
		
		self.collision = self.gobj.collision
		
		self.state("damage_calc")
		
		
		
	def damage_calc(self):
		self.gobj.got_hit = False
		if self.collision.positive:
			hit_list = [b for b in self.collision.hitObjectList if "bullet" in b and\
						b['bullet']]
						
			self.gobj.health -= len(hit_list)
			if len(hit_list):
				self.gobj.got_hit = True
			
			
			for b in hit_list:
				b.endObject()
				handle = self.device.play(self.factory)
				handle.volume = 0.3
				return
				
		if self.gobj.health <= 0:
			self.gobj.dead = True
			return
				
	
class Movement(nl.Component):
	def __init__(self, gobj):
		
		super().__init__(gobj)
		
		self.patrol_ticker = 0
		self.patrol_sets = [Vector((1 ,0 , 0)), Vector((0, 1, 0))]
		self.patrol_speed = 5
		
		self.patrol_vect = Vector((0 ,0 ,0))
		
		self.collision = self.gobj.sensors['Collision']
		
		self.follow_speed = self.patrol_speed * 1.6
		
		self.state("randomize_patrol")
		
		
	def patrol(self):
		self.gobj.attack = False
		self.gobj.worldLinearVelocity = self.patrol_vect*self.patrol_speed
		self.gobj.alignAxisToVect(self.patrol_vect, 1, 0.5)
		self.gobj.alignAxisToVect(Vector((0, 0, 1)), 2, 1)
		
		if self.patrol_ticker():
			self.patrol_vect *= -1
			
		
		if self.gobj.closest_player:
			self.gobj.worldLinearVelocity.magnitude = 0
			self.state("follow_player")
			
		if self.gobj.dead:
			self.state("dead")
	
	def track_to(self, other):
		delta = other.worldPosition - self.gobj.worldPosition
		delta.normalize()
		self.gobj.alignAxisToVect(delta, 1, 1)
		self.gobj.alignAxisToVect(Vector((0 , 0, 1)), 2, 1)
	
	def dead(self):
		self.gobj.components = None
		self.gobj.endObject()
		return
	
	def follow_player(self):
		hit_list = []
		if self.collision.positive:
			hit_list  = [p for p in self.collision.hitObjectList if "player" in p]
		
		self.gobj.attack = True
		if self.gobj.closest_player:
			if self.gobj.getDistanceTo(self.gobj.closest_player) < self.gobj.stop_distance or\
				len(hit_list):
				self.gobj.localLinearVelocity.y = 0
			else:
				self.gobj.localLinearVelocity.y = self.follow_speed
				self.gobj.localLinearVelocity.magnitude = self.follow_speed
				
			
			self.track_to(self.gobj.closest_player)
			
		else:
			self.state("randomize_patrol")
			self.gobj.localLinearVelocity.magnitude = 0
			return
			
		if self.gobj.dead:
			self.state("dead")
		
		
	def randomize_patrol(self):
		self.patrol_ticker = nl.Ticker(rand.randint(2,4))
		self.patrol_vect = rand.choice(self.patrol_sets)
		
		self.state("patrol")

class Animation(nl.Component):
	def __init__(self, gobj):
		super().__init__(gobj)
	
		self.armature = [a for a in self.gobj.children if "armature" in a][0]
		self.mode = logic.KX_ACTION_MODE_LOOP
		self.attack_animation = self.gobj['who']+"_attack"
		self.movement_animation = self.gobj['who']+"_movement"
		
		self.attack_frames = self.gobj.attack_frames
		self.movement_frames = self.gobj.movement_frames
		
		self.state("wait")
	
	def wait(self):
		
		if self.gobj.attack:
			self.armature.playAction(self.attack_animation, \
			self.attack_frames[0], \
			self.attack_frames[1], 1, 1, 1.0, self.mode, 0, 1, 1)
		else:
			self.armature.playAction(self.movement_animation, \
			self.movement_frames[0], \
			self.movement_frames[1], 1, 1, 1.0, self.mode, 0, 1, 1)	
		

class Enemy(nl.GameObject):
	def __init__(self, own):
		
		self.health_max = 20
		self.health = self.health_max
		self.dead = False
		
		self.attack_frames = [0, 0]
		self.movement_frames = [0, 0]
		
		self.closest_player = None
		
		self.stop_distance = self['stop_dist']
		self.sight_distance = self['sight_dist']
		self.collision = self.sensors['Collision']
		
		follow = Follow(self)
		hurting = Hurting(self)
		
		self.attack = False
		
		self.got_hit = False
		
		self.components = [follow, hurting]
		if self['enemy'] != "goat":
			movement = Movement(self)
			self.components.append(movement)
		
		
		
	