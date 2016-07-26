import bench

bench.denseRun(1<<17)
bench.sparseRun(30000,1<<64)

# make sure createVEB works and BitVEB on its own works
bench.denseRun(255)
bench.denseRun(256)
bench.sparseRun(100, 240)
