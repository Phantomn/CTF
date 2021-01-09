import angr,sys

def main():
    proj = angr.Project('./handray')
    init_state = proj.factory.entry_state()
    simulation = proj.factory.simgr(init_state)

    good=0x400586
    bad = 0x400597
    simulation.explore(find=good, avoid=bad)

    if simulation.found:
        solution = simulation.found[0]
        print('flag: ', solution.posix.dumps(sys.stdin.fileno()))
    else:
        print('no flag')

# set expected function
# note: sys.stdout.fileno() is the stdout file discription number. you can replace it by 1
# note: state.posix is the api for posix, and dumps(file discription number) will get the 
# bytes for the pointed file.
#def is_successful(state):
#    return b"That's cool. Follow me" in state.posix.dumps(sys.stdout.fileno())

# set disexpected function
#def should_abort(state):
#    return b"Why are you here?" in state.posix.dumps(sys.stdout.fileno())

if __name__ == '__main__':
    main()
