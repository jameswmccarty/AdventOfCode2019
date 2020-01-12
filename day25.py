#!/usr/bin/python

from itertools import combinations

"""
--- Day 25: Cryostasis ---

As you approach Santa's ship, your sensors report two important details:

First, that you might be too late: the internal temperature is -40 degrees.

Second, that one faint life signature is somewhere on the ship.

The airlock door is locked with a code; your best option is to send in a small droid to investigate the situation. You attach your ship to Santa's, break a small hole in the hull, and let the droid run in before you seal it up again. Before your ship starts freezing, you detach your ship and set it to automatically stay within range of Santa's ship.

This droid can follow basic instructions and report on its surroundings; you can communicate with it through an Intcode program (your puzzle input) running on an ASCII-capable computer.

As the droid moves through its environment, it will describe what it encounters. When it says Command?, you can give it a single instruction terminated with a newline (ASCII code 10). Possible instructions are:

    Movement via north, south, east, or west.
    To take an item the droid sees in the environment, use the command take <name of item>. For example, if the droid reports seeing a red ball, you can pick it up with take red ball.
    To drop an item the droid is carrying, use the command drop <name of item>. For example, if the droid is carrying a green ball, you can drop it with drop green ball.
    To get a list of all of the items the droid is currently carrying, use the command inv (for "inventory").

Extra spaces or other characters aren't allowed - instructions must be provided precisely.

Santa's ship is a Reindeer-class starship; these ships use pressure-sensitive floors to determine the identity of droids and crew members. The standard configuration for these starships is for all droids to weigh exactly the same amount to make them easier to detect. If you need to get past such a sensor, you might be able to reach the correct weight by carrying items from the environment.

Look around the ship and see if you can find the password for the main airlock.

To begin, get your puzzle input.

--- Part Two ---

As you move through the main airlock, the air inside the ship is already heating up to reasonable levels. Santa explains that he didn't notice you coming because he was just taking a quick nap. The ship wasn't frozen; he just had the thermostat set to "North Pole".

You make your way over to the navigation console. It beeps. "Status: Stranded. Please supply measurements from 49 stars to recalibrate."

"49 stars? But the Elves told me you needed fifty--"

Santa just smiles and nods his head toward the window. There, in the distance, you can see the center of the Solar System: the Sun!

The navigation console beeps again.

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

if __name__ == "__main__":

	"""
	# Part 1 Solution (for manual solution)
	with open("day25_input", 'r') as infile:
		prog = [ int(x) for x in infile.readline().strip().split(',') ]
	vm = IntPuterVM(prog[:])
	vm.buffer_read(10)
	for out in vm.run():
		print(chr(out), end='')

	while True:
		print('> ', end='')
		command = input()
		for char in command:
			vm.buffer_read(ord(char))
		vm.buffer_read(10)
		for out in vm.run():
			print(chr(out), end='')
	"""

	# Part 1 Solution
	with open("day25_input", 'r') as infile:
		prog = [ int(x) for x in infile.readline().strip().split(',') ]
	vm = IntPuterVM(prog[:])
	vm.buffer_read(10)
	for out in vm.run():
		continue
		#print(chr(out), end='')

	seq = ['north', 'take dark matter', 'east', 'south', 'take dehydrated water', 'north', 'east', 'take bowl of rice', 'west', 'west', 'north', 'east', 'south', 'take antenna', 'west', 'take hypercube', 'east', 'north', 'west', 'north', 'take manifold', 'west', 'take jam', 'east', 'east', 'take candy cane', 'west', 'south', 'south', 'south', 'west', 'south', 'west'] # manually mapped

	for cmd in seq: # gather all items
		for char in cmd:
			vm.buffer_read(ord(char))
		vm.buffer_read(10)
		for out in vm.run():
			continue
			#print(chr(out), end='')

	items = ['jam', 'bowl of rice', 'antenna', 'manifold', 'hypercube', 'dehydrated water', 'candy cane', 'dark matter'] # all 'safe items'

	for item in items: # drop all items at Arcade room
		cmd = 'drop ' + item
		for char in cmd:
			vm.buffer_read(ord(char))
		vm.buffer_read(10)
		for out in vm.run():
			continue
			#print(chr(out), end='')	

	for i in range(8):
		for combo in list(combinations(items, i)):
			for item in combo:
				cmd = 'take ' + item
				for char in cmd:
					vm.buffer_read(ord(char))
				vm.buffer_read(10)
				for out in vm.run():
					continue
					#print(chr(out), end='')
			for char in 'west':
				vm.buffer_read(ord(char))
			vm.buffer_read(10)
			result = ''
			for out in vm.run():
				result += chr(out)
			if 'Alert' not in result:
				print(result)
				exit()
			for item in combo:
				cmd = 'drop ' + item
				for char in cmd:
					vm.buffer_read(ord(char))
				vm.buffer_read(10)
				for out in vm.run():
					continue
					#print(chr(out), end='')	
