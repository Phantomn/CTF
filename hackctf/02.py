import angr
import sys

def main():
    p = angr.Project("./keygen")
    init_state = p.factory.entry_state()
    simulation = p.factory.simgr(init_state)
    good = 0x4009b3
    simulation.explore(find=good)
    
    if simulation.found:
        solution = simulation.found[0]
        print("flag : ", solution.posix.dumps(sys.stdin.fileno()))
    else:
        print("no flag")

#def is_successful(state):
#	return b"Good Job" in state.posix.dumps(sys.stdout.fileno())

#def should_abort(state):
#	return b"Try again" in state.posix.dumps(sys.stdout.fileno())

if __name__ == "__main__":
    main()
