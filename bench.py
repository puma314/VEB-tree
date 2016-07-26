import veb, cProfile, random

def run():
	a = veb.VEB(4)
	lim = 1 << (1 << 4)
	for i in xrange(lim):
		a.insert(i)
	for i in xrange(lim):
		nxt = a.next(i-1)
		assert(nxt == i)
	for i in xrange(lim):
		a.delete(i)
	assert(a.isEmpty())
	for i in xrange(lim):
		assert(a.next(i) is None)

def sparseRun(n):
	a = veb.VEB(5)
	lim = 1 << (1 << 5)
	l = [random.randint(0, lim-1) for i in xrange(n)]
	l = list(set(l)) # remove repeats
	l.sort()
	for i in l:
		a.insert(i)
	assert(a.next(-12) == l[0])
	for i in xrange(n):
		nxt = a.next(l[i])
		if i != n-1:
			assert(nxt == l[i+1])
		else:
			assert(nxt == None)
	for i in xrange(n):
		a.delete(l[i])
	assert(a.isEmpty())
	for i in xrange(n):
		assert(a.next(l[i]) is None)

if __name__ == "__main__":
	cProfile.run("sparseRun(50000)")
