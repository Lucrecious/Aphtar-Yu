import nilutils as nl
from bge import logic

class Tutorial(nl.GameObject):
	def __init__(self, own):
		super().__init__(own)
		
		self.hud = [s for s in logic.getSceneList() if s.name == "HUD"][0]
		self.info_text = self.hud.objects['info_text']
		self.press_start = self.hud.objects['press_start']
		self.info_text['Text'] = ""
		self.info_text.setVisible(True)
		self.press_start.setVisible(True)
		
		self.delay_timer = nl.Ticker(5)
		
		self.info_order = [
		"Hello",
		"Yu can shoot\nwith the right stick.",
		"Try shooting, Yu.",
		"Good.",
		"Aphtar can aim\nwith the right stick.",
		"Now, kill this enemy."
		]
		
		self.info_part = -1
		
	def main(self):
		
		if self.info_part < len(self.info_order):
			self.info_text['Text'] = self.info_order[self.info_part]
			
		if self.delay_timer() and self.info_part != 2:
			self.info_part += 1
		
		if self.info_part == 6:
			obj = self.scene.addObject("Enemy1.001", self, 0)

			self.info_part += 1
		
		
		enemies = [e for e in self.scene.objects if "enemy" in e]
		if self.info_part > 6 and not len(enemies):
			self.info_text['Text'] = "Good. \nStart survival when\n you're ready."
			
			
		if self.info_part == 2:
			bullets = [i for i in self.scene.objects if "bullet" in i]
			if len(bullets):
				self.info_part += 1
				self.delay_timer.reset()
				
		buttons = [i for i in logic.joysticks if i and 7 in i.activeButtons]
		
		if len(buttons):
			self.info_text.setVisible(False)
			self.press_start.setVisible(False)
			logic.getCurrentController().activate(self.actuators[0])
				
		
		
		

		
def init(cont):
	Tutorial(cont.owner)
	
def main(cont):
	cont.owner.main()