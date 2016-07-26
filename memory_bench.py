from memory_profiler import profile
import veb

@profile
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

if __name__ == "__main__":
	run()
