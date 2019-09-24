from math import sin,cos,pi,sqrt
from mcpi import minecraft
try:
	mc = minecraft.Minecraft.create()
except:
	print "please open minecraft first"
	exit()



pos = mc.player.getPos()
pos.x = int(pos.x)
pos.y = int(pos.y)
pos.z = int(pos.z)

class sphere:
	def __init__(x,y,z,r):
		self.x = x
		self.y = y
		self.z = z
		self.radius = r
	def fill(quality):
        	for mi in range(90*quality, 180*quality, 1):
                	i=mi/quality
                	x_pos = cos((i*pi)/180)
                	x_pos = x_pos*self.r
                	x_pos += self.x

                	y_pos = sin((i*pi)/180)
                	y_pos = y_pos*self.r
                	y_pos += self.y
                	for mj in range(0, 720, quality):
                	        j = mj/2
                        	width = sqrt(self.r**2 - (y_pos - pos.y)**2)
                        	x_pos = cos((j*pi)/180)
                        	x_pos = x_pos*width
                        	x_pos += self.x

                        	z_pos = sin((j*pi)/180)
                        	z_pos = z_pos*width
                        	z_pos += self.z
                        	mc.setBlock(x_pos, y_pos, z_pos, block)


def sphere():
	quality = int(raw_input("Choose the quality of the sphere"))
	r = int(raw_input("What is the radius of the sphere?"))
	block = int(raw_input("What block do you want to use?"))
	for mi in range(180, 540, quality):
		i=mi/2
		x_pos = cos((i*pi)/180)
		x_pos = x_pos*r
		x_pos += pos.x

		y_pos = sin((i*pi)/180)
		y_pos = y_pos*r
		y_pos += pos.y
		for mj in range(0, 720, quality):
			j = mj/2
			width = sqrt(r**2 - (y_pos - pos.y)**2)
			x_pos = cos((j*pi)/180)
			x_pos = x_pos*width
			x_pos += pos.x

			z_pos = sin((j*pi)/180)
			z_pos = z_pos*width
			z_pos += pos.z
			mc.setBlock(x_pos, y_pos, z_pos, block)


while True:
	print "q: QUIT"
	print "1: SPHERE"
	print "2: SET NEW POS"
	choice = raw_input("...")
	if choice == 'q':
		exit()
	if choice == '1':
		sphere()
	if choice == '2':
		pos = mc.player.getPos()
       		pos.x = int(pos.x)
	        pos.y = int(pos.y)
        	pos.z = int(pos.z)
        print "Setting posistion to ({}, {}, {},)".format(pos.x, pos.y, pos.z)



