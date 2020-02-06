#!/usr/bin/python



"""
--- Day 23: Category Six ---

The droids have finished repairing as much of the ship as they can. Their report indicates that this was a Category 6 disaster - not because it was that bad, but because it destroyed the stockpile of Category 6 network cables as well as most of the ship's network infrastructure.

You'll need to rebuild the network from scratch.

The computers on the network are standard Intcode computers that communicate by sending packets to each other. There are 50 of them in total, each running a copy of the same Network Interface Controller (NIC) software (your puzzle input). The computers have network addresses 0 through 49; when each computer boots up, it will request its network address via a single input instruction. Be sure to give each computer a unique network address.

Once a computer has received its network address, it will begin doing work and communicating over the network by sending and receiving packets. All packets contain two values named X and Y. Packets sent to a computer are queued by the recipient and read in the order they are received.

To send a packet to another computer, the NIC will use three output instructions that provide the destination address of the packet followed by its X and Y values. For example, three output instructions that provide the values 10, 20, 30 would send a packet with X=20 and Y=30 to the computer with address 10.

To receive a packet from another computer, the NIC will use an input instruction. If the incoming packet queue is empty, provide -1. Otherwise, provide the X value of the next packet; the computer will then use a second input instruction to receive the Y value for the same packet. Once both values of the packet are read in this way, the packet is removed from the queue.

Note that these input and output instructions never block. Specifically, output instructions do not wait for the sent packet to be received - the computer might send multiple packets before receiving any. Similarly, input instructions do not wait for a packet to arrive - if no packet is waiting, input instructions should receive -1.

Boot up all 50 computers and attach them to your network. What is the Y value of the first packet sent to address 255?

--- Part Two ---

Packets sent to address 255 are handled by a device called a NAT (Not Always Transmitting). The NAT is responsible for managing power consumption of the network by blocking certain packets and watching for idle periods in the computers.

If a packet would be sent to address 255, the NAT receives it instead. The NAT remembers only the last packet it receives; that is, the data in each packet it receives overwrites the NAT's packet memory with the new packet's X and Y values.

The NAT also monitors all computers on the network. If all computers have empty incoming packet queues and are continuously trying to receive packets without sending packets, the network is considered idle.

Once the network is idle, the NAT sends only the last packet it received to address 0; this will cause the computers on the network to resume activity. In this way, the NAT can throttle power consumption of the network when the ship needs power in other areas.

Monitor packets released to the computer at address 0 by the NAT. What is the first Y value delivered by the NAT to the computer at address 0 twice in a row?

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

	def network_read(self, x, y):
		self.buffer_read(x)
		self.buffer_read(y)

	def ascii_read(self, cmd):
		for char in cmd:
			self.buffer_read(ord(char))
		self.buffer_read(10)

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
					#self.blocked = True
					#self.ip_state = ip
					#return
					self.prog_in.append(-1)
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
			self.ip_state = ip
			return

if __name__ == "__main__":

	# Part 1 Solution
	with open("day23_input", 'r') as infile:
		prog = [ int(x) for x in infile.readline().strip().split(',') ]
	num_vms = 50
	vms = []
	netbuf = dict()
	for i in range(num_vms):
		vms.append(IntPuterVM(prog[:]))
		netbuf[i] = list()
	for i in range(num_vms):
		vms[i].buffer_read(i)
	while True:
		for i in range(num_vms):
			for out in vms[i].run():
				netbuf[i].append(out)
			if len(netbuf[i]) == 3:
				dest = netbuf[i][0]
				x    = netbuf[i][1]
				y    = netbuf[i][2]
				netbuf[i] = list()
				if dest == 255:
					print(y)
					exit()
				if dest <= num_vms:
					vms[dest].buffer_read(x)
					vms[dest].buffer_read(y)


			
