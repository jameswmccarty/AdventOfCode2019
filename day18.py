#!/usr/bin/python

import heapq

"""
--- Day 18: Many-Worlds Interpretation ---

As you approach Neptune, a planetary security system detects you and activates a giant tractor beam on Triton! You have no choice but to land.

A scan of the local area reveals only one interesting feature: a massive underground vault. You generate a map of the tunnels (your puzzle input). The tunnels are too narrow to move diagonally.

Only one entrance (marked @) is present among the open passages (marked .) and stone walls (#), but you also detect an assortment of keys (shown as lowercase letters) and doors (shown as uppercase letters). Keys of a given letter open the door of the same letter: a opens A, b opens B, and so on. You aren't sure which key you need to disable the tractor beam, so you'll need to collect all of them.

For example, suppose you have the following map:

#########
#b.A.@.a#
#########

Starting from the entrance (@), you can only access a large door (A) and a key (a). Moving toward the door doesn't help you, but you can move 2 steps to collect the key, unlocking A in the process:

#########
#b.....@#
#########

Then, you can move 6 steps to collect the only other key, b:

#########
#@......#
#########

So, collecting every key took a total of 8 steps.

Here is a larger example:

########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################

The only reasonable move is to take key a and unlock door A:

########################
#f.D.E.e.C.b.....@.B.c.#
######################.#
#d.....................#
########################

Then, do the same with key b:

########################
#f.D.E.e.C.@.........c.#
######################.#
#d.....................#
########################

...and the same with key c:

########################
#f.D.E.e.............@.#
######################.#
#d.....................#
########################

Now, you have a choice between keys d and e. While key e is closer, collecting it now would be slower in the long run than collecting key d first, so that's the best choice:

########################
#f...E.e...............#
######################.#
#@.....................#
########################

Finally, collect key e to unlock door E, then collect key f, taking a grand total of 86 steps.

Here are a few more examples:

    ########################
    #...............b.C.D.f#
    #.######################
    #.....@.a.B.c.d.A.e.F.g#
    ########################

    Shortest path is 132 steps: b, a, c, d, f, e, g

    #################
    #i.G..c...e..H.p#
    ########.########
    #j.A..b...f..D.o#
    ########@########
    #k.E..a...g..B.n#
    ########.########
    #l.F..d...h..C.m#
    #################

    Shortest paths are 136 steps;
    one is: a, f, b, j, g, n, h, d, l, o, e, p, c, i, k, m

    ########################
    #@..............ac.GI.b#
    ###d#e#f################
    ###A#B#C################
    ###g#h#i################
    ########################

    Shortest paths are 81 steps; one is: a, c, f, i, d, g, b, e, h

How many steps is the shortest path that collects all of the keys?


"""

world = dict()
key_locs = dict()
door_locs = dict()
start = None

def parse_line(idx, line):
	global start
	for col, char in enumerate(line):
		pos = (idx,col)
		world[pos] = char
		if char >= 'a' and char <= 'z':
			key_locs[char] = pos
		elif char >= 'A' and char <= 'Z':
			door_locs[char] = pos
		elif char == '@':
			start = pos
			world[pos] = '.'

def key_search(start):
	# ( steps, (x,y), {keys} )
	loc    = start
	steps  = 0 # Time spent searching
	keys = ''
	h = []
	heapq.heappush(h, (steps, loc, keys) )
	min_search = float('inf')
	max_x = 0
	max_y = 0
	seen = set()
	seen.add((loc, keys))
	for key in world.keys():
		x, y = key
		max_x = max(x, max_x)
		max_y = max(y, max_y)
	while len(h) > 0 and h[0][0] <= min_search and len(keys) < len(key_locs):
		steps, loc, keys = heapq.heappop(h)
		x, y = loc
		if world[loc] in key_locs.keys() and world[loc] not in keys:
			keys += world[loc]
			keys = ''.join(sorted(keys))
		if len(keys) == len(key_locs):
			min_search = min(min_search, steps)			
		else: # still possible shorter path
			next_locs = []
			if x > 0:
				next_locs.append((x-1, y))
			if y > 0:
				next_locs.append((x, y-1))
			if x < max_x:
				next_locs.append((x+1, y))
			if y < max_y:
				next_locs.append((x, y+1))
			for next_loc in next_locs:
					t = world[next_loc]
					if (t == '.' or (t.lower() in keys) or (t >= 'a' and t <= 'z')) and ((next_loc, keys) not in seen):
						seen.add((next_loc, keys))
						heapq.heappush(h, ( steps + 1, next_loc, keys ) )
	return min_search

if __name__ == "__main__":

	# Part 1 Solution
	with open('day18_input', 'r') as infile:
		idx = 0
		for line in infile.readlines():
			parse_line(idx, line.strip())
			idx += 1
	"""
	max_x = 0
	max_y = 0
	for key in world.keys():
		x, y = key
		max_x = max(x, max_x)
		max_y = max(y, max_y)
	for x in range(max_x):
		line = ''
		for y in range(max_y):
			line += world[(x,y)]
		print(line)
	"""
	print(key_search(start))







