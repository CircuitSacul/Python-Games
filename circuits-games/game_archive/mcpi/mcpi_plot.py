from mcpi import minecraft
from math import cos,sin
mc = minecraft.Minecraft.create()


mc.player.setPos(0, 60, 5)
for i in range(-100, 100):
	mc.setBlock(i, (cos(i)*5)+60, 0, 1)
	mc.setBlock(i, (sin(i)*5)+60, 1, 3)
