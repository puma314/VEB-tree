import os, sys

class VEB:
	
	def __init__(self, n, firstCall = True): 
		if firstCall: 
			power = 0
			while (1 << (1 << power)) < n: 
				power += 1
		else: 
			power = n

		self.usize = 1 << (1 << power)
		self.min = self.usize
		self.max = -1

		if self.usize != 2:
			self.power = power
			self.numbits = 1 << (power-1)
			self.aux = None
			self.children = {}
		#else:
		#	self.a = 0
		#	self.b = 0

	def isEmpty(self):
		return self.min > self.max

	def insert(self, key):
		if self.usize == 2:
			res = (key != self.min and key != self.max)
		else:
			block = key >> self.numbits
			if self.aux is None:
				if self.power > 4:
					self.aux = VEB(self.power-1, False)
				else:
					self.aux = BitVEB(self.power-1)
			self.aux.insert(block)
			if block not in self.children:
				if self.power > 4: # only make real VEB for big trees
					self.children[block] = VEB(self.power-1, False)
				else:
					self.children[block] = BitVEB(self.power-1)

			res = self.children[block].insert(key & ((1 << self.numbits) - 1))

		self.min = min(self.min, key)
		self.max = max(self.max, key)
		return res # return whether a new element was added

	def next(self, key):
		if self.isEmpty() or key >= self.max:
			return None
		if key < self.min:
			return self.min
		if self.usize == 2:
			return self.max # key should be self.min so next is max

		block = key >> self.numbits
		pos = key & ((1<< self.numbits) - 1)

		if block in self.children:
			if pos < self.children[block].max:
				return key - pos + self.children[block].next(pos) #otherwise nextBlock needed

		nextBlock = self.aux.next(block) #nextBlock should exist
		return key - pos + self.children[nextBlock].min + ((nextBlock - block)  << self.numbits)

	def delete(self, key):
		if self.isEmpty():
			return
		
		if self.usize == 2:
			if self.min == key and self.max == key:
				self.min = self.usize
				self.max = -1
			elif self.min == key:
				self.min = self.max
			elif self.max == key:
				self.max = self.min
			return

		block = key >> self.numbits
		if block not in self.children:
			return #block doesn't exist, so no continuing

		self.children[block].delete(key & ((1<<self.numbits) - 1))

		if self.children[block].isEmpty():
			del self.children[block]
			self.aux.delete(block)

		if self.min == key and self.max == key:
			self.min = self.usize
			self.max = -1
		elif self.min == key:
			self.min = (self.aux.min  << self.numbits) + self.children[self.aux.min].min
		elif self.max == key:
			self.max = (self.aux.max << self.numbits) + self.children[self.aux.max].max
	
	def __str__(self):
		if self.usize == 2:
			return str((self.min, self.max))
		
		s = str((self.usize, self.min, self.max)) + "\nchildren"
		for i in self.children:
			s += str(i)
		return s

class BitVEB(VEB):
	def __init__(self, power):
		self.usize = 1 << (1 << power)
		self.min = self.usize
		self.max = -1
		self.bits = 0

	def isEmpty(self):
		return self.bits == 0

	def insert(self, key):
		if ((self.bits >> key) & 1) == 0:
			self.bits |= (1 << key)
			self.min = min(self.min, key)
			self.max = max(self.max, key)
			return True
		return False

	def next(self, key):
		if self.isEmpty() or key >= self.max:
			return None
		for i in xrange(key+1, self.max+1):
			if ((self.bits >> i) & 1) == 1:
				return i
	def prev(self, key):
		if self.isEmpty() or key <= self.min:
			return None
		for i in xrange(key-1, self.min-1, -1):
			if ((self.bits >> i) & 1) == 1:
				return i
	
	def delete(self, key):
		if ((self.bits >> key) & 1) == 1:
			self.bits ^= (1 << key)
			if key == self.min and key == self.max:
				self.min = self.usize
				self.max = -1
			elif key == self.min:
				self.min = self.next(key)
			elif key == self.max:
				self.max = self.prev(key)

	def __str__(self):
		return str(self.bits)

if __name__ == "__main__":
	a = VEB(1000)
	a.insert(5)
	a.insert(7)
	a.insert(120)
	a.insert(88)
	#list: 5, 7, 88, 120
	assert(a.next(80) == 88)
	assert(a.next(110) == 120)
	assert(a.next(120) == None)
	assert(a.next(3) == 5)
	a.delete(88) # list: 5, 7, 120
	assert(a.next(80) == 120)
	a.delete(119)
	assert(a.next(110) == 120)
