from time import sleep
from math import cos,sin,pi
import random

G = 0.098 #every 1/100 of a second

class tub:
	def __init__(self, s_x, s_y, s_z, e_x, e_y, e_z):
		self.s_pos = {'x':s_x, 'y':s_y, 'z':s_z}
		self.e_pos = {'x':e_x, 'y':e_y, 'z':e_z}
		mc.setBlocks(self.s_pos['x'], self.s_pos['y'], self.s_pos['z'], self.e_pos['x'], self.e_pos['y'], self.e_pos['z'])
		mc.setBlocks(self.s_pos['x']-

