from sys import argv
from os.path import exists

script, from_file, to_file = argv

print 'Copying from {0} to {1}'.format(from_file, to_file)

# we could do these rwo on one line too, how?
input = open(from_file)
indata = input.read()

print 'The input file is {0} bytes long'.format(len(indata))

print 'Does the output file exist? {0}'.format(exists(to_file))
print 'Ready, hit RETURN to continue, CTRL-C to abort.'
raw_input()

output = open(to_file, 'w')
output.write(indata)

print 'Alright, we\'re done.'

output.close()
input.close()
