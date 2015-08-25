import nilutils as nl
from bge import logic
import random as rand
import math

class Spawner(nl.GameObject):
	def __init__(self, own):
		super().__init__(own)
		
		self.rounds = [[0, 0], [2, 0], [0, 2], [2, 2], [2, 4], [3, 6], [3, 6], [0, 0] ]
		
		
		self.round_delay = nl.Ticker(20)
		
		self.hud = [s for s in logic.getSceneList() if s.name == "HUD"][0]
		self.timer_text = self.hud.objects['time_left']
		self.round_text = self.hud.objects['round_text']
		self.gameover_text = self.hud.objects['gameover_text']
		
		self.message_recieved = self.sensors['Message']
		
		#Turn on their visibility
		self.timer_text.setVisible(True)
		self.round_text.setVisible(True)
		
		self.round = -1
		
	def main(self):
		
		
		self.timer_text["Text"] = "Time Left for Next Round: "+str(math.ceil(self.round_delay.delta - self.round_delay.time()))
		self.round_text['Text'] = "Round: "+ str(self.round)
		
		if self.round_delay():
			self.round = self.round + 1 if self.round < len(self.rounds)-1 else len(self.rounds)-1
			self.spawn_monsters(self.rounds[self.round])
		
		if self.round == len(self.rounds)-1:
			enemies = [e for e in self.scene.objects if "enemy" in e]
			if not len(enemies):
				self.sendMessage("GOAT")
			
		if self.message_recieved.positive:
			self.gameover_text['Text'] = "You win!\nPress A to\nplay again!"
			self.sendMessage("gameover")
		
	def spawn_monsters(self, round):
		order = [i for i in range(len(self.children))]
		rand.shuffle(order)
		
		for i in range(0, len(order)):
			if i < round[0]:
				
				self.scene.addObject("Enemy1", self.children[order[i]], 0)
			
			elif i >= round[0] and i < round[1]+round[0]:
				self.scene.addObject("Enemy2", self.children[order[i]], 0)
			
		
		
		
def init(cont):
	Spawner(cont.owner)
	
def main(cont):
	cont.owner.main()