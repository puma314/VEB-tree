def createVEB(usize):
	exp = 1
	while (1 << exp) < usize:
		exp <<= 1
	if exp > 8:
		return VEB(exp)
	else:
		return BitVEB(exp)

class VEB:
	def __init__(self, exp):
		self.usize = 1 << exp
		self.min = self.usize
		self.max = -1

		self.numbits = exp >> 1
		self.aux = None
		self.children = {}
		#else:
		#	self.a = 0
		#	self.b = 0

	def isEmpty(self):
		return self.min > self.max

	def insert(self, key):
		block = key >> self.numbits
		if self.aux is None:
			if self.numbits > 8:
				self.aux = VEB(self.numbits)
			else:
				self.aux = BitVEB(self.numbits)
		self.aux.insert(block)
		if block not in self.children:
			if self.numbits > 8: # only make real VEB for 16+ bit universe
				self.children[block] = VEB(self.numbits)
			else:
				self.children[block] = BitVEB(self.numbits)

		self.min = min(self.min, key)
		self.max = max(self.max, key)
		# return whether a new element was added
		return self.children[block].insert(key & ((1 << self.numbits) - 1))

	def next(self, key):
		if self.isEmpty() or key >= self.max:
			return None
		if key < self.min:
			return self.min

		block = key >> self.numbits
		pos = key & ((1 << self.numbits) - 1)

		if block in self.children:
			if pos < self.children[block].max:
				return (key ^ pos) | self.children[block].next(pos) #otherwise nextBlock needed

		nextBlock = self.aux.next(block) #nextBlock should exist
		return ((key ^ pos) | self.children[nextBlock].min) + ((nextBlock - block)  << self.numbits)

	def delete(self, key):
		if self.isEmpty():
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
			self.min = (self.aux.min  << self.numbits) | self.children[self.aux.min].min
		elif self.max == key:
			self.max = (self.aux.max << self.numbits) | self.children[self.aux.max].max
	
	def __str__(self):
		s = str((self.usize, self.min, self.max)) + "\nchildren"
		for i in self.children:
			s += str(i)
		return s

class BitVEB(VEB):
	def __init__(self, exp):
		self.usize = 1 << exp
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
		if key < self.min:
			return self.min
		x = self.bits >> (key + 1)
		# return lowest set bit after key bit
		return (x & -x).bit_length() + key

	def prev(self, key):
		if self.isEmpty() or key <= self.min:
			return None
		if key > self.max:
			return self.max
		# of the bits before key, return highest one
		return (self.bits & ((1 << key) - 1)).bit_length()
	
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
		return bin(self.bits)

if __name__ == "__main__":
<<<<<<< Updated upstream
	a = createVEB(200)
=======
	a = VEB(1000)
>>>>>>> Stashed changes
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
