import veb, cProfile, random

def denseRun(usz):
	a = veb.VEB(usz)
	for i in xrange(usz):
		a.insert(i)
	for i in xrange(usz):
		nxt = a.next(i-1)
		assert(nxt == i)
	for i in xrange(usz):
		a.delete(i)
	assert(a.isEmpty())
	for i in xrange(usz):
		assert(a.next(i) is None)

def sparseRun(n, usz):
	a = veb.VEB(usz)
	l = [random.randint(0, usz-1) for i in xrange(n)]
	l = list(set(l)) # remove repeats
	l.sort()
	n = len(l)
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
	cProfile.run("denseRun(1<<17)")
	cProfile.run("sparseRun(50000, 1<<32)")
	cProfile.run("sparseRun(90000, 1<<64)")
