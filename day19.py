#!/usr/bin/python

"""
--- Day 19: Tractor Beam ---

Unsure of the state of Santa's ship, you borrowed the tractor beam technology from Triton. Time to test it out.

When you're safely away from anything else, you activate the tractor beam, but nothing happens. It's hard to tell whether it's working if there's nothing to use it on. Fortunately, your ship's drone system can be configured to deploy a drone to specific coordinates and then check whether it's being pulled. There's even an Intcode program (your puzzle input) that gives you access to the drone system.

The program uses two input instructions to request the X and Y position to which the drone should be deployed. Negative numbers are invalid and will confuse the drone; all numbers should be zero or positive.

Then, the program will output whether the drone is stationary (0) or being pulled by something (1). For example, the coordinate X=0, Y=0 is directly in front of the tractor beam emitter, so the drone control program will always report 1 at that location.

To better understand the tractor beam, it is important to get a good picture of the beam itself. For example, suppose you scan the 10x10 grid of points closest to the emitter:

       X
  0->      9
 0#.........
 |.#........
 v..##......
  ...###....
  ....###...
Y .....####.
  ......####
  ......####
  .......###
 9........##

In this example, the number of points affected by the tractor beam in the 10x10 area closest to the emitter is 27.

However, you'll need to scan a larger area to understand the shape of the beam. How many points are affected by the tractor beam in the 50x50 area closest to the emitter? (For each of X and Y, this will be 0 through 49.)

To begin, get your puzzle input.

--- Part Two ---

You aren't sure how large Santa's ship is. You aren't even sure if you'll need to use this thing on Santa's ship, but it doesn't hurt to be prepared. You figure Santa's ship might fit in a 100x100 square.

The beam gets wider as it travels away from the emitter; you'll need to be a minimum distance away to fit a square of that size into the beam fully. (Don't rotate the square; it should be aligned to the same axes as the drone grid.)

For example, suppose you have the following tractor beam readings:

#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########

In this example, the 10x10 square closest to the emitter that fits entirely within the tractor beam has been marked O. Within it, the point closest to the emitter (the only highlighted O) is at X=25, Y=20.

Find the 100x100 square closest to the emitter that fits entirely within the tractor beam; within that square, find the point closest to the emitter. What value do you get if you take that point's X coordinate, multiply it by 10000, then add the point's Y coordinate? (In the example above, this would be 250020.)

Although it hasn't changed, you can still get your puzzle input.

"""

