import angr

p = angr.Project("r100", auto_load_libs=False)
path_group = p.factory.path_group()
print(path_group.explore(find=0x400844, avoid=0x400855))
print(path_group.found[0].state.posix.dumps(3))
