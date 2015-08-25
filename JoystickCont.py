from math import fabs
import mathutils as mt

class Joystick:
	def __init__(self, joy):
		self.joy = joy
		
		self.threshold = 0.25 #percent
		
	def values(self, x, y):
		
		joy_vect = mt.Vector((self.joy.axisValues[x], -self.joy.axisValues[y]))
		
		
		return joy_vect if joy_vect.magnitude > self.threshold else mt.Vector((0, 0))