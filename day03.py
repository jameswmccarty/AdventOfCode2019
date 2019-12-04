#!/usr/bin/python

"""
--- Day 3: Crossed Wires ---

The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.

Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).

The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for this measurement. While the wires do technically cross right at the central port where they both start, this point does not count, nor does a wire count as crossing with itself.

For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5, left 5, and finally down 3:

...........
...........
...........
....+----+.
....|....|.
....|....|.
....|....|.
.........|.
.o-------+.
...........

Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.

Here are a few more examples:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

What is the Manhattan distance from the central port to the closest intersection?

To begin, get your puzzle input.

--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value from the first time it visits that position when calculating the total value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

What is the fewest combined steps the wires must take to reach an intersection?

Although it hasn't changed, you can still get your puzzle input.

"""

seen_posits = set((0,0))
intersections = set()
timings = dict()

def taxi(coord):
	return abs(coord[0])+abs(coord[1])

def populate(path):
	x = 0
	y = 0
	for step in path:
		way, val = step[0], int(step[1:])
		for i in range(val):
			if way == 'U':
				y += 1
			elif way == 'D':
				y -= 1
			elif way == 'L':
				x -= 1
			elif way == 'R':
				x += 1
			seen_posits.add((x,y))

def trace(path):
	x = 0
	y = 0
	for step in path:
		way, val = step[0], int(step[1:])
		for i in range(val):
			if way == 'U':
				y += 1
			elif way == 'D':
				y -= 1
			elif way == 'L':
				x -= 1
			elif way == 'R':
				x += 1
			if (x,y) in seen_posits:
				intersections.add((x,y))

def delay(path, wire):
	x = 0
	y = 0
	time = 0
	for step in path:
		way, val = step[0], int(step[1:])
		for i in range(val):
			if way == 'U':
				y += 1
			elif way == 'D':
				y -= 1
			elif way == 'L':
				x -= 1
			elif way == 'R':
				x += 1
			time += 1
			if (x,y) in intersections:
				if time < timings[(x,y)][wire]:
					u,v = timings[(x,y)]
					if wire == 0:
						u = time
					else:
						v = time
					timings[(x,y)] = (u,v)

if __name__ == "__main__":
	
	# Part 1 Solution
	with open("day03_input", 'r') as infile:
		populate(infile.readline().strip().split(','))
		trace(infile.readline().strip().split(','))
	print(min([ taxi(x) for x in intersections ]))
	
	# Part 2 Solution
	for posit in intersections:
		timings[posit] = (float('inf'), float('inf'))
	with open("day03_input", 'r') as infile:
		delay(infile.readline().strip().split(','),0)
		delay(infile.readline().strip().split(','),1)
	print(min([ taxi(x) for x in timings.values() ]))


