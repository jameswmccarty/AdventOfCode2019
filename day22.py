#!/usr/bin/python

"""
--- Day 22: Slam Shuffle ---

There isn't much to do while you wait for the droids to repair your ship. At least you're drifting in the right direction. You decide to practice a new card shuffle you've been working on.

Digging through the ship's storage, you find a deck of space cards! Just like any deck of space cards, there are 10007 cards in the deck numbered 0 through 10006. The deck must be new - they're still in factory order, with 0 on the top, then 1, then 2, and so on, all the way through to 10006 on the bottom.

You've been practicing three different techniques that you use while shuffling. Suppose you have a deck of only 10 cards (numbered 0 through 9):

To deal into new stack, create a new stack of cards by dealing the top card of the deck onto the top of the new stack repeatedly until you run out of cards:

Top          Bottom
0 1 2 3 4 5 6 7 8 9   Your deck
                      New stack

  1 2 3 4 5 6 7 8 9   Your deck
                  0   New stack

    2 3 4 5 6 7 8 9   Your deck
                1 0   New stack

      3 4 5 6 7 8 9   Your deck
              2 1 0   New stack

Several steps later...

                  9   Your deck
  8 7 6 5 4 3 2 1 0   New stack

                      Your deck
9 8 7 6 5 4 3 2 1 0   New stack

Finally, pick up the new stack you've just created and use it as the deck for the next technique.

To cut N cards, take the top N cards off the top of the deck and move them as a single unit to the bottom of the deck, retaining their order. For example, to cut 3:

Top          Bottom
0 1 2 3 4 5 6 7 8 9   Your deck

      3 4 5 6 7 8 9   Your deck
0 1 2                 Cut cards

3 4 5 6 7 8 9         Your deck
              0 1 2   Cut cards

3 4 5 6 7 8 9 0 1 2   Your deck

You've also been getting pretty good at a version of this technique where N is negative! In that case, cut (the absolute value of) N cards from the bottom of the deck onto the top. For example, to cut -4:

Top          Bottom
0 1 2 3 4 5 6 7 8 9   Your deck

0 1 2 3 4 5           Your deck
            6 7 8 9   Cut cards

        0 1 2 3 4 5   Your deck
6 7 8 9               Cut cards

6 7 8 9 0 1 2 3 4 5   Your deck

To deal with increment N, start by clearing enough space on your table to lay out all of the cards individually in a long line. Deal the top card into the leftmost position. Then, move N positions to the right and deal the next card there. If you would move into a position past the end of the space on your table, wrap around and keep counting from the leftmost card again. Continue this process until you run out of cards.

For example, to deal with increment 3:


0 1 2 3 4 5 6 7 8 9   Your deck
. . . . . . . . . .   Space on table
^                     Current position

Deal the top card to the current position:

  1 2 3 4 5 6 7 8 9   Your deck
0 . . . . . . . . .   Space on table
^                     Current position

Move the current position right 3:

  1 2 3 4 5 6 7 8 9   Your deck
0 . . . . . . . . .   Space on table
      ^               Current position

Deal the top card:

    2 3 4 5 6 7 8 9   Your deck
0 . . 1 . . . . . .   Space on table
      ^               Current position

Move right 3 and deal:

      3 4 5 6 7 8 9   Your deck
0 . . 1 . . 2 . . .   Space on table
            ^         Current position

Move right 3 and deal:

        4 5 6 7 8 9   Your deck
0 . . 1 . . 2 . . 3   Space on table
                  ^   Current position

Move right 3, wrapping around, and deal:

          5 6 7 8 9   Your deck
0 . 4 1 . . 2 . . 3   Space on table
    ^                 Current position

And so on:

0 7 4 1 8 5 2 9 6 3   Space on table

Positions on the table which already contain cards are still counted; they're not skipped. Of course, this technique is carefully designed so it will never put two cards in the same position or leave a position empty.

Finally, collect the cards on the table so that the leftmost card ends up at the top of your deck, the card to its right ends up just below the top card, and so on, until the rightmost card ends up at the bottom of the deck.

The complete shuffle process (your puzzle input) consists of applying many of these techniques. Here are some examples that combine techniques; they all start with a factory order deck of 10 cards:

deal with increment 7
deal into new stack
deal into new stack
Result: 0 3 6 9 2 5 8 1 4 7

cut 6
deal with increment 7
deal into new stack
Result: 3 0 7 4 1 8 5 2 9 6

deal with increment 7
deal with increment 9
cut -2
Result: 6 3 0 7 4 1 8 5 2 9

deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
Result: 9 2 5 8 1 4 7 0 3 6

Positions within the deck count from 0 at the top, then 1 for the card immediately below the top card, and so on to the bottom. (That is, cards start in the position matching their number.)

After shuffling your factory order deck of 10007 cards, what is the position of card 2019?

--- Part Two ---

After a while, you realize your shuffling skill won't improve much more with merely a single deck of cards. You ask every 3D printer on the ship to make you some more cards while you check on the ship repairs. While reviewing the work the droids have finished so far, you think you see Halley's Comet fly past!

When you get back, you discover that the 3D printers have combined their power to create for you a single, giant, brand new, factory order deck of 119315717514047 space cards.

Finally, a deck of cards worthy of shuffling!

You decide to apply your complete shuffle process (your puzzle input) to the deck 101741582076661 times in a row.

You'll need to be careful, though - one wrong move with this many cards and you might overflow your entire ship!

After shuffling your new, giant, factory order deck that many times, what number is on the card that ends up in position 2020?

Although it hasn't changed, you can still get your puzzle input.

"""

