from mpi4py import MPI

comm = MPI.COMM_WORLD

print(" I am rank%d from %d" %(comm.rank, comm.size))

comm.Barrier()
