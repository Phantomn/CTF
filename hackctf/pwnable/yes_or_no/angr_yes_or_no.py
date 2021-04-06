import angr, sys

def main():
	p = angr.Project("./yes_or_no")
	init_state = p.factory.entry_state()
	simulation = p.factory.simgr(init_state)

	simulation.explore(find=is_successful, avoid=should_abort)

	if simulation.found:
		solution = simulation.found[0]
		print("flag: ", solution.posix.dumps(sys.stdin.fileno()))
	else:
		print("no flag")

def is_successful(state):
	return b"That's cool. Follow me" in state.posix.dumps(sys.stdout.fileno())
def should_abort(state):
	return b"Why are you here?" in state.posix.dumps(sys.stdout.fileno())

if __name__ == "__main__":
	main()