deck = None
decksize = None

def cut(N):
	global deck
	deck = deck[N:] + deck[:N]

def deal(N):
	global deck
	new = [ None ] * len(deck)
	idx = 0
	while len(deck) > 0:
		new[idx%len(new)] = deck.pop(0)
		idx += N
	deck = new

def new_stack():
	global deck
	deck.reverse()

def parse_line(line):
	line = line.split(' ')
	if line[0] == 'cut':
		cut(int(line[-1]))
	elif line[0] == 'deal' and line[-1] == 'stack':
		new_stack()
	elif line[0] == 'deal':
		deal(int(line[-1]))
	else:
		print("Error:", line)
		exit()

def cut_2(i, N):
	global decksize
	#return ((decksize-N)+i) % decksize
	return (N+i) % decksize

def deal_2(i, N):
	global decksize
	return (i*N) % decksize

def new_stack_2(i):
	global decksize
	return (decksize - i - 1) % decksize

def parse_line_2(line, i):
	line = line.split(' ')
	if line[0] == 'cut':
		i = cut_2(i, int(line[-1]))
	elif line[0] == 'deal' and line[-1] == 'stack':
		i = new_stack_2(i)
	elif line[0] == 'deal':
		i = deal_2(i, int(line[-1]))
	else:
		print("Error:", line)
		exit()
	return i

def unshuffle(n):
	return ((n - 2) * 6871724559536 + 140568611385) % 119315717514047

"""
Next function borrowed:
https://github.com/metalim/metalim.adventofcode.2019.python/blob/master/22_cards_shuffle.ipynb
"""
# modpow the polynomial: (ax+b)^m % n
# f(x) = ax+b
# g(x) = cx+d
# f^2(x) = a(ax+b)+b = aax + ab+b
# f(g(x)) = a(cx+d)+b = acx + ad+b
def polypow(a,b,m,n):
    if m==0:
        return 1,0
    if m%2==0:
        return polypow(a*a%n, (a*b+b)%n, m//2, n)
    else:
        c,d = polypow(a,b,m-1,n)
        return a*c%n, (a*d+b)%n

def shuffle2(L, N, a, b, pos):
    a,b = polypow(a,b,N,L)
    return (pos*a+b)%L

def parse3(L, rules):
    a,b = 1,0
    for s in rules[::-1]:
        if s == 'deal into new stack':
            a = -a
            b = L-b-1
            continue
        if s.startswith('cut'):
            n = int(s.split(' ')[1])
            b = (b+n)%L
            continue
        if s.startswith('deal with increment'):
            n = int(s.split(' ')[3])
            z = pow(n,L-2,L) # == modinv(n,L)
            a = a*z % L
            b = b*z % L
            continue
        raise Exception('unknown rule', s)
    return a,b

if __name__ == "__main__":

	# Part 1 Solution

	deck = [ i for i in range(10007) ]
	with open("day22_input", 'r') as infile:
		for line in infile.readlines():
			parse_line(line.strip())
	print(deck.index(2019))


	place = 2019
	decksize = 10007
	with open("day22_input", 'r') as infile:
		for line in infile.readlines():
			place = parse_line_2(line.strip(), place)
	print(place)


	# Part 2 Solution

	big_size = 119315717514047
	num_shuffle = 101741582076661
	shuff_seq = []
	place = 0
	decksize = big_size
	with open("day22_input", 'r') as infile:
		for line in infile.readlines():
			shuff_seq.append(line.strip())
	shuff_seq.reverse()
	for z in range(250):
		place = z
		for step in shuff_seq:
			place = parse_line_2(step, place)
		print(z, place)

	"""


	# Place				Delta		Difference
	# 0	105712837006360		
	# 1	112584561565896		
	# 2	140568611385		
	# 3	7012293170921	6871724559536	140568611385
	# 4	13884017730457	6871724559536	

	# Linear sequence: P1 = ((P0 - 2) * 6871724559536 + 140568611385) % 119315717514047

	"""
	"""
	big_size = 119315717514047
	num_shuffle = 101741582076661
	print(shuffle2(big_size,num_shuffle,78329155583898,41150195162392,2020))
	"""
	


