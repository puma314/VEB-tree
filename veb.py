import os, sys

class VEB:
	def __init__(self, power):
		self.usize = 1 << (1 << power)
		self.min = self.usize
		self.max = -1

		if self.usize != 2:
			# block size is square root of universe size
			self.bsize = 1 << (1 << (power - 1))
			self.aux = VEB(power-1)
			self.children = [VEB(power-1) for i in xrange(self.bsize)]
		#else:
		#	self.a = 0
		#	self.b = 0
	
	def isEmpty(self): 
		return self.min > self.max

	def insert(self, key):
		if self.usize == 2:
			res = (key != self.min and key != self.max)
		else:
			block = key // self.bsize
			self.aux.insert(block)
			res = self.children[block].insert(key % self.bsize)

		self.min = min(self.min, key) 
		self.max = max(self.max, key)
		return res # return whether a new element was added

	def next(self, key):
		if self.usize == 2:
			return self.max # key should be self.min so next is max

		if key < self.min:
			return self.min
		if key >= self.max:
			return None
		block = key//self.bsize
		pos = key % self.bsize
		if pos < self.children[block].max:
			return key - pos + self.children[block].next(pos)
		nextBlock = self.aux.next(block)
		return key - pos + self.children[nextBlock].min + (nextBlock - block) * self.bsize

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
		
		block = key//self.bsize
		self.children[block].delete(key % self.bsize)

		if self.children[block].isEmpty(): 
			self.aux.delete(block)
		
		if self.min == key and self.max == key: 
			self.min = self.usize
			self.max = -1
		elif self.min == key:
			self.min = self.aux.min * self.bsize + self.children[self.aux.min].min
		elif self.max == key:
			self.max = self.aux.max * self.bsize + self.children[self.aux.max].max
	
	def __str__(self):
		if self.usize == 2: 
			return str((self.min, self.max))
		
		s = str((self.usize, self.min, self.max)) + "\nchildren"
		for i in self.children: 
			s += str(i) 
		return s

a = VEB(4)
a.insert(5)
a.insert(7)
a.insert(120)
a.insert(88)
print a.next(80)
print a.next(110)
print a.next(120)
print a.next(3)
a.delete(88)
print a.next(80)
a.delete(119)
print a.next(110)
