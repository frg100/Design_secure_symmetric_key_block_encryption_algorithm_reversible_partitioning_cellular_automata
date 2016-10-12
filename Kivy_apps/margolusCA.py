import kivy
#kivy.require('1.9.0')

from kivy.config import Config

Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '500')

__version__ = "1"

import random
#import block_ca
#import numpy as np


from kivy.clock import Clock
from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.core.window import Window
from kivy.base import EventLoop
from kivy.metrics import sp
from kivy.core.audio import SoundLoader




##############VARIABLES##############
##############VARIABLES##############


Builder.load_string("""

<Menu>:
    id: menu
    name: 'menu_screen'
    BoxLayout:
        id: box_layout
        orientation: 'vertical'
        Label:
            id: label1
            text: "Margolus Block Cellular Automata:"
        Label:
            id: label1
            text: "Developed by Federico Reyes"
        Button:
            id: start
            text: "START"
            on_press: root.change_screen()



<ParameterScreen>
	id: parameter_screen
	name: 'parameter_screen'
	BoxLayout:
        id: box_layout
        orientation: 'vertical'
        TextInput:
            id: generations
            hint_text: 'Enter generations:'
        TextInput:
            id: size
            hint_text: 'Enter size:'
	    Button:
	    	name: critters
            id: critters
            text: "Critters Rule"
            on_release: root.critters()
        Button:
	    	name: bbm
            id: bbm
            text: "Billiard Ball Model"
            on_release: root.bbm()
        Button:
	    	name: tron
            id: tron
            text: "Tron Rule"
            on_release: root.tron()
        Button:
	    	name: sand
            id: sand
            text: "Sand Rule"
            on_release: root.sand()
        BoxLayout:
        	id: rule_list
        	orientation: 'horizontal'
    		TextInput:
	            id: rule_0
	            hint_text: '0'
	        TextInput:
	            id: rule_1
	            hint_text: '1'
	        TextInput:
	            id: rule_2
	            hint_text: '2'
	        TextInput:
	            id: rule_3
	            hint_text: '3'
	        TextInput:
	            id: rule_4
	            hint_text: '4'
	        TextInput:
	            id: rule_5
	            hint_text: '5'
	        TextInput:
	            id: rule_6
	            hint_text: '6'
	        TextInput:
	            id: rule_7
	            hint_text: '7'
	        TextInput:
	            id: rule_8
	            hint_text: '8'
	        TextInput:
	            id: rule_9
	            hint_text: '9'
	        TextInput:
	            id: rule_10
	            hint_text: '10'
	        TextInput:
	            id: rule_11
	            hint_text: '11'
	        TextInput:
	            id: rule_12
	            hint_text: '12'
	        TextInput:
	            id: rule_13
	            hint_text: '13'
	        TextInput:
	            id: rule_14
	            hint_text: '14'
	        TextInput:
	            id: rule_15
	            hint_text: '15'
	    Button:
	    	name: start
            id: start
            text: "start"
            on_release: root.start()



<DishScreen>:
    name: 'dish_screen'
    id: dish_screen
    GridLayout:
        id: grid_layout
        name: grid_layout
        cols: 4
        rows: 4
        size_hint: (1,.95)
    BoxLayout:
        id: box_layout
        name: box_layout
        orientation: 'horizontal'
        size_hint: (1,.05)
        Button:
            name: run
            id: run
            text: "Advance to next generation ->"
            on_release: root.step()
        Button:
            name: start
            id: start
            text: "start"
            on_release: root.run()
        Button:
            name: end
            id: end
            text: "end"
            on_release: root.end()
        Button:
            name: restart
            id: restart
            text: "restart"
            on_release: root.restart()
        Button:
            name: quit
            id: quit
            text: "Quit"
            on_release: exit()
	""")

class Menu(Screen): 
	global sm

	def change_screen(self,*args):
		global sm
		parameter_screen = ParameterScreen()
		sm.add_widget( parameter_screen )
		sm.current = 'parameter_screen' #changes the screen to game_screen instance


class ParameterScreen(Screen):
	global sm

	def start(self):
		rule_list = [ int(self.ids.rule_0.text), int(self.ids.rule_1.text),int(self.ids.rule_2.text),int(self.ids.rule_3.text),int(self.ids.rule_4.text),int(self.ids.rule_5.text),int(self.ids.rule_6.text),int(self.ids.rule_7.text),int(self.ids.rule_8.text),int(self.ids.rule_9.text),int(self.ids.rule_10.text),int(self.ids.rule_11.text),int(self.ids.rule_12.text),int(self.ids.rule_13.text),int(self.ids.rule_14.text),int(self.ids.rule_15.text)]
		generations = int( self.ids.generations.text)
		dish_screen = DishScreen()
		sm.add_widget(dish_screen)
		sm.current = 'dish_screen' #changes the screen to game_screen instance

	def critters(self):
		rule_list = [15,14,13,3,11,5,6,1,7,9,10,2,12,4,8,0]
		generations = int( self.ids.generations.text)
		dish_screen = DishScreen()
		sm.add_widget(dish_screen)
		sm.current = 'dish_screen' #changes the screen to game_screen instance

	def bbm(self):
		rule_list = [0,8,4,3,2,5,9,7,1,6,10,11,12,13,14,15]
		generations = int( self.ids.generations.text)
		dish_screen = DishScreen()
		sm.add_widget(dish_screen)
		sm.current = 'dish_screen' #changes the screen to game_screen instance

	def tron(self):
		rule_list = [15,1,2,3,4,5,6,7,8,9,10,11,12,13,14,0]
		generations = int( self.ids.generations.text)
		dish_screen = DishScreen()
		sm.add_widget(dish_screen)
		sm.current = 'dish_screen' #changes the screen to game_screen instance

	def sand(self):
		rule_list = [0,4,8,12,4,12,12,13,8,12,12,14,12,13,14,15]
		generations = int( self.ids.generations.text)
		dish_screen = DishScreen()
		sm.add_widget(dish_screen)
		sm.current = 'dish_screen' #changes the screen to game_screen instance
		
class DishScreen(Screen):
	global sm,parameter_screen, generations, rule_list

	def step(self):
		size = int(parameter_screen.ids.size.text)
        table = np.zeros( (size,size), dtype=np.int )
        for child in self.ids.grid_layout.children:
            coords = child.id.split(',')
            x = int(coords[0])
            y = int(coords[1])
            if child.state == 'down':
                table[x][y] = 1
            elif child.state == 'normal':
                table[x][y] == 0
        table = block_ca.block_ca.forward_evolution(1, rule_list, table)
        for child in ms.ids.grid_layout.children:
            coords = child.id.split(',')
            x = int(coords[0])
            y = int(coords[1])
            if table[x][y] == 1:
                child.state = 'down' 
            elif table[x][y] == 0:
                child.state = 'normal'


	def run(self):
		global generations
		Clock.schedule_interval(self.step, float(generations))
	
	def end(self):
		Clock.unschedule(self.step)

	def restart(self):
		sm.remove_widget(parameter_screen)
		parameter_screen = ParameterScreen()
		sm.add_widget(parameter_screen)
		sm.current = 'parameter_screen' #changes the screen to game_screen instance


class MargolusCAApp(App):
	global sm

	def build(self):
		global sm,game_screen,score_screen
		sm = ScreenManager() #initializes a new screenmanager instance
		menu = Menu() #initializes a new menu instance
		sm.add_widget(menu) #adds the menu instance to the screenmanager instance
		return sm #returns the screenmanager to start the app





if __name__=='__main__':
	MargolusCAApp().run()