class IntPuterVM:
	
	def __init__(self, memory):
		self.mem = memory
		self.mem += [0] * 5000
		self.last_out = None
		self.prog_in = []
		self.halted = False
		self.blocked = True
		self.ip_state = 0
		self.base = 0

	def buffer_read(self, i):
		self.prog_in.append(i)
		self.blocked = False

	def run(self):
		ip = self.ip_state
		while True:
			A = None
			B = None
			C = None
			d_ip = None
			ip_updated = False
			op = self.mem[ip]
			modes, opcode = str(op)[:-2], int(str(op)[-2:])
			if opcode == 99: # Halt
				self.halted = True
				return
			if opcode == 1: # res = C + B
				d_ip = 4
				if modes == '':
					self.mem[self.mem[ip+3]] = self.mem[self.mem[ip+1]] + self.mem[self.mem[ip+2]]
				else:
					if modes[-1] == '1':
						C = self.mem[ip+1]
					elif modes[-1] == '2':
						C = self.mem[self.base+self.mem[ip+1]]
					elif modes[-1] == '0':
						C = self.mem[self.mem[ip+1]]
					modes = modes[:-1]
					if modes == '':
						modes = '0'
					if modes[-1] == '1':
						B = self.mem[ip+2]
					elif modes[-1] == '2':
						B = self.mem[self.base+self.mem[ip+2]]
					elif modes[-1] == '0':
						B = self.mem[self.mem[ip+2]]
					modes = modes[:-1]
					if modes == '' or modes[-1] == '0':
						self.mem[self.mem[ip+3]] = C + B
					elif modes == '2':
						self.mem[self.base+self.mem[ip+3]] = C + B
			elif opcode == 2: # res = C * B
				d_ip = 4
				if modes == '':
					self.mem[self.mem[ip+3]] = self.mem[self.mem[ip+1]] * self.mem[self.mem[ip+2]]
				else:
					if modes[-1] == '1':
						C = self.mem[ip+1]
					elif modes[-1] == '2':
						C = self.mem[self.base+self.mem[ip+1]]
					elif modes[-1] == '0':
						C = self.mem[self.mem[ip+1]]
					modes = modes[:-1]
					if modes == '':
						modes = '0'
					if modes[-1] == '1':
						B = self.mem[ip+2]
					elif modes[-1] == '2':
						B = self.mem[self.base+self.mem[ip+2]]
					elif modes[-1] == '0':
						B = self.mem[self.mem[ip+2]]
					modes = modes[:-1]
					if modes == '' or modes[-1] == '0':
						self.mem[self.mem[ip+3]] = C * B
					elif modes[-1] == '2':
						self.mem[self.base+self.mem[ip+3]] = C * B
			elif opcode == 3: # Store input at param 1
				d_ip = 2
				if len(self.prog_in) == 0:
					self.blocked = True
					self.ip_state = ip
					return
				if modes == '' or modes == '0':
					self.mem[self.mem[ip+1]] = self.prog_in.pop(0)
				elif modes == '1':
					self.mem[ip+1] = self.prog_in.pop(0)
				elif modes == '2':
					self.mem[self.base+self.mem[ip+1]] = self.prog_in.pop(0)
			elif opcode == 4: # Output value at param 1
				d_ip = 2
				if modes == '' or modes == '0':
					self.last_out = self.mem[self.mem[ip+1]]
				elif modes == '1':
					self.last_out = self.mem[ip+1]
				elif modes == '2':
					self.last_out = self.mem[self.base+self.mem[ip+1]]
				yield self.last_out
			elif opcode == 5: # Jump if True (non-zero)
				d_ip = 3
				if modes == '':
					if self.mem[self.mem[ip+1]] != 0:
						ip = self.mem[self.mem[ip+2]]
						ip_updated = True
				else:
					if modes[-1] == '1':
						C = self.mem[ip+1]
					elif modes[-1] == '0':
						C = self.mem[self.mem[ip+1]]
					elif modes[-1] == '2':
						C = self.mem[self.base+self.mem[ip+1]]
					modes = modes[:-1]
					if modes == '':
						modes = '0'
					if modes[-1] == '1':
						B = self.mem[ip+2]
					elif modes[-1] == '0':
						B = self.mem[self.mem[ip+2]]
					elif modes[-1] == '2':
						B = self.mem[self.base+self.mem[ip+2]]
					modes = modes[:-1]
					if C != 0:
						ip = B
						ip_updated = True
			elif opcode == 6: # Jump if False (zero)
				d_ip = 3
				if modes == '':
					if self.mem[self.mem[ip+1]] == 0:
						ip = self.mem[self.mem[ip+2]]
						ip_updated = True
				else:
					if modes[-1] == '1':
						C = self.mem[ip+1]
					elif modes[-1] == '0':
						C = self.mem[self.mem[ip+1]]
					elif modes[-1] == '2':
						C = self.mem[self.base+self.mem[ip+1]]
					modes = modes[:-1]
					if modes == '':
						modes = '0'
					if modes[-1] == '1':
						B = self.mem[ip+2]
					elif modes[-1] == '0':
						B = self.mem[self.mem[ip+2]]
					elif modes[-1] == '2':
						B = self.mem[self.base+self.mem[ip+2]]
					modes = modes[:-1]
					if C == 0:
						ip = B
						ip_updated = True
			elif opcode == 7: # res = C < B
				d_ip = 4
				if modes == '':
					if self.mem[self.mem[ip+1]] < self.mem[self.mem[ip+2]]:
						self.mem[self.mem[ip+3]] = 1
					else:
						self.mem[self.mem[ip+3]] = 0
				else:
					if modes[-1] == '1':
						C = self.mem[ip+1]
					elif modes[-1] == '0':
						C = self.mem[self.mem[ip+1]]
					elif modes[-1] == '2':
						C = self.mem[self.base+self.mem[ip+1]]
					modes = modes[:-1]
					if modes == '':
						modes = '0'
					if modes[-1] == '1':
						B = self.mem[ip+2]
					elif modes[-1] == '0':
						B = self.mem[self.mem[ip+2]]
					elif modes[-1] == '2':
						B = self.mem[self.base+self.mem[ip+2]]
					modes = modes[:-1]
					if C < B:
						if modes == '' or modes[-1] == '0':
							self.mem[self.mem[ip+3]] = 1
						elif modes[-1] == '2':
							self.mem[self.base+self.mem[ip+3]] = 1
					else:
						if modes == '' or modes[-1] == '0':
							self.mem[self.mem[ip+3]] = 0
						elif modes[-1] == '2':
							self.mem[self.base+self.mem[ip+3]] = 0
			elif opcode == 8: # res = C == B
				d_ip = 4
				if modes == '':
					if self.mem[self.mem[ip+1]] == self.mem[self.mem[ip+2]]:
						self.mem[self.mem[ip+3]] = 1
					else:
						self.mem[self.mem[ip+3]] = 0
				else:
					if modes[-1] == '1':
						C = self.mem[ip+1]
					elif modes[-1] == '0':
						C = self.mem[self.mem[ip+1]]
					elif modes[-1] == '2':
						C = self.mem[self.base+self.mem[ip+1]]
					modes = modes[:-1]
					if modes == '':
						modes = '0'
					if modes[-1] == '1':
						B = self.mem[ip+2]
					elif modes[-1] == '0':
						B = self.mem[self.mem[ip+2]]
					elif modes[-1] == '2':
						B = self.mem[self.base+self.mem[ip+2]]
					modes = modes[:-1]
					if C == B:
						if modes == '' or modes[-1] == '0':
							self.mem[self.mem[ip+3]] = 1
						elif modes[-1] == '2':
							self.mem[self.base+self.mem[ip+3]] = 1
					else:
						if modes == '' or modes[-1] == '0':
							self.mem[self.mem[ip+3]] = 0
						elif modes[-1] == '2':
							self.mem[self.base+self.mem[ip+3]] = 0
			elif opcode == 9: # adjust base pointer by param
				d_ip = 2
				if modes == '':
					self.base += self.mem[self.mem[ip+1]]
				else:
					if modes[-1] == '1':
						self.base += self.mem[ip+1]
					elif modes[-1] == '0':
						self.base += self.mem[self.mem[ip+1]]
					elif modes[-1] == '2':
						self.base += self.mem[self.base+self.mem[ip+1]]
			if not ip_updated:
				ip += d_ip

def check(x,y,prog):
	vm = IntPuterVM(prog[:])
	vm.buffer_read(x)
	vm.buffer_read(y)	
	for out in vm.run():
		return out

if __name__ == "__main__":

	# Part 1 Solution
	space = dict()
	with open("day19_input", 'r') as infile:
		prog = [ int(x) for x in infile.readline().strip().split(',') ]
	vm = IntPuterVM(prog[:])
	for x in range(50):
		for y in range(50):
			vm = IntPuterVM(prog[:])
			vm.buffer_read(x)
			vm.buffer_read(y)
			for out in vm.run():
				space[(x,y)] = out
	print(list(space.values()).count(1))

	# Part 2 Solution
	x = 0
	y = 0
	while check(x+99,y,prog) != 1:
		y += 1
		while check(x,y+99,prog) != 1:
			x += 1
	print(10000*x+y)		
