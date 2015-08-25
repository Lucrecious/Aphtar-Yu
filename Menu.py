import nilutils as nl
from bge import logic

class Menu (nl.Component):
	
	def __init__(self):
		self.buttons = []
		objects = logic.getCurrentScene().objects
		
		self.text = objects['Text']
		self.menu_empty = objects['Empty']
		self.joys = [j for j in logic.joysticks if j]
		
		
		
		self.state("check_for_joys")
	def check_for_joys (self):
		
		connected = len(self.joys)
		
		if connected < 2:
			self.text['Text'] = "There is only "+str(connected)+" joystick connected.\n " +\
			"Exit. Connect. Reopen game!"
		else:
			self.text["Text"] = "A to start game"
			self.state("start_game")
			
	def start_game(self):
		for b in self.joys:
			if 0 in b.activeButtons: #pressed A?
				scene_switch = self.menu_empty.actuators[0]
				cont = logic.getCurrentController()
				cont.activate(scene_switch)
 
	
			
	
		
	


	
menu = Menu()
def main(cont):
	menu.main()
