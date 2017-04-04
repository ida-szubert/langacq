import os

print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

print("This file path, relative to os.getcwd()")
print(__file__ + "\n")

print("This file full path (following symlinks)")
full_path = os.path.realpath(__file__)
print(full_path + "\n")

print("This file directory and name")
path, file = os.path.split(full_path)
print(path + ' --> ' + file + "\n")

print("This file directory only")
print(os.path.dirname(full_path))


print(os.path.dirname(os.path.realpath(__file__))+'/dax_examples/dax_example1')
f = open(os.path.dirname(os.path.realpath(__file__))+'/dax_examples/dax_example1')
for line in f:
    print(line)
f.close()
