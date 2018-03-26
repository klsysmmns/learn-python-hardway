people = 30
cars = 40
buses = 15

# decides if there are more cars than people
if cars > people:
    #runs this code if there are more cars than People
    print 'We should take the cars.'
#if there were not more cars than people it checks if there are less cars than people
elif cars < people:
    #if so prints this line
    print 'We should not take the cars.'
#if neither of those statements are true it runs this code
else:
    print 'We can\'t decide.'

if buses > cars:
    print 'That\'s too many buses.'
elif buses < cars:
    print 'Maybe we could take the buses.'
else:
    print 'We still can\'t decide.'

if people > buses:
    print 'Alright, let\'s just take the buses.'
else:
    print 'Fine, let\'s stay home then.'
